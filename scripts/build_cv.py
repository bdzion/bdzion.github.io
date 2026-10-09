"""Retired: the manually reviewed academic CV PDF is the canonical version.

This entry point deliberately refuses to generate or overwrite the public CV.
Replace assets/Md_Bodrud_Doza_Academic_CV.pdf with a reviewed export from the
owner's master document, following MAINTENANCE_GUIDE.md section J.
"""
if __name__ == '__main__':
    raise SystemExit(
        'CV generation is retired. The reviewed PDF in '
        'assets/Md_Bodrud_Doza_Academic_CV.pdf is canonical. '
        'Export the updated master CV, review every page, and replace the PDF '
        'using the same filename. See MAINTENANCE_GUIDE.md section J.'
    )
