import sympy
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
def fullparen_nomore(input_string):
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
		return False
def cleanp(inputexpression, dvar):
	for fnsqs in ['log','sin','cos','tan','cot','sec','csc']:
		fnsq = inputexpression.find(fnsqs+'^') 
		if fnsq >-1:
			for idx, i in enumerate(inputexpression[fnsq+4:]):
				if fullparen(inputexpression[fnsq+4:fnsq+4+idx]):
					endfnexp = idx
			the_exp = inputexpression[fnsq+4:fnsq+4+endfnexp]
			for idx, i in enumerate(inputexpression[fnsq+4+len(the_exp):]):
				if fullparen(inputexpression[fnsq+4+len(the_exp):fnsq+4+len(the_exp)+idx]):
					endfnsq = idx
			inputexpression = inputexpression.replace(fnsqs+'^'+the_exp,fnsqs)
			inputexpression=inputexpression[:fnsq+4+len(the_exp)+endfnsq]+'^'+the_exp+inputexpression[fnsq+4+len(the_exp)+endfnsq:]

	for fnsqs in ['arcsin','arccos','arctan','arccot','arcsec','arccsc']:
		fnsq = inputexpression.find(fnsqs+'^') 
		if fnsq >-1:
			for idx, i in enumerate(inputexpression[fnsq+8:]):
				if fullparen(inputexpression[fnsq+8:fnsq+8+idx]):
					endfnexp = idx
			the_exp = inputexpression[fnsq+8:fnsq+8+endfnexp]
			for idx, i in enumerate(inputexpression[fnsq+8+len(the_exp):]):
				if fullparen(inputexpression[fnsq+8+len(the_exp):fnsq+8+len(the_exp)+idx]):
					endfnsq = idx
			inputexpression = inputexpression.replace(fnsqs+'^'+the_exp,fnsqs)
			inputexpression=inputexpression[:fnsq+8+len(the_exp)+endfnsq]+'^'+the_exp+inputexpression[fnsq+8+len(the_exp)+endfnsq:]
	for fnsqs in ['ln']:
		fnsq = inputexpression.find(fnsqs+'^') 
		if fnsq >-1:
			for idx, i in enumerate(inputexpression[fnsq+3:]):
				if fullparen(inputexpression[fnsq+3:fnsq+3+idx]):
					endfnexp = idx
			the_exp = inputexpression[fnsq+3:fnsq+3+endfnexp]
			for idx, i in enumerate(inputexpression[fnsq+3+len(the_exp):]):
				if fullparen(inputexpression[fnsq+3+len(the_exp):fnsq+3+len(the_exp)+idx]):
					endfnsq = idx
			inputexpression = inputexpression.replace(fnsqs+'^'+the_exp,fnsqs)
			inputexpression=inputexpression[:fnsq+3+len(the_exp)+endfnsq]+'^'+the_exp+inputexpression[fnsq+3+len(the_exp)+endfnsq:]
	if inputexpression[0]=='/':
		inputexpression='1'+inputexpression
	inputexpression = inputexpression.replace(' ','')
	if inputexpression[0]=='(':
		if inputexpression[len(inputexpression)-1]==')':
			justenough = 0
			openpar = 0
			for i in inputexpression[:len(inputexpression)-2]:
				if i =='(':
					openpar = openpar+1
				elif i == ')':
					openpar = openpar-1
				if openpar < 0:
					donot = 0
					#print "too many closing parentheses"
				elif openpar == 0:
					justenough = 1
			if justenough !=1:
				inputexpression = inputexpression[1:len(inputexpression)-1]

	openpar = 0
	isbreak = 0
	cancelnext = 0
	allparts = []
	#add exceptions for trig functions, etc
	for idx,i in enumerate(inputexpression):
		if i == '(':
			noweird = 0
			for tstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','ln']:
				if inputexpression[:idx].count(tstr) > inputexpression[:idx].count(tstr+'('):
					noweird = 1
					break
			if noweird == 0:
				if idx > 0:
					if inputexpression[idx-1]!='*':
						if inputexpression[idx-1]!='/':
							if inputexpression[idx-1]!='^':
								if inputexpression[idx-1]!='+':
									if inputexpression[idx-1]!='-':
										if inputexpression[idx-1]!='(':
											if inputexpression[idx-1]!='|':
												if inputexpression[idx-3:idx]!='log':
													if inputexpression[idx-3:idx]!='sin':
														if inputexpression[idx-3:idx]!='cos':
															if inputexpression[idx-3:idx]!='tan':
																if inputexpression[idx-3:idx]!='sec':
																	if inputexpression[idx-3:idx]!='csc':
																		if inputexpression[idx-3:idx]!='cot':
																			if inputexpression[idx-4:idx]!='sqrt':
																				if inputexpression[idx-2:idx]!='ln':
																					inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
																					##print inputexpression
																					inputexpression = cleanpar(inputexpression,dvar)
																					cancelnext = 1
																					break
	if cancelnext != 1:
		norunidx = []
		for idx,i in enumerate(inputexpression):
			if idx not in norunidx:
				if inputexpression[idx:idx+11] in ['holdfordydx']:
					for ii in range(1,11):
						norunidx.append(idx+ii)
					if idx > 0:
						if inputexpression[idx-1]==dvar:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1]==')':
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1] in ['0','1','2','3','4','5','6','7','8','9']:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
				elif inputexpression[idx:idx+2] in ['ln']:
					norunidx.append(idx+1)
					if idx > 0:
						if inputexpression[idx-1]==dvar:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1]==')':
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1] in ['0','1','2','3','4','5','6','7','8','9']:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
				elif inputexpression[idx:idx+3] in ['sin','cos','log','tan','cot','sec','csc','sqr','arc']:
					if inputexpression[idx:idx+3] in ['sin','cos','log','tan','cot','sec','csc']:
						norunidx.append(idx+1)
						norunidx.append(idx+2)
					elif inputexpression[idx:idx+3] in ['sqrt']:
						norunidx.append(idx+1)
						norunidx.append(idx+2)
						norunidx.append(idx+3)
					elif inputexpression[idx:idx+3] in ['arc']:
						norunidx.append(idx+1)
						norunidx.append(idx+2)
						norunidx.append(idx+3)
						norunidx.append(idx+4)
						norunidx.append(idx+5)
					if idx > 0:
						if inputexpression[idx-1]==dvar:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1]==')':
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1] in ['0','1','2','3','4','5','6','7','8','9']:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
				elif inputexpression[idx:idx+2] in ['e^']:
					norunidx.append(idx+1)
					norunidx.append(idx+2)
					if idx > 0:
						if inputexpression[idx-1]==dvar:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1]==')':
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
						elif inputexpression[idx-1] in ['0','1','2','3','4','5','6','7','8','9']:
							inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
							inputexpression = cleanpar(inputexpression,dvar)
							cancelnext = 1
							break
				elif i in [dvar]:
					if idx > 0:
						if inputexpression[idx-1]!='*':
							if inputexpression[idx-1]!='^':
								if inputexpression[idx-1]!='(':
									if inputexpression[idx-1]!='/':
										if inputexpression[idx-1]!='+':
											if inputexpression[idx-1]!='-':
												if inputexpression[idx-1]!='|':
													if inputexpression[idx-3:idx] in ['sin','cos','log','tan','cot','sec','csc','cot','qrt']:
														inputexpression=inputexpression[0:idx]+'('+dvar+')'+inputexpression[idx+1:]
														##print inputexpression
														inputexpression = cleanpar(inputexpression,dvar)
														cancelnext = 1
														break
													elif inputexpression[idx-2:idx] in ['ln']:
														inputexpression=inputexpression[0:idx]+'('+dvar+')'+inputexpression[idx+1:]
														##print inputexpression
														inputexpression = cleanpar(inputexpression,dvar)
														cancelnext = 1
														break
													else:
														inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
														##print inputexpression
														inputexpression = cleanpar(inputexpression,dvar)
														cancelnext = 1
														break
													
	##print 'xxx', inputexpression, str(sympy.sympify(inputexpression))
	return inputexpression
#print sympy.sympify('sec(x)^2')
##print cleanpar('1/3x^2*abc/(1+2)/ x*4(1+x)(x+1-3)*(x)/(1+1)x','x')
def cleanpar(f,dvar):
	#print f
	#print f, 'fffff'
	f=cleanp(f,dvar)
	#print f
	#print f, 'ggggg'
	try:
		f=str(sympy.sympify(f))
	except:
		f=f
	f=f.replace("**","^")
	#f=f.replace("1/"+dvar,"*"+dvar+"^(-1)")
	f=cleanp(f,dvar)
	if f=='1/'+dvar:
		f=dvar+'^(-1)'
	#print f, 'gggg'
	return f
def post_clean(f):
	f=f.replace('+-','-')
	try:
		f = str(eval(f))
	except:
		if fullparen_nomore(f):
			if len(f)>1:
				f = f[1:len(f)-1]
				try:
					f = str(eval(f))
				except:
					pass
	return f
#print cleanpar('cot(t)','t')


