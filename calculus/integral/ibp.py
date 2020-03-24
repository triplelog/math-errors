#from powerrulew import powerrulew
#from trigrulew import trigrulew
#from expologw import exporulew
import sympy
from sympy import diff, integrate, Symbol
from clean import post_clean
from clean import cleanpar
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
def getfullparen(input_string):
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
	return input_string[:isbreak+1]
def usubstitution(inputexpression,dvar,u):
	oexp = inputexpression
	dv = sympy.sympify('('+inputexpression+')/('+str(u)+')')
	#print dv
	v=integrate(dv,sympy.sympify(dvar))
	#print v
	du = diff(sympy.sympify(u),sympy.sympify(dvar))
	#inputexpression='('+str(u)+')*('+str(v)+')-('+str(integrate(sympy.sympify('('+str(v)+')*('+str(du)+')'),sympy.sympify(dvar)))+')'
	#if diff(sympy.sympify(inputexpression),dvar)==sympy.sympify(oexp):
	#	print "success", u,du,v,dv
	return [u,v,du,dv,oexp,dvar]
def breakproduct(inputexpression,dvar):
	openpar = 0
	isbreak = 0
	cancelnext = 0
	for idx,i in enumerate(inputexpression):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		elif i == '+':
			if openpar == 0:
				breakhere = idx
				isbreak = 1
				isneg = 0
				break
		elif i == '-':
			if idx > 0:
				if openpar == 0:
					breakhere = idx
					isbreak = 1
					isneg = 1
					break
	if isbreak != 1:
		firstdvar = -1
		lastdvar = len(inputexpression)+1
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			elif i == '*':
				if inputexpression[idx+1] != '*':
					if inputexpression[idx-1] != '*':
						if openpar == 0:
							#print inputexpression, dvar
							if idx > firstdvar:
								if idx < lastdvar:
									breakhere = idx
									isbreak = 1
									isneg = 0
									break

		if isbreak == 1:
			leftpart = inputexpression[0:breakhere]
			rightpart = inputexpression[breakhere+1:]
			return leftpart
		else:
			return inputexpression
	else:
		return inputexpression
def do_ibp(inputexpression,dvar,u,dv):
	x = Symbol('x')
	du = diff(sympy.sympify(u))
	try:
		v = integrate(sympy.sympify(dv),x)
		return [True,str(u),str(v),str(du),str(dv)]
	except:
		return [False]
	
def ibp(inputexpression,dvar):
	possibleu = []
	inputexpression = cleanpar(inputexpression,dvar)
	oexp = inputexpression
	numruns = 0
	while sympy.sympify(breakproduct(oexp,dvar))!=sympy.sympify(oexp):
		if cleanpar(breakproduct(oexp,dvar),dvar) not in possibleu:
			possibleu.append(cleanpar(breakproduct(oexp,dvar),dvar))
		oexp=str(sympy.sympify('('+str(oexp)+')/('+str(breakproduct(oexp,dvar))+')'))
		if cleanpar(oexp,dvar) not in possibleu:
			possibleu.append(cleanpar(oexp,dvar))
		if numruns > 10:
			break
		else:
			numruns=numruns+1
	for i in range(0,len(inputexpression)):
		if inputexpression[i]=='(':
			if cleanpar(getfullparen(inputexpression[i:]),dvar) not in possibleu:
				possibleu.append(cleanpar(getfullparen(inputexpression[i:]),dvar))
			if i>2:
				if inputexpression[i-3:i] in ['log','sin','cos','tan','cot','sec','csc']:
					if cleanpar(inputexpression[i-3:i]+getfullparen(inputexpression[i:]),dvar) not in possibleu:
						possibleu.append(cleanpar(inputexpression[i-3:i]+getfullparen(inputexpression[i:]),dvar))
			if i>3:
				if inputexpression[i-4:i] in ['sqrt']:
					if cleanpar(inputexpression[i-4:i]+getfullparen(inputexpression[i:]),dvar) not in possibleu:
						possibleu.append(cleanpar(inputexpression[i-4:i]+getfullparen(inputexpression[i:]),dvar))
	#print possibleu
	possibleset = []
	#print possibleu
	for u in possibleu:
		#print inputexpression, u
		dv = sympy.sympify('('+inputexpression+')/('+u+')')
		#print dv
		ibped = do_ibp(inputexpression,dvar,u,dv)
		if ibped[0]:
			possibleset.append(ibped)


	if len(possibleset) >0:
		return [True, possibleset]
	else:
		return [False, inputexpression]
#print ibp('ln(x)','x')
