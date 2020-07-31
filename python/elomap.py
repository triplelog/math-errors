import math

for rr in range(1,100):
	rrr = (100.0-rr)/rr
	rrrr = math.round(1000*math.log(rrr)/math.log(10))
	print(rrr,rrrr)