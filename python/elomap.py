import math

for rr in range(1,100):
	rrr = (100.0-rr)/rr
	rrrr = round(1000*math.log(rrr)/math.log(10))
	print(rrr,rrrr)