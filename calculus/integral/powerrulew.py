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
def powerrulew(inputexpression,dvar):
	#print "pr", inputexpression
	#print inputexpression, dvar
	if inputexpression == 'sqrt('+dvar+')':
		return [True,[['2/3*('+dvar+')^(3/2)','Correct',.9],['1/2sqrt('+dvar+')','Take the integral not the derivative.',.1]],'Take the integral of the square root function.']
	if len(inputexpression)>len(dvar)+1:
		if inputexpression[:len(dvar)]==dvar:
			if inputexpression[len(dvar)]=='^':
				#print 'hhe'
				if inputexpression[len(dvar)+1:].find(dvar,0)==-1:
					#print "heree"
					the_exponent = inputexpression[len(dvar)+1:]
					#print the_exponent
					try:
						if str(the_exponent)=='(-1)':
							#print 'hi'
							#print cleanpar('ln(|'+dvar+'|)',dvar)
							#print 'hop'
							return [True,[[cleanpar('ln|'+dvar+'|',dvar),'Correct',.9],['1','Integrating with -1 as the exponent is special. The integral is the natural logarithm.',.1]],'The integral of <div class="katex_div_il">'+'1/('+dvar+')'+'</div> is the natural log of the absolute value of <div class="katex_div_il">'+dvar+'</div>']
						else:
							#if the_exponent.find(dvar,0)==-1:
							return [True,[[cleanpar('1/('+str(the_exponent)+'+1)*'+dvar+'^('+str(the_exponent)+'+1)',dvar),'Correct',.9],[cleanpar('1/('+str(the_exponent)+'-1)*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Add one to the exponent not subtract one.',.05],[cleanpar('('+str(the_exponent)+')*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Take the integral not the derivative.',.05]],'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>']
					except:
						return [True,[[cleanpar('1/('+str(the_exponent)+'+1)*'+dvar+'^('+str(the_exponent)+'+1)',dvar),'Correct',.9],[cleanpar('1/('+str(the_exponent)+'-1)*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Add one to the exponent not subtract one.',.05],[cleanpar('('+str(the_exponent)+')*'+dvar+'^('+str(the_exponent)+'-1)',dvar),'Take the integral not the derivative.',.05]],'Apply the power rule to <div class="katex_div_il">'+dvar+'^a</div> with <div class="katex_div_il">a='+str(the_exponent)+'</div>']						
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression == dvar:
		return [True,[['('+dvar+')^2/2','Correct',.9],['1','Take the integral not the derivative.',.05],['2('+dvar+')^2','Divide by the new exponent instead of multiplying.',.05]], 'The integral of '+dvar+' is '+'('+dvar+')^2/2']
	elif inputexpression.find(dvar,0)<0:
		return [True,[['('+inputexpression+')('+dvar+')','Correct',.9],['0','Take the integral not the derivative.',.1]], 'The integral of a constant is . If this appears there is an error earlier.']
	else:
		return [False,inputexpression]

#print powerrule('sqrt(x)','x')
#print powerrule('x^(1/3)','x')