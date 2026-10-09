"""Guard scholarly timeline scope and the manually reviewed CV workflow."""
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_publication_timeline import build_timeline

def record(identifier, year, category):
    return {'id': identifier, 'year': year, 'category': category, 'topics': ['test-domain'],
            'doi': None, 'url': 'https://example.org/paper', 'citation': 'Synthetic test record'}

class PublicationTimelineTests(unittest.TestCase):
    def setUp(self):
        self.config = {'domains': [{'label': 'Test domain', 'topics': ['test-domain']}], 'milestones': []}
        self.paper = record('test-article', 2020, 'First-Authored Articles')

    def test_nonscholarly_outputs_cannot_extend_bands(self):
        for category in ['Conference Abstracts', 'Working Papers', 'Technical Reports and Policy Contributions',
                         'Policy Brief', 'Selected Public and Policy Writing']:
            with self.subTest(category=category):
                records = [self.paper, record('test-early', 2010, category), record('test-late', 2030, category)]
                domains, _, first, last = build_timeline(records, self.config)
                self.assertEqual((first, last), (2020, 2020))
                self.assertEqual(domains[0]['years'], [2020])

    def test_articles_and_chapters_extend_bands(self):
        for category in ['First-Authored Articles', 'Co-Authored Articles', 'Book Chapters']:
            with self.subTest(category=category):
                _, _, first, last = build_timeline([self.paper, record('test-new', 2027, category)], self.config)
                self.assertEqual((first, last), (2020, 2027))

    def test_undated_record_does_not_extend_bands(self):
        _, _, first, last = build_timeline([self.paper, record('test-undated', None, 'Book Chapters')], self.config)
        self.assertEqual((first, last), (2020, 2020))

    def test_domain_needs_scholarly_support(self):
        with self.assertRaisesRegex(ValueError, 'peer-reviewed'):
            build_timeline([record('test-public', 2026, 'Selected Public and Policy Writing')], self.config)

    def test_public_writing_cannot_be_a_scholarly_milestone(self):
        self.config['milestones'] = [{'label': 'Test', 'summary': 'Test', 'papers': [{'id': 'test-public', 'label': 'Test'}]}]
        with self.assertRaisesRegex(ValueError, 'scholarly'):
            build_timeline([self.paper, record('test-public', 2026, 'Selected Public and Policy Writing')], self.config)

    def test_unknown_milestone_id_fails(self):
        self.config['milestones'] = [{'label': 'Test', 'summary': 'Test', 'papers': [{'id': 'missing', 'label': 'Test'}]}]
        with self.assertRaisesRegex(ValueError, 'Unknown milestone'):
            build_timeline([self.paper], self.config)

    def test_retired_generator_cannot_overwrite_reviewed_pdf(self):
        pdf = ROOT / 'assets/Md_Bodrud_Doza_Academic_CV.pdf'
        before = hashlib.sha256(pdf.read_bytes()).digest()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_cv.py')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('CV generation is retired', result.stderr)
        self.assertEqual(hashlib.sha256(pdf.read_bytes()).digest(), before)

if __name__ == '__main__':
    unittest.main()
