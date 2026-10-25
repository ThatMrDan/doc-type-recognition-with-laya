p='build_sov.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a)); s=s.replace(a,b)
rep('"PINEBROOK RISK ADVISORS ; Gem State Farm & Ranch Supply - 34 stores - ACV ; "','"PINEBROOK ; Gem State Farm Supply - ACV ; "')
rep('"SUMMIT PLAINS INSURANCE CO - SPX LOCATION EXTRACT - Pol SPP-0091744 - Lenape Valley Engineering PC\\n"','"SUMMIT PLAINS SPX EXTRACT - SPP-0091744 - Lenape Valley Engineering PC\\n"')
i=s.index('     (["3", "1", "5030 State Rte 9"'); j=s.index('\n',i)
s=s[:i]+s[j+1:]
rep('[8_100_000, 7_250_000, 1_300_000, 3_400_000]),','[8_100_000, 7_250_000, 1_300_000, 3_400_000])],')
rep('rows_shown="first 4 of 18"','rows_shown="first 2 of 18"')
rep('''         "NOTE: construction per owner's property managers, not verified. Values trended +6% over expiring.\\n" + t +''','''         "NOTE: construction per property managers, not verified.\\n" + t +''')
rep('| Account TIV $289,775,000 | Wind ded 2% named storm\\n"','| Account TIV $289,775,000\\n"')
rep(' - DO NOT REORDER COLUMNS\\n"','\\n"')
open(p,'w').write(s)
