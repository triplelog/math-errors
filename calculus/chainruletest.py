from powerrule import powerrule
from trigrule import trigrule
from expolog import exporule

def fullparen(input_string):
	openpar = 0
	isbreak = 0
	cancel_it = 0
	really_cancel = 0
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			cancel_it = 1
			isbreak = idx
			break
	if isbreak == len(input_string)-1:
		return True
	else:
		if input_string[0:3] in ['log','sin','cos','tan','cot','sec','csc']:
			return fullparen(input_string[3:])
		elif input_string[0:2] in ['ln']:
			return fullparen(input_string[2:])
		elif input_string[0:6] in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
			return fullparen(input_string[6:])
		else:
			try:
				floatexp = float(input_string)
				return True
			except:
				return False

def checkifdvar(input_string,dvar):
	spart = input_string
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		spart=spart.replace(sstr,'')
	if spart.find(dvar)>-1:
		return True
	else:
		return False
def checkpower(inputexpression,dvar):
	#print inputexpression, 'hhhh'
	power_spots = []
	if inputexpression[0:5]=='sqrt(':
		if fullparen(inputexpression[4:]):
			return [True,powerrule(inputexpression,inputexpression[4:])[1],inputexpression[4:]]
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		for i in power_spots:
			if fullparen(inputexpression[:i+1]):
				if fullparen(inputexpression[i+2:]):
					if checkifdvar(inputexpression[:i+1],dvar):
						if not checkifdvar(inputexpression[i+2:],dvar):
							return [True,powerrule(inputexpression,inputexpression[:i+1])[1],inputexpression[:i+1]]
		return [False,inputexpression]
	else:
		return [False,inputexpression]

def checkexpo(inputexpression,dvar):
	power_spots = []
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		for i in power_spots:
			if fullparen(inputexpression[:i+1]):
				if fullparen(inputexpression[i+2:]):
					if not checkifdvar(inputexpression[:i+1],dvar):
						if checkifdvar(inputexpression[i+2:],dvar):
							return [True,exporule(inputexpression,inputexpression[i+2:])[1],inputexpression[i+2:]]
		return [False,inputexpression]
	else:
		return [False,inputexpression]

def checklog(inputexpression,dvar):
	if inputexpression[:4]=='log(':
		if fullparen(inputexpression[3:]):
			the_exponent = inputexpression[4:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar):
				return [True,'1/('+the_exponent+')',the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	elif inputexpression[:3]=='ln(':
		if fullparen(inputexpression[2:]):
			the_exponent = inputexpression[3:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar):
				return [True,'1/('+the_exponent+')',the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def checktrig(inputexpression,dvar,tf):
	if inputexpression[:4]==tf+'(':
		if fullparen(inputexpression[3:]):
			the_exponent = inputexpression[4:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar):
				return [True,trigrule(inputexpression,the_exponent)[1],the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def checkitrig(inputexpression,dvar,tf):
	if inputexpression[:7]==tf+'(':
		if fullparen(inputexpression[6:]):
			the_exponent = inputexpression[7:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar):
				return [True,trigrule(inputexpression,the_exponent)[1],the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]

def chainrule(inputexpression,dvar):
	expo_chain = checkexpo(inputexpression,dvar)
	log_chain = checklog(inputexpression,dvar)
	power_chain = checkpower(inputexpression,dvar)
	trig_chain = []
	for tf in ['sin','cos','tan','cot','sec','csc']:
		trig_chain.append(checktrig(inputexpression,dvar,tf))
	for itf in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
		trig_chain.append(checkitrig(inputexpression,dvar,itf))
	if expo_chain[0]:
		return expo_chain
	elif log_chain[0]:
		return log_chain
	elif power_chain[0]:
		return power_chain
	else:
		for i in range(0,len(trig_chain)):
			if trig_chain[i][0]:
				return trig_chain[i]
	return [False, inputexpression]

