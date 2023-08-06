# 2022.11.21 cp from dsk_fastapi.py 
import json, requests,time,sys, traceback, difflib,os, spacy
import gecv1
if not hasattr(spacy, 'nlp'): 
	spacy.nlp = spacy.load(os.getenv('spacy_model', 'en_core_web_sm') ) 

def sntbr(essay, trim:bool=False, with_pid:bool=False): 
	''' sntbr("[\u8bd1\u6587]The 55-kilometre Hong Kong Zhuhai-Macau Bridge is an extraordinary engineering. It is the world's longest sea-crossing transportation system combining bridges and tunnels, which joins the three cities of Hong Kong Zhuhai and Macao, cutting the travelling time among them from 3 hours to 30 minutes. The reinforced concrete bridge with huge spans fully not only proves that China has the ability to complete the record-breaking mega-construction, but also will enhance the regional integration and boost the economic growth. It plays a crucial role in the overall plan to develop China’s Great Bay Area, which China intends to turn into one rivaling those of San Francisco, New York and Tokyo in terms of technological innovation and economic prosperity.") '''
	from spacy.lang import en
	if not hasattr(sntbr, 'inst'): 
		sntbr.inst = en.English()
		sntbr.inst.add_pipe("sentencizer")

	doc = sntbr.inst(essay)
	if not with_pid: return [ snt.text.strip() if trim else snt.text for snt in  doc.sents]
	pid = 0 #spacy.sntpidoff	= lambda essay: (pid:=0, doc:=spacy.sntbr(essay), [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid, doc[snt.start].idx))[-1] for snt in  doc.sents] )[-1]
	arr = []
	for snt in  doc.sents:
		if "\n" in snt.text: pid = pid + 1 
		arr.append( (snt.text, pid) ) 
	return arr 

def getdocs(snts, redis_r):
	if redis_r is None : return [spacy.nlp(snt) for snt in snts] 
	reslist = redis_r.mget([f"snt:{snt}" for snt in snts]) # prefill by spacy 3.4.1
	return  [ spacy.nlp(snt) if res is None else  spacy.tokens.Doc(spacy.nlp.vocab).from_json(json.loads(res) ) for snt, res in zip(snts, reslist) ]

trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
def mkf_input(snts, docs, tokenizer, sntdic:dict={},diffmerge:bool=False): # mkf input for 7095 java calling 
	srcs	= [ [t.text for t in doc] for doc in docs]
	tgts	= [ [t.text for t in doc] if ( snt not in sntdic or snt == sntdic.get(snt,snt) ) else [t.text for t in tokenizer(sntdic.get(snt,snt))] for snt, doc in zip(snts, docs)]
	input	= [ {"pid":0, "sid":i, "snt":snts[i], "tok": [t.text for t in doc],  
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": sntdic.get(snts[i],snts[i]), "diff": trans_diff_merge( srcs[i] , tgts[i]) if diffmerge else  trans_diff( srcs[i] , tgts[i] )	}
				for i, doc in enumerate(docs)]
	return input 

def xgecsnts(redis_gec, snts:list=["She has ready.","It are ok."], timeout:int=9,): #gechost:str='gpu120.wrask.com', gecport:int=6379
	''' {'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}  2022.11.21 '''
	if redis_gec is None: return {}
	id	= redis_gec.xadd("xsnts", {'snts':json.dumps(snts)})
	res = redis_gec.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	redis_gec.xdel("xsnts", id)
	return {} if res is None else json.loads(res[1])

def gecdsk(essay_or_snts:str="She has ready. It are ok.",timeout:int=9, redis_spacy=None, redis_gec=None,
		 use_gec:bool=True, topk_gec:int=64, gec_local:bool=False,
		dskhost:str='gpu120.wrask.com:7095'):  #gechost:str='gpu120.wrask.com', gecport:int=6379 ,
	''' assure: rgec_host is in the white ip list, added 2022.7.19 '''
	tims	= [time.time()]
	snts	= json.loads(essay_or_snts) if essay_or_snts.startswith('["') else sntbr(essay_or_snts)
	if redis_spacy: [redis_spacy.xadd('xsnt', {'snt':snt}, maxlen=30000) for snt in snts]

	sntdic = {} if not use_gec else xgecsnts(redis_gec, snts[0:topk_gec],timeout=timeout) if not gec_local else gecv1.gecsnts(snts[0:topk_gec])
	tims.append(time.time())
	
	docs	= getdocs(snts, redis_spacy) #[parse(snt) for snt in snts ] 
	tims.append(time.time())
	input	= mkf_input(snts, docs, spacy.nlp.tokenizer, sntdic)
	dsk		= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} ).encode("utf-8")}).json()
	tims.append(time.time())
	dsk['tim'] = {'gec': tims[1] - tims[0] , 'parse': tims[2] - tims[1] , 'mkf': tims[3] - tims[2] }
	return dsk

def uvirun(port): 
	''' python -m dsk.mkf uvirun 17095 '''
	import fastapi,uvicorn,redis
	app	= fastapi.FastAPI()

	@app.get('/')
	def home(): return fastapi.responses.HTMLResponse(content=f"<h2>dsk basic api</h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br> last update: 2022-11-21 <hr>")

	@app.post('/gecdsk')
	def gec_dsk(essay_or_snts:str="She has ready. It are ok.",timeout:int=9,  use_gec:bool=True, topk_gec:int=64, gec_local:bool=False,	
		spacyhost:str="hw160.jukuu.com:6626", gechost:str="gpu120.wrask.com:6379",	dskhost:str='gpu120.wrask.com:7095'):
		''' wrapper, 2022.11.21 '''
		if not hasattr(gec_dsk, 'spa'):
			gec_dsk.spa = redis.Redis(host=spacyhost.split(':')[0], port=int(spacyhost.split(':')[-1]), decode_responses=True)
			gec_dsk.gec = redis.Redis(host=gechost.split(':')[0], port=int(gechost.split(':')[-1]), decode_responses=True)
		return gecdsk(essay_or_snts,timeout=timeout, redis_spacy = gec_dsk.spa, redis_gec = gec_dsk.gec ,
			use_gec=use_gec, topk_gec=topk_gec, gec_local=gec_local, dskhost=dskhost)

	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == "__main__":  
	import fire
	print ( gecdsk(gec_local=True) )
	fire.Fire(uvirun)	