import sympy
from clean import post_clean
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

def invtrigrule(inputexpression,dvar,tf,dtf,wdtf):
	if inputexpression == tf:
		return [True,[[dtf,'Correct'],[wdtf,'Wrong Trig Derivative-The derivative of <div class="katex_div_il">'+slatex(tf)+'</div> is <div class="katex_div_il">'+slatex(dtf)+'</div> not <div class="katex_div_il">'+slatex(wdtf)+'</div>.']],'Apply the rule for the derivative of <div class="katex_div_il">'+slatex(tf)+'</div>.']
	else:
		return [False,inputexpression]

def trigrulew(inputexpression,dvar,wrongness):
	for tf,dtf,wdtf in [['sin('+dvar+')','cos('+dvar+')','-cos('+dvar+')'],['cos('+dvar+')','-sin('+dvar+')','sin('+dvar+')'],['tan('+dvar+')','sec('+dvar+')^2','sec('+dvar+')*tan('+dvar+')'],['csc('+dvar+')','-csc('+dvar+')'+'cot('+dvar+')','csc('+dvar+')'+'cot('+dvar+')'],['sec('+dvar+')','sec('+dvar+')'+'tan('+dvar+')','-sec('+dvar+')'+'tan('+dvar+')'],['cot('+dvar+')','-csc('+dvar+')^2','csc('+dvar+')'+'cot('+dvar+')']]:
		the_d = invtrigrule(inputexpression,dvar,tf,dtf,wdtf)
		#print tf, dvar, inputexpression, the_d
		if the_d[0]:
			return the_d
	for tf,dtf,wdtf in [['arcsin('+dvar+')','1/(sqrt(1-('+dvar+')^2))','arccos('+dvar+')'],['arccos('+dvar+')','-1/(sqrt(1-('+dvar+')^2))','-arcsin('+dvar+')'],['arctan('+dvar+')','1/(1+('+dvar+')^2)','arcsec('+dvar+')^2'],['arccot('+dvar+')','-1/(1+('+dvar+')^2)','-arccsc('+dvar+')^2'],['arcsec('+dvar+')','1/(abs(x)*sqrt(('+dvar+')^2-1))','arcsec('+dvar+')'+'arctan('+dvar+')'],['arccsc('+dvar+')','-1/(abs(x)*sqrt(('+dvar+')^2-1))','-arccsc('+dvar+')'+'arccot('+dvar+')']]:
		the_d = invtrigrule(inputexpression,dvar,tf,dtf,wdtf)
		if the_d[0]:
			return the_d
	return [False,inputexpression]
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]