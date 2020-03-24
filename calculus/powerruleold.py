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
		return False
def powerrule(inputexpression,dvar):
	#print inputexpression, dvar
	if inputexpression == 'sqrt(x)':
		return [True,'1/(2sqrt(x))']
	if len(inputexpression)>len(dvar)+1:
		if inputexpression[:len(dvar)]==dvar:
			if inputexpression[len(dvar)]=='^':
				if inputexpression[len(dvar)+1:].find(dvar,0)==-1:
					#print "heree"
					the_exponent = inputexpression[len(dvar)+1:]
					#if the_exponent.find(dvar,0)==-1:
					try:
						the_exponent = float(the_exponent)
						if int(the_exponent)==float(the_exponent):
							the_exponent=int(the_exponent)
							if the_exponent-1 == 1:
								return [True,str(the_exponent)+'*'+dvar]
							elif the_exponent-1==0:
								return [True,str(the_exponent)]
							else:
								return [True,str(the_exponent)+'*'+dvar+'^'+str(the_exponent-1)]
						else:
							return [True,str(the_exponent)+'*'+dvar+'^'+str(the_exponent-1)]
						#print 'hereee'
					except:
						try:
							if the_exponent[0]=='(':
								if the_exponent[len(the_exponent)-1]==')':
									the_exponent = the_exponent[1:len(the_exponent)-1]
									the_exponent = float(the_exponent)
									if int(the_exponent)==float(the_exponent):
										the_exponent=int(the_exponent)
										if the_exponent-1 == 1:
											return [True,str(the_exponent)+'*'+dvar]
										elif the_exponent-1==0:
											return [True,str(the_exponent)]
										else:
											return [True,str(the_exponent)+'*'+dvar+'^'+str(the_exponent-1)]

									else:
										return [True,str(the_exponent)+'*'+dvar+'^('+str(the_exponent-1)+')']
								else:
									#print the_exponent, 'aa'
									if fullparen(the_exponent):
										return [True,the_exponent+'*'+dvar+'^('+the_exponent[1:len(the_exponent)-1]+'-1)']
									elif the_exponent.find('+',0)+the_exponent.find('-',0)+the_exponent.find('*',0)+the_exponent.find('/',0)+the_exponent.find('(',0)==-5:
										return [True,the_exponent+'*'+dvar+'^('+the_exponent+'-1)']
									else:
										return [False,inputexpression]
							else:
								if fullparen(the_exponent):
									if len(the_exponent)>1:
										return [True,the_exponent+'*'+dvar+'^('+the_exponent[1:len(the_exponent)-1]+'-1)']
									else:
										return [True,the_exponent+'*'+dvar+'^('+the_exponent+'-1)']
								elif the_exponent.find('+',0)+the_exponent.find('-',0)+the_exponent.find('*',0)+the_exponent.find('/',0)+the_exponent.find('(',0)==-5:
									return [True,the_exponent+'*'+dvar+'^('+the_exponent+'-1)']
								else:
									return [False,inputexpression]
						except:
							if fullparen(the_exponent):
								if len(the_exponent)>1:
									return [True,the_exponent+'*'+dvar+'^('+the_exponent[1:len(the_exponent)-1]+'-1)']
								else:
									return [True,the_exponent+'*'+dvar+'^('+the_exponent+'-1)']
							elif the_exponent.find('+',0)+the_exponent.find('-',0)+the_exponent.find('*',0)+the_exponent.find('/',0)+the_exponent.find('(',0)==-5:
								return [True,the_exponent+'*'+dvar+'^('+the_exponent+'-1)']
							else:
								return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression == dvar:
		return [True,'1']
	elif inputexpression.find(dvar,0)<0:
		return [True,'0']
	else:
		return [False,inputexpression]


#print powerrule('sqrt(x)','x')
print powerrule('x^(1/3)','x')


