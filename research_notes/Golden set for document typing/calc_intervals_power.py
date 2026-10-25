import math
from scipy import stats
z=1.959964
def wilson(x,n):
    p=x/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def cp(x,n):
    lo=stats.beta.ppf(0.025,x,n-x+1) if x>0 else 0; hi=stats.beta.ppf(0.975,x+1,n-x) if x<n else 1; return lo,hi
for n in (50,100,150):
  for p in (0.80,0.90,0.95,0.98,1.0):
    x=round(p*n); lo,hi=wilson(x,n); a,b=cp(x,n)
    print(f"n={n} x={x} phat={x/n:.3f} wald_half={z*math.sqrt(p*(1-p)/n):.3f} wilson=[{lo:.3f},{hi:.3f}] width/2={(hi-lo)/2:.3f} CP=[{a:.3f},{b:.3f}]")
print("n for wald half-width 0.05:",[ (p,math.ceil(z*z*p*(1-p)/0.05**2)) for p in (0.5,0.8,0.9,0.95)])
print("n for half 0.03:",[ (p,math.ceil(z*z*p*(1-p)/0.03**2)) for p in (0.8,0.9,0.95)])
# rule of three
for n in (50,100,150): print("zero errors n",n,"upper 95% one-sided",3/n, 1-0.05**(1/n))
# McNemar power: overall n=500, detect difference delta given discordant rate psi
from scipy.stats import norm
def mcn_n(delta,psi,alpha=0.05,power=0.8):
    za=norm.ppf(1-alpha/2); zb=norm.ppf(power)
    return (za*math.sqrt(psi)+zb*math.sqrt(psi-delta**2))**2/delta**2
def mcn_mde(n,psi,alpha=0.05,power=0.8):
    lo,hi=1e-4,psi
    for _ in range(100):
        m=(lo+hi)/2
        if mcn_n(m,psi,alpha,power)>n: lo=m
        else: hi=m
    return hi
for N in (100,500):
  for psi in (0.02,0.05,0.10,0.15):
    print(f"N={N} discordant={psi} MDE(80% power,a=.05)={mcn_mde(N,psi):.3f}")
# unpaired comparison MDE for two proportions each n, p=0.9
for n in (100,500):
    p=0.9; print("unpaired MDE n",n, (1.96+0.8416)*math.sqrt(2*p*(1-p)/n))
# ECE bias: perfectly calibrated model, conf ~ high, n samples, 15 bins
import numpy as np
rng=np.random.default_rng(0)
def ece(conf,correct,B=15,mass=False):
    if mass:
        idx=np.argsort(conf); bins=np.array_split(idx,B)
    else:
        edges=np.linspace(0,1,B+1); b=np.clip(np.digitize(conf,edges)-1,0,B-1); bins=[np.where(b==i)[0] for i in range(B)]
    e=0
    for ix in bins:
        if len(ix): e+=len(ix)/len(conf)*abs(conf[ix].mean()-correct[ix].mean())
    return e
for n in (100,500,2000,10000):
  for mass in (False,True):
    es=[]
    for _ in range(500):
        conf=rng.beta(9,1,n)  # mean 0.9, calibrated
        corr=(rng.random(n)<conf).astype(float)
        es.append(ece(conf,corr,15,mass))
    es=np.array(es); print(f"calibrated n={n} {'equal-mass' if mass else 'equal-width'} 15 bins: mean ECE={es.mean():.4f} sd={es.std():.4f} p95={np.quantile(es,.95):.4f}")
# difference of two calibrated models' ECE sd (independent-ish)
