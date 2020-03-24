#from powerrulew import powerrulew
#from trigrulew import trigrulew
#from expologw import exporulew
import sympy
from sympy import diff
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
	
	du = diff(sympy.sympify(u),sympy.sympify(dvar))
	try:
		float(du)
		inputexpression=inputexpression.replace(u,'(u)')
		inputexpression='('+inputexpression+')/('+str(du)+')'
	except:
		inputexpression=inputexpression.replace(u,'(u)')
		inputexpression='('+inputexpression+')/('+str(du)+')'
	return str(sympy.simplify(sympy.sympify(cleanpar(inputexpression,dvar))))
def usub(inputexpression,dvar):
	inputexpression = cleanpar(inputexpression,dvar)
	possibleu = []
	for i in range(0,len(inputexpression)):
		if inputexpression[i]=='(':
			possibleu.append(getfullparen(inputexpression[i:]))
			if i>1:
				if inputexpression[i-1:i] in ['^']:
					possibleu.append(inputexpression[i-2:i]+getfullparen(inputexpression[i:]))
			if i>1:
				if inputexpression[i-2:i] in ['ln']:
					possibleu.append(inputexpression[i-2:i]+getfullparen(inputexpression[i:]))
			if i>2:
				if inputexpression[i-3:i] in ['log','sin','cos','tan','cot','sec','csc']:
					possibleu.append(inputexpression[i-3:i]+getfullparen(inputexpression[i:]))
			if i>3:
				if inputexpression[i-4:i] in ['sqrt']:
					possibleu.append(inputexpression[i-4:i]+getfullparen(inputexpression[i:]))
			if i>5:
				if inputexpression[i-6:i] in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
					possibleu.append(inputexpression[i-6:i]+getfullparen(inputexpression[i:]))
	#print possibleu
	for u in possibleu:
		usubbed = usubstitution(inputexpression,dvar,u)
		#print usubbed, u
		if usubbed.find(dvar)==-1:
			if u != dvar and u != '('+dvar+')' and '('+u+')'!=dvar and usubbed != 'u' and usubbed != '('+'u'+')':
				return [True,usubbed,u]
	return [False,inputexpression]
#print usub('sin(10*x)','x')
