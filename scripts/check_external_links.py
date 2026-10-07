"""Bounded manual external-link audit. Blocks and rate limits remain unverified.
Run after rendering. Confirmed HTTP 404/410 responses exit nonzero. Not run in CI.
"""
import argparse,concurrent.futures,json,time
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and urlsplit(a.get('href','')).scheme in ('http','https'):self.urls.add(a['href'])
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--timeout',type=float,default=8);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--max-seconds',type=float,default=180);ap.add_argument('--output');args=ap.parse_args()
 root=Path(__file__).resolve().parents[1];parser=Links()
 for f in (root/'_site').glob('*.html'):parser.feed(f.read_text(encoding='utf-8'))
 if not parser.urls:raise SystemExit('No rendered pages: run quarto render first.')
 started=time.monotonic()
 def check(url):
  if time.monotonic()-started>=args.max_seconds:return dict(url=url,result='unverified',reason='Time budget reached')
  try:
   request=Request(url,headers={'User-Agent':'AcademicSiteLinkCheck/1.0','Range':'bytes=0-1023'})
   with urlopen(request,timeout=args.timeout) as response:return dict(url=url,result='reachable',status=response.status,final_url=response.url)
  except HTTPError as exc:return dict(url=url,result='broken' if exc.code in (404,410) else 'unverified',status=exc.code,reason=str(exc.reason))
  except Exception as exc:return dict(url=url,result='unverified',reason=str(exc))
 with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(args.workers,8))) as pool:results=list(pool.map(check,sorted(parser.urls)))
 counts={key:sum(r['result']==key for r in results) for key in ['reachable','broken','unverified']};print(json.dumps(counts))
 for result in results:
  if result['result']!='reachable':print(json.dumps(result))
 if args.output:Path(args.output).write_text(json.dumps(dict(summary=counts,links=results),indent=2),encoding='utf-8')
 if counts['broken']:raise SystemExit(1)
if __name__=='__main__':main()
