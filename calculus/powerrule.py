from clean import cleanpar
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
def powerrule(inputexpression,dvar,idvar):
	#print "pr", inputexpression
	#print inputexpression, dvar
	if inputexpression == 'sqrt('+dvar+')':
		return [True,'1/(2sqrt('+dvar+'))','The derivative of <div class="katex_div_il">\sqrt{'+dvar+'}</div> is <div class="katex_div_il">\\frac{1}{2\sqrt{'+dvar+'}}',0]
	if len(inputexpression)>len(dvar)+1:
		if inputexpression[:len(dvar)]==dvar:
			if inputexpression[len(dvar)]=='^':
				#print 'hhe'
				if inputexpression[len(dvar)+1:].find(dvar,0)==-1:
					
					#print "heree"
					the_exponent = inputexpression[len(dvar)+1:]
					#if the_exponent.find(dvar,0)==-1:
					try:
						if int(the_exponent)==2:
							return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',3]
						elif float(the_exponent)-int(the_exponent)<.00000001:
							if int(the_exponent)<0:
								return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',4]
							else:
								return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',5]
						else:
							if float(the_exponent)<0:
								return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',6]
							else:
								return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',7]					
					except:
						return [True,cleanpar(str(the_exponent)+'*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>',8]					
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression == dvar:
		return [True,'1', 'The derivative of '+dvar+' is 1',1]
	elif inputexpression == idvar:
		return [True,'holdfordydx','The derivative of '+idvar+' is dy/dx since y is a function of x',9]
	elif inputexpression.find(dvar,0)<0:
		return [True,'0', 'The derivative of a constant is 0',2]
	else:
		return [False,inputexpression]


#print powerrule('sqrt(x)','x')
#print powerrule('x^(1/3)','x')


