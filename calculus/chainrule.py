from powerrule import powerrule
from trigrule import trigrule
from expolog import exporule
import sympy
from clean import post_clean
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

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

def checkifdvar(input_string,dvar,idvar):
	spart = input_string
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		spart=spart.replace(sstr,'')
	if spart.find(dvar)>-1:
		return True
	elif spart.find(idvar)>-1:
		return True
	else:
		return False
def checkpower(inputexpression,dvar,idvar):
	#print inputexpression, 'hhhh'
	power_spots = []
	if inputexpression[0:5]=='sqrt(':
		if fullparen(inputexpression[4:]):
			return [True,powerrule(inputexpression,inputexpression[5:len(inputexpression)-1],idvar)[1],inputexpression[4:],'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)=sqrt(U)</div> and <div class="katex_div_il">g('+dvar+')='+slatex(inputexpression[4:])+'</div>',0]
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		for i in power_spots:
			if fullparen(inputexpression[:i+1]):
				if fullparen(inputexpression[i+2:]):
					if checkifdvar(inputexpression[:i+1],dvar,idvar):
						if not checkifdvar(inputexpression[i+2:],dvar,idvar):
							return [True,powerrule(inputexpression,inputexpression[:i+1],idvar)[1],inputexpression[:i+1],'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)=U^'+inputexpression[i+2:]+'</div> and <div class="katex_div_il">g('+dvar+')='+slatex(inputexpression[:i+1])+'</div>',0]
		return [False,inputexpression]
	else:
		return [False,inputexpression]

def checkexpo(inputexpression,dvar,idvar):
	power_spots = []
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		for i in power_spots:
			if fullparen(inputexpression[:i+1]):
				if fullparen(inputexpression[i+2:]):
					if not checkifdvar(inputexpression[:i+1],dvar,idvar):
						if checkifdvar(inputexpression[i+2:],dvar,idvar):
							return [True,exporule(inputexpression,inputexpression[i+2:])[1],inputexpression[i+2:],'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)='+inputexpression[:i+1]+'^U</div> and <div class="katex_div_il">g('+dvar+')='+slatex(inputexpression[i+2:])+'</div>',2]
		return [False,inputexpression]
	else:
		return [False,inputexpression]

def checklog(inputexpression,dvar,idvar):
	if inputexpression[:4]=='log(':
		if fullparen(inputexpression[3:]):
			the_exponent = inputexpression[4:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar,idvar):
				return [True,'1/('+the_exponent+')',the_exponent,'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)=log(U)</div> and <div class="katex_div_il">g('+dvar+')='+slatex(the_exponent)+'</div>',1]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	elif inputexpression[:3]=='ln(':
		if fullparen(inputexpression[2:]):
			the_exponent = inputexpression[3:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar,idvar):
				return [True,'1/('+the_exponent+')',the_exponent,'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)=ln(U)</div> and <div class="katex_div_il">g('+dvar+')='+slatex(the_exponent)+'</div>',1]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def checktrig(inputexpression,dvar,idvar,tf):
	if inputexpression[:4]==tf+'(':
		if fullparen(inputexpression[3:]):
			the_exponent = inputexpression[4:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar,idvar):
				return [True,trigrule(inputexpression,the_exponent)[1],the_exponent,'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)='+slatex(tf)+'(U)</div> and <div class="katex_div_il">g('+dvar+')='+slatex(the_exponent)+'</div>',3]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def checkitrig(inputexpression,dvar,idvar,tf):
	if inputexpression[:7]==tf+'(':
		if fullparen(inputexpression[6:]):
			the_exponent = inputexpression[7:len(inputexpression)-1]
			if checkifdvar(the_exponent,dvar,idvar):
				return [True,trigrule(inputexpression,the_exponent)[1],the_exponent,'Apply the chain rule to <div class="katex_div_il">f(g('+dvar+'))</div> with <div class="katex_div_il">f(U)='+slatex(tf)+'(U)</div> and <div class="katex_div_il">g('+dvar+')='+slatex(the_exponent)+'</div>',3]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]

def chainrule(inputexpression,dvar,idvar):
	expo_chain = checkexpo(inputexpression,dvar,idvar)
	log_chain = checklog(inputexpression,dvar,idvar)
	power_chain = checkpower(inputexpression,dvar,idvar)
	trig_chain = []
	for tf in ['sin','cos','tan','cot','sec','csc']:
		trig_chain.append(checktrig(inputexpression,dvar,idvar,tf))
	for itf in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
		trig_chain.append(checkitrig(inputexpression,dvar,idvar,itf))
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

