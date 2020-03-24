from productrule import productrule
from clean import cleanpar
import sympy
from clean import post_clean
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

def quorule(inputexpression,dvar):
	h = productrule(inputexpression,[],dvar)
	if len(h)==1:
		#do quotient
		openpar = 0
		hasone = False
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			if openpar == 0:
				if i == '/':
					firstspot = idx
					hasone = True
					break
		if hasone:
			rest_of_denom = inputexpression[firstspot+1:].replace('/','*')
			return [True,cleanpar(inputexpression[0:firstspot],dvar),cleanpar(rest_of_denom,dvar),'Apply the quotient rule to <div class="katex_div_il">'+slatex(cleanpar(inputexpression[0:firstspot],dvar))+'</div> divided by <div class="katex_div_il">'+slatex(cleanpar(rest_of_denom,dvar))+'</div>']
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]
	

#print quorule('(x+2)^2/x/(x+1)','x')