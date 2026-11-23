#!/usr/bin/env python3
"""Monitor company-specific recruitment mentions via public Google News RSS search.
Search results are leads, not verified active job openings.
"""
import datetime,email.utils,hashlib,json,pathlib,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
ROOT=pathlib.Path(__file__).resolve().parents[1]
QUERY='(펌웨어 OR 임베디드 OR firmware OR embedded OR STM32 OR MCU) (채용 OR 모집 OR hiring)'
def search_company(company):
 leads=[]
 q='"'+company+'" '+QUERY
 url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q,'hl':'ko','gl':'KR','ceid':'KR:ko'})
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; FirmwareCareerTracker/1.0)'})
 with urllib.request.urlopen(req,timeout=12) as res:root=ET.fromstring(res.read())
 for node in root.findall('.//item')[:20]:
  title=node.findtext('title','').strip();link=node.findtext('link','').strip()
  date=node.findtext('pubDate','')
  try:published=email.utils.parsedate_to_datetime(date).isoformat()
  except Exception:published=None
  if not link.startswith('https://'):continue
  leads.append({'id':hashlib.sha256((company+link).encode()).hexdigest()[:20],'company':company,'title':title,'url':link,'published_at':published,'source':'Google News RSS','verified_opening':False})
 return leads

def main():
 names=json.loads((ROOT/'data/watchlist.json').read_text()).get('companies',[])
 companies=list(dict.fromkeys((x if isinstance(x,str) else x.get('name','')).strip() for x in names[:50]))
 companies=[x for x in companies if x]
 leads=[];errors=[]
 with ThreadPoolExecutor(max_workers=6) as pool:
  futures={pool.submit(search_company,company):company for company in companies}
  for future in as_completed(futures):
   company=futures[future]
   try:leads.extend(future.result())
   except Exception as exc:errors.append(company+': '+str(exc))
 path=ROOT/'data/watch_results.json'
 if errors and not leads and path.exists():
  old=json.loads(path.read_text());leads=old.get('leads',[])
 path.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'leads':leads,'errors':errors,'companies_checked':len(companies)},ensure_ascii=False,indent=2)+'\n')
 print('watch companies:',len(companies),'leads:',len(leads),'errors:',len(errors))
if __name__=='__main__':main()
