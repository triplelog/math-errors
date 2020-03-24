import sympy
from clean import post_clean
def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))

def productrulew(inputexpression,allparts,dvar,wrongness):
	#print inputexpression
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
			allparts.append(leftpart)
			allparts.append(rightpart)
			allparts.append('Apply the product rule to <div class="katex_div_il">'+slatex(leftpart)+'</div> times <div class="katex_div_il">'+slatex(rightpart)+'</div>.')
		else:
			allparts.append(inputexpression)
	else:
		allparts.append(inputexpression)
	return allparts

#print productrule('3abc*x^2*abc/(1+2)/x*4(1+x)(x+1-3)*(x)/(1+1)*x',[],'x')