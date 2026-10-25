import numpy as np, math
from scipy.stats import norm
rng=np.random.default_rng(1)
def ece(conf,corr,B=15):
    edges=np.linspace(0,1,B+1); b=np.clip(np.digitize(conf,edges)-1,0,B-1)
    return sum((b==i).mean()*abs(conf[b==i].mean()-corr[b==i].mean()) for i in range(B) if (b==i).any())
# two equally calibrated models, correlated confidences, same 500 items
for n in (500,2000):
  d=[]
  for _ in range(2000):
    u=rng.beta(9,1,n)
    ca=np.clip(u+rng.normal(0,0.03,n),0.2,0.999); cb=np.clip(u+rng.normal(0,0.03,n),0.2,0.999)
    z=rng.random(n)  # shared latent so correctness correlated
    ya=(z<ca).astype(float); yb=(z<cb).astype(float)
    d.append(ece(cb,yb)-ece(ca,ya))
  d=np.array(d); print(f"n={n}: ECE(B)-ECE(A) for identical true calibration: sd={d.std():.4f}, P(diff>0.02)={(d>0.02).mean():.3f}")
# per-class recall paired: n_c=100, discordant fraction among class items psi; MDE
def mde(n,psi,alpha=0.05,power=0.8):
    za=norm.ppf(1-alpha/2); zb=norm.ppf(power)
    lo,hi=1e-4,psi
    for _ in range(100):
        m=(lo+hi)/2; req=(za*math.sqrt(psi)+zb*math.sqrt(psi-m*m))**2/(m*m)
        lo,hi=(m,hi) if req>n else (lo,m)
    return hi
for nc in (50,100,150):
  print(nc,[ (psi,round(mde(nc,psi),3)) for psi in (0.04,0.08,0.12)])
# probability that a true drop of 0 trips a -0.05 point gate (no test), recall ~0.9, discordant psi
for nc in (50,100,150):
  for psi in (0.04,0.08,0.12):
    sims=[]
    for _ in range(20000):
        k=rng.binomial(nc,psi); down=rng.binomial(k,0.5); sims.append((k-2*down)/nc)  # B-A change
    sims=np.array(sims); print(f"nc={nc} psi={psi}: P(observed drop>0.05 | no true change)={(sims< -0.05).mean():.3f}")
# selective: coverage 0.8 of 500 -> 400 accepted; risk 0.02 Wilson
def wilson(x,n,z=1.96):
    p=x/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return round(c-h,4),round(c+h,4)
for acc_n,err in ((400,8),(400,4),(250,5)):
    print("selective risk",acc_n,err,wilson(err,acc_n))
# AURC* for error 0.1
r=0.1; print("AURC* r=0.1", r+(1-r)*math.log(1-r))
# precision reweighting example
