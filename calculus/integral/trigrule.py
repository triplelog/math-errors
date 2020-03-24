import sympy
from clean import post_clean, cleanpar
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

def invtrigrule(inputexpression,dvar,tf,dtf):
	if inputexpression == tf:
		return [True,dtf,'Apply the rule for the integral of <div class="katex_div_il">'+slatex(tf)+'</div>.']
	else:
		return [False,inputexpression]

def trigrule(inputexpression,dvar):
	for tf,dtf in [['sin('+dvar+')','-cos('+dvar+')'],['cos('+dvar+')','sin('+dvar+')'],['tan('+dvar+')','-ln(cos('+dvar+'))'],['csc('+dvar+')','ln(csc('+dvar+')-'+'cot('+dvar+'))'],['sec('+dvar+')','ln(sec('+dvar+')+'+'tan('+dvar+'))'],['cot('+dvar+')','ln(sin('+dvar+'))']]:
		the_d = invtrigrule(inputexpression,dvar,tf,dtf)
		if the_d[0]:
			return the_d
	for dtf,tf in [['sin('+dvar+')','cos('+dvar+')'],['cos('+dvar+')','-sin('+dvar+')'],['tan('+dvar+')','sec('+dvar+')^2'],['csc('+dvar+')','-csc('+dvar+')'+'cot('+dvar+')'],['sec('+dvar+')','sec('+dvar+')'+'tan('+dvar+')'],['cot('+dvar+')','-csc('+dvar+')^2']]:
		the_d = invtrigrule(cleanpar(inputexpression,dvar),dvar,cleanpar(tf,dvar),dtf)
		if the_d[0]:
			return the_d
	for dtf,tf in [['arcsin('+dvar+')','1/(sqrt(1-('+dvar+')^2))'],['arccos('+dvar+')','-1/(sqrt(1-('+dvar+')^2))'],['arctan('+dvar+')','1/(1+('+dvar+')^2)'],['arccot('+dvar+')','-1/(1+('+dvar+')^2)'],['arcsec('+dvar+')','1/(abs(x)*sqrt(('+dvar+')^2-1))'],['arccsc('+dvar+')','-1/(abs(x)*sqrt(('+dvar+')^2-1))']]:
		the_d = invtrigrule(cleanpar(inputexpression,dvar),dvar,cleanpar(tf,dvar),dtf)
		if the_d[0]:
			return the_d
	return [False,inputexpression]
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]