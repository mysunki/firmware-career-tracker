#!/usr/bin/env python3
"""Fetch verified public Greenhouse/Lever postings; never invent salaries."""
import datetime,json,pathlib,re,urllib.request,urllib.parse,hashlib,html
ROOT=pathlib.Path(__file__).resolve().parents[1]
KEYWORDS=re.compile(r'firmware|embedded|펌웨어|임베디드|STM32|RTOS|\bMCU\b|전장.*개발',re.I)
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'FirmwareCareerTracker/1.0','Accept':'application/json'})
 with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
def strip(s):return re.sub('<[^>]*>',' ',html.unescape(str(s or '')))
def main():
 config=json.loads((ROOT/'data/sources.json').read_text())
 out=[];errors=[]
 for b in config.get('boards',[]):
  provider=b.get('provider','').lower();token=b.get('token','');company=b.get('company','');sector=b.get('sector','mid')
  if not re.fullmatch(r'[\w-]+',token):errors.append('Invalid board token: '+company);continue
  try:
   if provider=='greenhouse':
    rows=fetch('https://boards-api.greenhouse.io/v1/boards/'+token+'/jobs?content=true')['jobs']
    items=[(str(x['id']),x.get('title',''),(x.get('location') or {}).get('name',''),x.get('absolute_url',''),strip(x.get('content',''))) for x in rows]
   elif provider=='lever':
    rows=fetch('https://api.lever.co/v0/postings/'+token+'?mode=json')
    items=[(str(x['id']),x.get('text',''),(x.get('categories') or {}).get('location',''),x.get('hostedUrl',''),strip(x.get('descriptionPlain',''))) for x in rows]
   else:raise ValueError('unsupported provider')
   for key,title,location,url,desc in items:
    if not KEYWORDS.search(title+' '+desc) or not url.startswith('https://'):continue
    out.append({'id':hashlib.sha256((provider+key).encode()).hexdigest()[:20],'company':company,'title':title,'location':location,'url':url,'sector':sector,'sector_label':{'medical':'의료기기','large':'대기업','automotive':'자동차·전장','mid':'중견·기타'}.get(sector,'기타'),'salary_min_10k':None,'skills':[s for s in ['STM32','MCU','UART','SPI','I2C','DMA','RTOS','CAN','C++'] if s.lower() in (title+' '+desc).lower()],'source':provider})
  except Exception as exc:errors.append(company+': '+str(exc))
 target=ROOT/'data/jobs.json'
 old=json.loads(target.read_text()) if target.exists() else {'jobs':[]}
 from work24 import fetch as fetch_work24
 work24_jobs,work24_errors=fetch_work24()
 out.extend(work24_jobs)
 errors.extend(work24_errors)
 if errors and not out and old.get('jobs'):out=old['jobs']
 target.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobs':out,'errors':errors},ensure_ascii=False,indent=2)+'\n')
 print('Jobs:',len(out),'errors:',errors)
if __name__=='__main__':main()
