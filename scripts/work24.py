"""Work24 official recruitment list API integration (requires approved key)."""
import os,urllib.parse,urllib.request,xml.etree.ElementTree as ET,hashlib,re
URL='https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L01.do'
PATTERN=re.compile(r'펌웨어|임베디드|firmware|embedded|STM32|MCU|전장.*개발',re.I)
def text(node,*names):
 for name in names:
  x=node.findtext(name)
  if x:return x.strip()
 return ''
def fetch():
 key=os.getenv('WORK24_API_KEY','')
 if not key:return [],['고용24: WORK24_API_KEY 미설정 (API 신청 및 승인 필요)']
 out=[];errors=[]
 for page in range(1,4):
  args=urllib.parse.urlencode({'authKey':key,'callTp':'L','returnType':'XML','startPage':page,'display':100})
  try:
   req=urllib.request.Request(URL+'?'+args,headers={'User-Agent':'FirmwareCareerTracker/1.0'})
   with urllib.request.urlopen(req,timeout=25) as resp: root=ET.fromstring(resp.read())
   rows=root.findall('.//wanted')
   if not rows:
    errors.append('고용24: 응답 목록 없음 또는 API 응답 형식 확인 필요')
    break
   for x in rows:
    title=text(x,'title','wantedTitle')
    if not PATTERN.search(title):continue
    company=text(x,'company','companyNm')
    code=text(x,'wantedAuthNo','wantedNo')
    if not code:continue
    location=text(x,'region','workRegion')
    link='https://www.work24.go.kr/wk/a/b/1500/empDetailAuthView.do?'+urllib.parse.urlencode({'wantedAuthNo':code,'infoTypeCd':'VALIDATION','infoTypeGroup':'tb_workinfoworknet'})
    out.append({'id':hashlib.sha256(('work24'+code).encode()).hexdigest()[:20],'company':company,'title':title,'location':location,'url':link,'sector':'mid','sector_label':'중견·기타','salary_min_10k':None,'skills':[],'source':'고용24'})
  except Exception as exc:
   errors.append('고용24 API 오류: '+str(exc));break
 return out,errors
