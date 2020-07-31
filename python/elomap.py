import math

outstr = "flat_hash_map<int,int> eloMap; "
for rr in range(1,100):
	rrr = (100.0-rr)/rr
	rrrr = round(1000*math.log(rrr)/math.log(10))
	outstr += "eloMap["+str(rr)+"]="+str(rrrr)+"; "
print(outstr)