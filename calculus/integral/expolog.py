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

def logrule(inputexpression,dvar):
	return [False,inputexpression]
	if inputexpression[:4]=='log(':
		if inputexpression[4:4+len(dvar)]==dvar:
			if inputexpression[4+len(dvar):]==')':
				return [True,'('+dvar+')*ln('+dvar+')-'+dvar, 'Apply the logarithm rule.']
			else:
				return [False,inputexpression]
		elif inputexpression[4:2+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if inputexpression[2+len(dvar):]==')':
						return [True,dvar+'*ln('+dvar+')-'+dvar, 'Apply the logarithm rule.']
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[4:6+len(dvar)]=='('+dvar+')':
			if inputexpression[6+len(dvar):]==')':
				return [True,'('+dvar+')*ln('+dvar+')-'+dvar,'Apply the logarithm rule.']
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression[:3]=='ln(':
		if inputexpression[3:3+len(dvar)]==dvar:
			if inputexpression[3+len(dvar):]==')':
				return [True,'('+dvar+')*ln('+dvar+')-'+dvar, 'Apply the logarithm rule.']
			else:
				return [False,inputexpression]
		elif inputexpression[3:1+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if inputexpression[1+len(dvar):]==')':
						return [True,dvar+'*ln('+dvar+')-'+dvar, 'Apply the logarithm rule.']
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[3:5+len(dvar)]=='('+dvar+')':
			if inputexpression[5+len(dvar):]==')':
				return [True,'('+dvar+')*ln('+dvar+')-'+dvar, 'Apply the logarithm rule.']
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]

def exporule(inputexpression,dvar):
	found_one = False
	openpar = 0
	for idx,i in enumerate(inputexpression):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			#print i
			if i == '^':
				first_p = idx
				found_one = True
				break
	#print found_one, inputexpression
	if found_one:
		the_base = inputexpression[:first_p]
		if fullparen(the_base):
			spart = the_base
			for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
				spart=spart.replace(sstr,'')
			if spart.find(dvar)==-1:
				#print the_base
				if inputexpression[:len(the_base)+2]==the_base+'^(':
					if inputexpression[len(the_base)+2:len(the_base)+2+len(dvar)]==dvar:
						if inputexpression[len(the_base)+2+len(dvar):]==')':
							if the_base == 'e':
								return [True,inputexpression,'Apply the exponential rule.']
							else:
								return [True,inputexpression+'/log('+the_base+')', 'Apply the exponential rule to <div class="katex_div_il">a^'+dvar+'</div> with the base <div class="katex_div_il">a='+the_base+'</div>.']
						else:
							return [False,inputexpression]
					elif inputexpression[len(the_base)+2:len(the_base)+len(dvar)]==dvar[len(the_base):len(dvar)-1]:
						if dvar[0]=='(':
							if dvar[len(dvar)-1]==')':
								if inputexpression[len(the_base)+len(dvar):]==')':
									if the_base == 'e':
										return [True,inputexpression,'Apply the exponential rule.']
									else:
										return [True,inputexpression+'/log('+the_base+')', 'Apply the exponential rule to <div class="katex_div_il">a^'+dvar+'</div> with the base <div class="katex_div_il">a='+the_base+'</div>.']
								else:
									return [False,inputexpression]
							else:
								return [False,inputexpression]
						else:
							return [False,inputexpression]
					elif inputexpression[len(the_base)+2:len(the_base)+4+len(dvar)]=='('+dvar+')':
						if inputexpression[len(the_base)+4+len(dvar):]==')':
							if the_base == 'e':
								return [True,inputexpression,'Apply the exponential rule.']
							else:
								return [True,inputexpression+'/log('+the_base+')', 'Apply the exponential rule to <div class="katex_div_il">a^'+dvar+'</div> with the base <div class="katex_div_il">a='+the_base+'</div>.']
						else:
							return [False,inputexpression]
					else:
						return [False,inputexpression]
				elif inputexpression[:len(the_base)+1]==the_base+'^':
					if inputexpression[len(the_base)+1:len(the_base)+1+len(dvar)]==dvar:
						if len(inputexpression)==len(dvar)+len(the_base)+1:
							if the_base == 'e':
								return [True,inputexpression,'Apply the exponential rule.']
							else:
								return [True,inputexpression+'/log('+the_base+')', 'Apply the exponential rule to <div class="katex_div_il">a^'+dvar+'</div> with the base <div class="katex_div_il">a='+the_base+'</div>.']
						else:
							return [False,inputexpression]
					elif inputexpression[len(the_base)+1:len(the_base)-1+len(dvar)]==dvar[len(the_base):len(dvar)-1]:
						if dvar[0]=='(':
							if dvar[len(dvar)-1]==')':
								if len(inputexpression)==len(dvar):
									if the_base == 'e':
										return [True,inputexpression,'Apply the exponential rule.']
									else:
										return [True,inputexpression+'/log('+the_base+')', 'Apply the exponential rule to <div class="katex_div_il">a^'+dvar+'</div> with the base <div class="katex_div_il">a='+the_base+'</div>.']
								else:
									return [False,inputexpression]
							else:
								return [False,inputexpression]
						else:
							return [False,inputexpression]
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]

def expologrule(inputexpression,dvar):
	log_it = logrule(inputexpression,dvar)
	if log_it[0]:
		return log_it
	else:
		exp_it = exporule(inputexpression,dvar)
		if exp_it[0]:
			return exp_it
		else:
			return [False,inputexpression]
