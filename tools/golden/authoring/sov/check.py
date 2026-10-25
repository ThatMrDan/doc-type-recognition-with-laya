import json, re, collections, sys
rows=[json.loads(l) for l in open(sys.argv[1],encoding='utf-8')]
keys=["id","slice","generator","generator_family","prompt_id","attribute_cell","template_group","generator_label","edge_rule","expected_flags","parent_id","pair_id","text"]
assert all(list(r.keys())==keys for r in rows)
assert len({r['id'] for r in rows})==len(rows)
print(collections.Counter((r['slice'],r['generator_label']) for r in rows))
core=[r for r in rows if r['slice']=='core']
g=collections.Counter(r['template_group'] for r in core); print('core groups',len(g),'max',max(g.values()))
print('lengths core',collections.Counter(r['attribute_cell']['length'] for r in core))
print('lengths all',collections.Counter(r['attribute_cell']['length'] for r in rows))
for f in ['market','format','size','columns','valuation','currency']:
    print(f,dict(collections.Counter(r['attribute_cell'][f] for r in core)))
print('core without TIV', sum(not r['attribute_cell']['tiv_token'] for r in core))
banned_sub=["harbourline","kestrel","northgate","ashby","blackfriars","saltmarsh","redcliffe","fenwick","larkspur","tamar","wexcombe","aldgate","marsh","willis","lockton","howden","ajg","bms","brindle","copperleaf","merrow","ostrander","pellow","quarry lane","rowan","tillery","vance & hart","wickham","yardley","ebury"]
banned_word="aon amy tom lee kim sam ana raj zoe ben eve ola max ivy noah vance".split()
for r in rows:
    t=r['text'].lower()+' '+r['template_group'].lower()
    for b in banned_sub:
        if b in t: print('SUBSTR',r['id'],b)
    for b in banned_word:
        if re.search(r'\b'+b+r'\b',t): print('WORD',r['id'],b)
# arithmetic: last big number in a row == sum of a contiguous run of big numbers before it
def num(c):
    c=c.strip().replace('£','').replace('$','').replace('€','')
    if re.fullmatch(r'\d{1,3}([,.]\d{3})+|\d{4,}',c): return int(re.sub(r'[,.]','',c))
for r in rows:
    for line in re.split(r'\n| ; ',r['text']):
        cells=[c for c in re.split(r'\s*\|\s*|\s{2,}',line)]
        vals=[num(c) for c in cells]
        big=[v for v in vals if v and v>=10000]
        if len(big)<3: continue
        tail=[]
        for v in reversed(vals):
            if v is None or v<10000:
                if v==0 or (v is None and False): pass
                break
            tail.insert(0,v)
        ok=any(sum(big[i:-1])==big[-1] for i in range(len(big)-1))
        if not ok: print('SUM?',r['id'],line[:110])
