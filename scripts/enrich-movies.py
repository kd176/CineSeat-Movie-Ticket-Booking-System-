"""Refresh locally saved poster assets from reviewed posterRemote URLs.
Run explicitly from the project directory; never replaces film metadata.
Sources and snapshot dates are retained in server/enrichment.json and releases.json.
Requires Pillow. Failed downloads retain the existing asset or remote fallback.
"""
import json,pathlib,urllib.request,io,concurrent.futures
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
enrichment=json.loads((ROOT/'server/enrichment.json').read_text())
releases=json.loads((ROOT/'server/releases.json').read_text())
def download(pair):
 key,item=pair
 try:
  raw=urllib.request.urlopen(item['posterRemote'],timeout=20).read(10000000)
  im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((600,900))
  target=ROOT/'public/posters'/f'{key}.jpg';target.parent.mkdir(exist_ok=True)
  im.save(target,quality=85,optimize=True);item['poster']='/posters/'+key+'.jpg'
  return key,'saved'
 except Exception as error:return key,str(error)
if __name__=='__main__':
 jobs=list(enrichment.items())+[(r['id'],r) for r in releases]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(download,jobs):print(result,flush=True)
 (ROOT/'server/enrichment.json').write_text(json.dumps(enrichment,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'server/releases.json').write_text(json.dumps(releases,indent=2,ensure_ascii=False)+'\n')
