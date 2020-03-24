from clean import cleanpar
from clean import post_clean
import sympy
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
def powerrulew(inputexpression,dvar,idvar,wrongness):
	#print "pr", inputexpression
	#print inputexpression, dvar
	if inputexpression == 'sqrt('+dvar+')':
		return [True,[['1/(2sqrt('+dvar+'))','Correct'],['1/(sqrt('+dvar+'))','Do not forget to multiply by 1/2.']],'The derivative of the square root of '+dvar+' is 1 divided by twice the square root of '+dvar+'.']
	if len(inputexpression)>len(dvar)+1:
		if inputexpression[:len(dvar)]==dvar:
			if inputexpression[len(dvar)]=='^':
				#print 'hhe'
				if inputexpression[len(dvar)+1:].find(dvar,0)==-1:
					#print "heree"
					the_exponent = inputexpression[len(dvar)+1:]
					#if the_exponent.find(dvar,0)==-1:
					return [True,[[cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Correct'],[cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'+1)',dvar),'Subtract one in the exponent, not add one. The derivative of <div class="katex_div_il">'+slatex(inputexpression)+'</div> is <div class="katex_div_il">'+slatex(cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar))+'</div> not <div class="katex_div_il">'+slatex(cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'+1)',dvar))+'</div>.'],[cleanpar('1/'+str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Multiply by the exponent, not divide. The derivative of <div class="katex_div_il">'+slatex(inputexpression)+'</div> is <div class="katex_div_il">'+slatex(cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar))+'</div> not <div class="katex_div_il">'+slatex(cleanpar('1/'+str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar))+'</div>.']],'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>']
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression == dvar:
		return [True,[['1','Correct'],['0','The derivative of '+dvar+' is 1 not 0']], 'The derivative of '+dvar+' is 1']
	elif inputexpression == idvar:
		return [True,[['holdfordydx','Correct'],['1','The derivative of y is dy/dx'],['0','The derivative of y is dy/dx']],'The derivative of '+idvar+' is dy/dx since y is a function of x']
	elif inputexpression.find(dvar,0)<0:
		return [True,[['0','Correct'],[inputexpression,'The derivative of a constant is 0']], 'The derivative of a constant is 0']
	else:
		return [False,inputexpression]


#print powerrule('sqrt(x)','x')
#print powerrule('x^(1/3)','x')


