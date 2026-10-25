import json,re,sys
rows=[json.loads(l) for l in open(sys.argv[1],encoding='utf-8')]
def num(c):
    c=c.strip().replace('£','').replace('$','').replace('€','')
    if re.fullmatch(r'\d{1,3}([,.]\d{3})+|\d+',c): return int(re.sub(r'[,.]','',c))
for r in rows:
    lines=[l for l in re.split(r'\n| ; ',r['text'])]
    tab=[]
    for l in lines:
        cells=[c.strip() for c in re.split(r'\s*\|\s*',l)]
        if re.match(r'(?i)^(grand )?(total|tot)s?\b',cells[0]):
            body=[t for t in tab if len(t)==len(cells)]
            bad=[]
            for j,c in enumerate(cells):
                v=num(c)
                if v is None or v<1000: continue
                col=[num(t[j]) for t in body]
                if all(x is not None for x in col) and sum(col)!=v: bad.append((j,v,sum(col)))
            print(r['id'],'rows',len(body),'BAD' if bad else 'ok',bad)
            tab=[]
        else: tab.append(cells)
    w=len(re.findall(r"[A-Za-z0-9£$€][^\s|;]*", r['text']))
