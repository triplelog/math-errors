import sympy
from clean import post_clean
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

def invtrigrule(inputexpression,dvar,tf,dtf,idx):
	if inputexpression == tf:
		return [True,dtf,'Apply the rule for the derivative of <div class="katex_div_il">'+slatex(tf)+'</div>.',idx]
	else:
		return [False,inputexpression]

def trigrule(inputexpression,dvar):
	idx = 0
	for tf,dtf in [['sin('+dvar+')','cos('+dvar+')'],['cos('+dvar+')','-sin('+dvar+')'],['tan('+dvar+')','sec('+dvar+')^2'],['cot('+dvar+')','-csc('+dvar+')^2'],['sec('+dvar+')','sec('+dvar+')'+'tan('+dvar+')'],['csc('+dvar+')','-csc('+dvar+')'+'cot('+dvar+')']]:
		the_d = invtrigrule(inputexpression,dvar,tf,dtf,idx)
		if the_d[0]:
			return the_d
		else:
			idx=idx+1
	for tf,dtf in [['arcsin('+dvar+')','1/(sqrt(1-('+dvar+')^2))'],['arccos('+dvar+')','-1/(sqrt(1-('+dvar+')^2))'],['arctan('+dvar+')','1/(1+('+dvar+')^2)'],['arccot('+dvar+')','-1/(1+('+dvar+')^2)'],['arcsec('+dvar+')','1/(abs(x)*sqrt(('+dvar+')^2-1))'],['arccsc('+dvar+')','-1/(abs(x)*sqrt(('+dvar+')^2-1))']]:
		the_d = invtrigrule(inputexpression,dvar,tf,dtf,idx)
		if the_d[0]:
			return the_d
		else:
			idx=idx+1
	return [False,inputexpression]
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]