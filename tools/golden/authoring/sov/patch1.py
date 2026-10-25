p='build_sov.py'; s=open(p).read()
def rm(sub, count=1):
    global s
    assert s.count(sub)==count, (sub[:60], s.count(sub)); s=s.replace(sub,'')
def rep(a,b,count=1):
    global s
    assert s.count(a)==count, (a[:60], s.count(a)); s=s.replace(a,b)
def cut(a, b_end):
    """remove from start of a to end of b_end (inclusive)"""
    global s
    i=s.index(a); j=s.index(b_end,i)+len(b_end); s=s[:i]+s[j:]
rm('''     (["1", "2", "4410 Industrial Pkwy", "Fresno", "CA", "93725", "Office", "2", "1998", "9,600", "2", "Y", "3"], [1_650_000, 240_000, 0]),\n''')
# r2 keep first 3
cut('     (["4", "1", "910 Hollis Ave"', '[380_000, 0, 0, 0])],\n')
rep('[1_900_000... ','',0) if False else None
rep('(["3", "1", "5030 State Rte 9", "Findlay", "OH", "Tool & die", "2", "1962", "31,200", "1", "N", "5"], [2_350_000, 2_900_000, 220_000, 0]),',
    '(["3", "1", "5030 State Rte 9", "Findlay", "OH", "Tool & die", "2", "1962", "31,200", "1", "N", "5"], [2_350_000, 2_900_000, 220_000, 0])],')
rep('rows_shown="first 8 of 18"','rows_shown="first 4 of 18"')
# r5 keep rows 1,2,4
cut('     (["3", "7 Pequot Dr"', '[21_300_000, 900_000, 350_000, 1_800_000])],\n')
rep('[9_800_000, 450_000, 150_000, 700_000]),','[9_800_000, 450_000, 150_000, 700_000]),\n     (["3", "2290 Post Rd", "Warwick RI", "Office - medical tenants", "JM/frame w mansard", "1968 / HVAC 2016", "18,200", "2", "Partial"], [2_750_000, 150_000, 0, 300_000])],\n')
rep('rows_shown="first 5 of 23"','rows_shown="first 3 of 23"')
# r8 keep 2
cut('              (["103", "9 Yellowstone Ave"', '[0, 290_000, 720_000])],\n')
rep('(["102", "220 N Main", "Pocatello", "ID"], [1_200_000, 340_000, 980_000]),','(["102", "220 N Main", "Pocatello", "ID"], [1_200_000, 340_000, 980_000])],\n')
rep('rows_shown="first 6 of 34"','rows_shown="first 2 of 34"')
rep('"PINEBROOK RISK ADVISORS ; Gem State Farm & Ranch Supply Inc - 34 stores - ACV basis - Bldg blank where leased ; "','"PINEBROOK RISK ADVISORS ; Gem State Farm & Ranch Supply - 34 stores - ACV ; "')
rm("Insulated panel type: polyisocyanurate (Loc 1, 3), approved PIR (Loc 2). Ammonia refrigeration all locations.\n")
cut("4 | 2200 Wilkinson Blvd", "BUR (3, 4, 5, 7).\n")
rep('rows_shown="first 7 of 27"','rows_shown="first 3 of 27"')
cut('          "003 | Bridgwater', '"007 | Penzance | TR18 2QW | Leasehold | 0 | 140,000 | 29,000 | 169,000")')
rep('"002 | Yeovil | BA20 1EG | Leasehold | 0 | 160,000 | 38,500 | 198,500 ; "\n','"002 | Yeovil | BA20 1EG | Leasehold | 0 | 160,000 | 38,500 | 198,500")\n')
rep('rows_shown="first 7 of 186"','rows_shown="first 2 of 186"')
rep('"CALLOWAY PRENTICE | Brackenhurst Opticians plc - store schedule (186 branches) | Reinstatement / Contents new for old ; "','"CALLOWAY PRENTICE | Brackenhurst Opticians plc - 186 branches | Reinstatement ; "')
rm("5 | Unit 3 Burton Latimer NN15 5YT | Bonded warehouse | Steel frame, LPCB panels | 2012 | 11,200 | In-rack | 7,800,000 | 900,000 | 14,600,000 | 23,300,000\n")
rep('rows_shown="first 5 of 14"','rows_shown="first 4 of 14"')
cut('          "FRA-1 | Frankfurt', '250,000,000 | 270,000,000")')
rep('"AMS-2 | Amsterdam | 34,000,000 | 61,000,000 | 15,000,000 | 110,000,000 | 118,800,000 ; "\n','"AMS-2 | Amsterdam | 34,000,000 | 61,000,000 | 15,000,000 | 110,000,000 | 118,800,000")\n')
rep('"LINDQVIST BROKERAGE | Arcwell Compute Inc. - European sites for US master program | RC | FX 1 EUR = 1.08 USD ; "','"LINDQVIST BROKERAGE | Arcwell Compute Inc. - EU site, US master program | RC | 1 EUR = 1.08 USD ; "')
cut('          "4 | 1012 | 120 E Hwy 60', '| 115,000 | 1,550,000")')
rep('290,000 | 2,995,000\\n"\n','290,000 | 2,995,000")\n')
rep('rows_shown="first 8 of 212"','rows_shown="first 3 of 212"')
cut('          "3 | 1 | 410 S Tryon St', '130,000 | 1,295,000")')
rep('240,000 | 2,280,000\\n"\n','240,000 | 2,280,000")\n')
rep('rows_shown="first 7 of 131"','rows_shown="first 3 of 131"')
cut('          "0003 | 22 COURT SQ', '240,000 | 610,000")')
rep('"0002 | 501 E PASS RD | GULFPORT | MS | METAL BLDG | N | 0 | 160,000 | 335,000 | 495,000 ; "\n','"0002 | 501 E PASS RD | GULFPORT | MS | METAL BLDG | N | 0 | 160,000 | 335,000 | 495,000")\n')
rep('rows_shown="first 5 of 260"','rows_shown="first 2 of 260"')
rep('"OKONKWO HALE & PARTNERS ; DOLLARWISE DISCOUNT STORES INC - 260 STORES - ACV ; "','"OKONKWO HALE ; DOLLARWISE DISCOUNT STORES - 260 STORES - ACV ; "')
cut('          "002|01|18 Stone Mill Rd', '150,000|1,270,000")')
rep('1,200,000|11,750,000\\n"\n','1,200,000|11,750,000")\n')
rep('rows_shown="first 3 of 12"','rows_shown="first 1 of 12"')
open(p,'w').write(s)
