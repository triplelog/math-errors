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
		else:
			return False

def othertricks(inputexpression,dvar):
	power_spots = []
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		#print power_spots, inputexpression
		openpar = 0
		isbreak = 0
		cancel_it = 0
		really_cancel = 0
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			if openpar == 0:
				cancel_it = 1
				stopper = idx
				#print stopper
				index1 = inputexpression[:stopper+1].find(dvar,0)
				index2 = inputexpression[stopper+2:].find(dvar,0)
				if index1 == -1:
					really_cancel = 1
					#print "a"
				if index2 ==-1:
					really_cancel = 1
				if not fullparen(inputexpression[stopper+2:]):
					really_cancel = 1
				if not fullparen(inputexpression[:stopper+1]):
					really_cancel = 1
				#print really_cancel, cancel_it, power_spots, inputexpression[:stopper+1], inputexpression[stopper+2:]
				break
		if really_cancel !=1:
			if cancel_it == 1:
				if stopper in power_spots:
					#print "win"
					if inputexpression[:stopper+1][0]=='(':
						if inputexpression[:stopper+1][len(inputexpression[:stopper+1])-1]==')':
							return [True,'e^('+inputexpression[stopper+2:]+'*log'+inputexpression[:stopper+1]+')']
						else:
							return [True,'e^('+inputexpression[stopper+2:]+'*log('+inputexpression[:stopper+1]+'))']
					else:
						return [True,'e^('+inputexpression[stopper+2:]+'*log('+inputexpression[:stopper+1]+'))']

				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]


#print othertricks('(x+1)^(x+1)','x')