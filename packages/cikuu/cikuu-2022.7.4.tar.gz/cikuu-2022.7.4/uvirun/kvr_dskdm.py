# 2022.11.11 cp from uviredis.py  # 2022.8.6 cp from stream/uvirun.py  | rhost=172.18.0.1 uvicorn kvr_dskdm:app --host 0.0.0.0 --reload 
import json,requests,hashlib,os,time,redis,fastapi, uvicorn , random,asyncio, platform 
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse,  RedirectResponse

app	= globals().get('app', fastapi.FastAPI()) 
if not hasattr(redis,'r'): redis.r		= redis.Redis(host=os.getenv("rhost", "172.17.0.1" if not "Windows" in platform.system() else "110.40.247.167"), port=int(os.getenv('rport', 6666)), db=int(os.getenv('rdb', 0)), decode_responses=True) 
final_version = lambda rid="2696701":  [ (k.split('-')[-1], redis.r.zrevrange(k, 0, 0)[0].split(':')[0] ) for k in redis.r.keys(f"rid:{rid}:ver-score-uid-*")]
first_version = lambda rid="2696701":  [ (k.split('-')[-1], redis.r.zrange(k, 0, 0)[0].split(':')[0] ) for k in redis.r.keys(f"rid:{rid}:ver-score-uid-*")]

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> dskdm </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>")

@app.get('/dskdm/version')
def dsk_version(rids:str="2552283,2696701", final:bool=True): #, asdic:bool=False
	''' rid:1257077:ver-score-uid-23447214 '''
	res = []
	for rid in rids.strip().split(','):
		for k in redis.r.keys(f"rid:{rid}:ver-score-uid-*"):
			ver = redis.r.zrevrange(k, 0, 0)[0].split(':')[0] if final else redis.r.zrange(k, 0, 0)[0].split(':')[0]
			uid = k.split('-')[-1]
			arr = redis.r.hgetall(f"rid:{rid}:uid-{uid}:{ver}")
			arr.update({"rid":rid, "uid":uid, "ver":ver, 'final':final}) # add uname ? 
			res.append(arr) 
	return res  #if not asdic else { ar['uid']: ar  for ar in res}

@app.get('/dskdm/version_count')
def dsk_version_count(rids:str="2552283,2696701"):
	'''  '''
	return [ {"rid": rid, "uid": k.split('-')[-1],  "count": redis.r.zcard(k)} for rid in rids.strip().split(',') for k in redis.r.keys(f"rid:{rid}:ver-score-uid-*") ]

@app.get('/dskdm/hgetall')
def dsk_hgetall(key:str="cate", keyname:str='key', valname:str='value'):
	'''  '''
	return [ {keyname: k, valname: v} for k,v in redis.r.hgetall(key).items() ]

@app.get('/dskdm/snt')
def dsk_snt(rids:str="2552283,2696701", field:str='tok'):
	''' grafana: extract fields '''
	res = []
	for rid in rids.strip().split(','):
		for uid, ver in final_version(rid): 
			for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
				v = redis.r.hget(f"snt:{snt}", field)
				if field in ("tok",'feedback','chunk'): # [{},{},...]
					[res.append( {"rid":rid, "uid":uid, "snt":snt, field: json.dumps(ar)} ) for ar in json.loads(v)]
				else: 
					res.append( {"rid":rid, "uid":uid, "snt":snt, field: v} )
	return res

@app.get('/dskdm/cate-in-snt')
def dsk_cate_in_snt(rids:str="2552283,2696701", hkey:str='feedback', field:str='topcate', value:str='snt', topk:int=10):
	''' 2022.11.21 '''
	res = []
	for rid in rids.strip().split(','):
		for uid, ver in final_version(rid): 
			for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
				v = redis.r.hget(f"snt:{snt}", hkey)
				if v: #feedback	= lambda arr : [ {"cate":v.get('cate',''), "topcate": v.get('cate','').split('.')[0][2:], "ibeg": v.get('ibeg',-1),"kp": v.get('kp',''), "msg":v.get("short_msg","")} for k,v in arr.items() if v.get('cate','').startswith( ("e_","w_") )]
					for ar in json.loads(v):
						if ar.get(field,'') == value: 
							res.append( dict(ar, **{"rid":rid, "uid":uid, "ver":ver, "snt":snt}) )
							break
				if len(res) >= topk: return res
	return res

@app.get('/dskdm/essay')
def dsk_essay(rid:str="2235895", uid:str="30031900",  ver:int=2):
	''' rid:2235895:ver-score-uid-30031900 '''
	arr = redis.r.hgetall(f"rid:{rid}:uid-{uid}:{ver}")
	snts = json.loads(arr['snts']) 
	arr['mkf'] = [redis.r.hgetall(f"snt:{snt}") for snt in snts ]
	return arr

if __name__ == '__main__':	 #uvicorn.run(app, host='0.0.0.0', port=16379)
	print( dsk_cate_in_snt() )

'''
from collections import Counter
@app.get('/dskdm/tok/si')
def dsk_tok_si(rid:str="2235895", field:str='pos'):
	#data for pos chart, field: pos/lex 
	si = Counter()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			[ si.update({t[field]:1}) for t in json.loads(arr['tok']) ]
	return si.most_common()

@app.get('/dskdm/cate')
def dsk_cate(rid:str="2235895"):
	si = Counter()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			for kp,v  in json.loads(arr['feedback']).items(): 
				if v['cate'].startswith ( ('e_', 'w_') ): 
					si.update({v['cate']:1})
	return si.most_common()

@app.get('/dskdm/lemma')
def dsk_lemma(rid:str="2696716", pos:str='VERB'):
	si = Counter()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			[ si.update({t['lem']:1}) for t in json.loads(arr['tok']) if t['pos'] == pos ]
	return si.most_common()

@app.get('/dskdm/trp')
def dsk_trp(rid:str="2696716", gpos:str='VERB', pos:str='NOUN', dep:str='dobj'):
	si = Counter()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			[ si.update({t['glem'] +":"+ t['lem']:1}) for t in json.loads(arr['tok']) if t['gpos'] == gpos and t['pos'] == pos and t['dep'] == dep ]
	return si.most_common()

@app.get('/dskdm/cate_in_snt')
def dsk_cate_in_snt(rid:str="2696716", cate:str='w_trp.chig', topk:int=10):
	snts = set()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			for kp, v in json.loads(arr['feedback']).items():
				if v['cate'] == cate :
					snts.add(snt)
					break
	return snts

@app.get('/dskdm/lemma_in_snt')
def dsk_lemma_in_snt(rid:str="2696716", pos:str='VERB', lemma:str='visit', topk:int=10):
	snts = set()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			for t in json.loads(arr['tok']):
				if t['pos'] == pos and t['lem'] == lemma:
					snts.add(snt)
					break
	return snts

@app.get('/dskdm/trp_in_snt')
def dsk_trp_in_snt(rid:str="2696716", gpos:str='VERB', glem:str='visit', pos:str='NOUN', lem:str='parent', dep:str='dobj'):
	snts = set()
	for uid, ver in final_version(rid): 
		for snt in json.loads(redis.r.hget(f"rid:{rid}:uid-{uid}:{ver}", 'snts')):
			arr = redis.r.hgetall(f"snt:{snt}")
			for t in json.loads(arr['tok']):
				if t['pos'] == pos and t['lem'] == lem and t['gpos'] == gpos and t['glem'] == glem and t['dep'] == dep:
					snts.add(snt)
					break
	return snts
'''