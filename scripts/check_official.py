#!/usr/bin/env python3
"""Check configured official career pages for reachability and content changes.
A changed page is NOT proof of a new open job. No credentials or scraping bypass.
"""
import concurrent.futures,datetime,hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def check(page):
 try:
  req=urllib.request.Request(page['url'],headers={'User-Agent':'Mozilla/5.0 (compatible; CareerTracker/1.0)'})
  with urllib.request.urlopen(req,timeout=15) as res:
   raw=res.read(1024*1024)
   final=res.geturl()
  return dict(page,status='ok',url=final,sha256=hashlib.sha256(raw).hexdigest(),error=None)
 except Exception as exc:return dict(page,status='error',sha256=None,error=str(exc)[:250])
def main():
 config=json.loads((ROOT/'data/official_sources.json').read_text())
 path=ROOT/'data/official_results.json'
 try:previous={x['company']:x for x in json.loads(path.read_text()).get('pages',[])}
 except (OSError,ValueError):previous={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:pages=list(pool.map(check,config['pages']))
 for p in pages:
  old=previous.get(p['company'],{})
  p['changed']=bool(p['sha256'] and old.get('sha256') and p['sha256']!=old['sha256'])
  p['last_success_at']=datetime.datetime.now(datetime.timezone.utc).isoformat() if p['status']=='ok' else old.get('last_success_at')
  if not p['sha256'] and old.get('sha256'):p['sha256']=old['sha256']
 path.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':pages},ensure_ascii=False,indent=2)+'\n')
 print('Official career pages checked:',len(pages),'ok:',sum(p['status']=='ok' for p in pages))
if __name__=='__main__':main()
