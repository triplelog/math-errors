import simplify

def fullparen(inputexp):
	numparen = 0;
	for i in range(0,len(inputexp)):
	   	if inputexp[i]=='(':
	   		numparen +=1
	   	elif inputexp[i]==')':
	   		numparen -=1

	return numparen

def BreakUp(inputexp, ChkOperation):
	for i in range(1,len(inputexp)):
		if inputexp[i]==ChkOperation:
			dest = inputexp[0:i];
			if fullparen(dest)==0:
				ToReturn = {'operation': ChkOperation, 'location': i}
				return ToReturn
	FailedReturn = {'operation': 'f', 'location': -1}
	return FailedReturn



def ChkOrigin(origin0, origin1):
	if origin0['location']==-1:
		if origin1['location']==-1:
			origin = origin1
		else:
			origin = origin1
	else:
		if origin1['location']==-1:
			origin = origin0
		else:
			if origin1['location'] < origin0['location']:
				origin = origin1
			else:
				origin = origin0
	return origin


def GetLR(source):
	breakeq = -1
	for i in range(0,len(source)):
		if source[i]=='=':
			breakeq = i
	equation = {'haseq': 0,'LHS':'','RHS':''}
	if breakeq!=-1:
		equation['LHS']=source[0:breakeq]
		equation['RHS']=source[breakeq+1:]
		equation['haseq']=1
	else:
		equation['LHS']=source
		equation['RHS']=''
		equation['haseq']=0
	return equation


def DivideUp(source0, StartPoint):

	stl = len(source0)
	source=source0[StartPoint:]

	origin0 = BreakUp(source,'+')
	origin1 = BreakUp(source,'-')
	origin = ChkOrigin(origin0,origin1)
	if origin['location'] ==-1:
		origin0 = BreakUp(source,'*')
		origin1 = BreakUp(source,'/')
		origin = ChkOrigin(origin0,origin1)

	if origin['location'] ==-1:
		origin = BreakUp(source,'^')
	return origin;

def MoveLtoR(equation, originL, variable, StartPoint, ChkOperation, InvOperation):
	if originL['operation']==ChkOperation or originL['operation']==InvOperation:
		FirstTerm = equation['LHS'][StartPoint:StartPoint+originL['location']]
		OtherTerm = equation['LHS'][StartPoint+originL['location']+1:len(equation['LHS'])]
		BreakVar = -1
		slft = len(FirstTerm)
		for i in range(0,slft):
			if FirstTerm[i]==variable:
				BreakVar = i
		StrOper = InvOperation
		COper = ChkOperation
		if BreakVar==-1:
			if StartPoint > 0:
				if equation['LHS'][StartPoint-1:StartPoint]==StrOper:
					equation['RHS']="("+equation['RHS']+")"+COper+"("+FirstTerm+")"
					print COper, FirstTerm, 'from both sides'
				
				else:
					if ChkOperation=='^':
						if OtherTerm.find(variable)!=-1:
							equation['RHS']="ln("+equation['RHS']+")"
							equation['LHS'] = "("+OtherTerm+")*ln("+equation['LHS'][0:StartPoint-1]+"^"+FirstTerm+")"
							print 'Take the natural logarithm of both sides'
						
					
					else:
						equation['RHS']="("+equation['RHS']+")"+StrOper+"("+FirstTerm+")"
						print StrOper, FirstTerm, 'from both sides'	
					
				
				if ChkOperation !='^':
					if originL['operation']==ChkOperation:
						equation['LHS'] = equation['LHS'][0:StartPoint-1]+COper+OtherTerm
					
					else:
						equation['LHS'] = equation['LHS'][0:StartPoint-1]+StrOper+OtherTerm	
					
				
			
			else:
				if equation['LHS'][0:1]==StrOper:
					equation['RHS']="("+equation['RHS']+")"+COper+"("+FirstTerm[1:len(FirstTerm)]+")"
					print COper, FirstTerm, 'from both sides'
				
				else:
					if ChkOperation=='^':
						if OtherTerm.find(variable)!=-1:
							equation['RHS']="ln("+equation['RHS']+")"
							equation['LHS'] = "("+OtherTerm+")*ln("+FirstTerm+")"
							print 'Take the natural logarithm of both sides'
						
					
					else:
						equation['RHS']="("+equation['RHS']+")"+StrOper+"("+FirstTerm+")"
						print StrOper, FirstTerm, 'from both sides'
					
				
				if originL['operation']==ChkOperation:
					if ChkOperation !='^':
						equation['LHS'] = OtherTerm
					
				
				else:
					if InvOperation=='-':
						equation['LHS'] = StrOper+OtherTerm	
					
					elif InvOperation=='/':
						equation['LHS'] = "1"+StrOper+OtherTerm	
		else:
			if ChkOperation=='^':
				print equation['LHS']
				print "HH"
				print equation['RHS']
				print "KK"
				print FirstTerm
				print "JJ"
				print OtherTerm
				print "II"
				equation['LHS']=FirstTerm
				equation['RHS']="("+equation['RHS']+")^(1/("+OtherTerm+"))"
				print 'Take the ',OtherTerm,' root of both sides'
			
			else:
				if BreakUp(OtherTerm,ChkOperation)['location']==-1 and BreakUp(OtherTerm,InvOperation)['location']==-1:
					
					BreakVar = -1
					slft = len(OtherTerm)
					for i in range(0,slft):
						if OtherTerm[i]==variable:
							BreakVar = i
										
					if BreakVar==-1:
						if StartPoint > 0:
							
							if equation['LHS'][originL['location']+StartPoint:originL['location']+StartPoint+1]==StrOper:
								equation['RHS']="("+equation['RHS']+")"+COper+"("+OtherTerm+")"
							
							else:
								equation['RHS']="("+equation['RHS']+")"+StrOper+"("+OtherTerm+")"	
							equation['LHS'] = equation['LHS'][0:StartPoint]+FirstTerm
							
						
						else:

							
							if equation['LHS'][originL['location']+StartPoint:originL['location']+StartPoint+1]==StrOper:
								equation['RHS']="("+equation['RHS']+")"+COper+"("+OtherTerm+")"
							
							else:
								equation['RHS']="("+equation['RHS']+")"+StrOper+"("+OtherTerm+")"	
							equation['LHS']=FirstTerm
							
				else:
					SPoint=StartPoint+len(FirstTerm)+1
					originLp = BreakUp(equation['LHS'][SPoint:len(equation['LHS'])],ChkOperation)
					originLm = BreakUp(equation['LHS'][SPoint:len(equation['LHS'])],InvOperation)
					if originLp['location']!=-1:
						if originLm['location']!=-1:
							if originLp['location']<originLm['location']:
								originL=originLp
							
							else:
								originL=originLm
							
						
						else:
							originL=originLp
						
					
					else:
						originL=originLm
					
					equation = MoveLtoR(equation, originL,variable,SPoint,ChkOperation,InvOperation)

	elif DivideUp(equation['LHS'],0)['location']==-1:
		BreakVar = -1
		slft = len(equation['LHS'])
		for i in range(0,slft):
			if equation['LHS'][i]==variable:
				BreakVar = i
			
		
		if BreakVar==-1:
			if equation['LHS']!="0":
				equation['RHS'] = "("+equation['RHS']+")-("+equation['LHS']+")"
				equation['LHS'] = "0"
	return equation

def MoveRtoL(equation, originL, variable, StartPoint, ChkOperation, InvOperation):
	if originL['operation']==ChkOperation or originL['operation']==InvOperation:
		FirstTerm = equation['RHS'][StartPoint:StartPoint+originL['location']]
		OtherTerm = equation['RHS'][StartPoint+originL['location']+1:len(equation['RHS'])]
		BreakVar = -1
		slft = len(FirstTerm)
		for i in range(0,slft):
			if FirstTerm[i]==variable:
				BreakVar = i
		StrOper = InvOperation
		COper = ChkOperation
		if BreakVar!=-1:
			if StartPoint > 0:
				if equation['RHS'][StartPoint-1:StartPoint]==StrOper:
					equation['LHS']="("+equation['LHS']+")"+COper+"("+FirstTerm+")"
				
				else:
					if ChkOperation=='^':
						if OtherTerm.find(variable)!=-1:
							equation['LHS']="ln("+equation['LHS']+")"
							equation['RHS'] = "("+OtherTerm+")*ln("+equation['RHS'][0:StartPoint-1]+"^"+FirstTerm+")"
						
					
					else:
						equation['LHS']="("+equation['LHS']+")"+StrOper+"("+FirstTerm+")"	
					
				
				if ChkOperation !='^':
					if originL['operation']==ChkOperation:
						equation['RHS'] = equation['RHS'][0:StartPoint-1]+COper+OtherTerm
					
					else:
						equation['RHS'] = equation['RHS'][0:StartPoint-1]+StrOper+OtherTerm	
					
				
			
			else:

				if equation['RHS'][0:1]==StrOper:
					equation['LHS']="("+equation['LHS']+")"+COper+"("+FirstTerm[1:len(FirstTerm)]+")"
				
				else:
					if ChkOperation=='^':
						if OtherTerm.find(variable)!=-1:
							equation['LHS']="ln("+equation['LHS']+")"
							equation['RHS'] = "("+OtherTerm+")*ln("+FirstTerm+")"
						
					
					else:
						equation['LHS']="("+equation['LHS']+")"+StrOper+"("+FirstTerm+")"
					
				
				if originL['operation']==ChkOperation:
					if ChkOperation !='^':
						equation['RHS'] = OtherTerm
					
				
				else:
					if InvOperation=='-':
						equation['RHS'] = StrOper+OtherTerm	
					
					elif InvOperation=='/':
						equation['RHS'] = "1"+StrOper+OtherTerm	
		else:
			if ChkOperation=='^':
				print equation['RHS']
				print "HH"
				print equation['LHS']
				print "KK"
				print FirstTerm
				print "JJ"
				print OtherTerm
				print "II"
				equation['RHS']=FirstTerm
				equation['LHS']="("+equation['LHS']+")^(1/("+OtherTerm+"))"
			
			else:
				if BreakUp(OtherTerm,ChkOperation)['location']==-1 and BreakUp(OtherTerm,InvOperation)['location']==-1:
					
					BreakVar = -1
					slft = len(OtherTerm)
					for i in range(0,slft):
						if OtherTerm[i]==variable:
							BreakVar = i
										
					if BreakVar!=-1:
						if StartPoint > 0:
							
							if equation['RHS'][originL['location']+StartPoint:originL['location']+StartPoint+1]==StrOper:
								equation['LHS']="("+equation['LHS']+")"+COper+"("+OtherTerm+")"
							
							else:
								equation['LHS']="("+equation['LHS']+")"+StrOper+"("+OtherTerm+")"	
							equation['RHS'] = equation['RHS'][0:StartPoint]+FirstTerm
							
						
						else:

							
							if equation['RHS'][originL['location']+StartPoint:originL['location']+StartPoint+1]==StrOper:
								equation['LHS']="("+equation['LHS']+")"+COper+"("+OtherTerm+")"
							
							else:
								equation['LHS']="("+equation['LHS']+")"+StrOper+"("+OtherTerm+")"
							equation['RHS']=FirstTerm	
							
				else:

					SPoint=StartPoint+len(FirstTerm)+1
					originLp = BreakUp(equation['RHS'][SPoint:len(equation['RHS'])],ChkOperation)
					originLm = BreakUp(equation['RHS'][SPoint:len(equation['RHS'])],InvOperation)
					if originLp['location']!=-1:
						if originLm['location']!=-1:
							if originLp['location']<originLm['location']:
								originL=originLp
							
							else:
								originL=originLm
							
						
						else:
							originL=originLp
						
					
					else:
						originL=originLm
					
					equation = MoveRtoL(equation, originL,variable,SPoint,ChkOperation,InvOperation)

	elif DivideUp(equation['RHS'],0)['location']==-1:
		BreakVar = -1
		slft = len(equation['RHS'])
		for i in range(0,slft):
			if equation['RHS'][i]==variable:
				BreakVar = i
			
		
		if BreakVar!=-1:
			if equation['RHS']!="0":
				equation['LHS'] = "("+equation['LHS']+")-("+equation['RHS']+")"
				equation['RHS'] = "0"
	return equation
import sys
def main():
	variable='x';
	source = sys.argv[1];
	equation = GetLR(source);
	print equation['LHS'], equation['RHS']
	equation['LHS']=simplify.CombineAllFloats(equation['LHS'])
	equation['RHS']=simplify.CombineAllFloats(equation['RHS'])
	if equation['haseq']==1:
		oldequation = equation
		newequation = {'LHS':"FAKE",'RHS': 'FAKE'}
		while oldequation['LHS'] != newequation['LHS'] or oldequation['RHS']!= newequation['RHS']:
			oldequation=equation
			originL = DivideUp(equation['LHS'],0)
			print equation, 'LtoR'
			equation = MoveLtoR(equation, originL,variable,0,'+','-')
			print equation, 'LtoR'
			newequation=equation
			if oldequation['LHS'] == newequation['LHS'] and oldequation['RHS']== newequation['RHS']:
				oldequation=equation
				originL = DivideUp(equation['LHS'],0)
				equation = MoveLtoR(equation, originL,variable,0,'*','/')
				newequation=equation
			
			if oldequation['LHS'] == newequation['LHS'] and oldequation['RHS']== newequation['RHS']:
				oldequation=equation
				originL = DivideUp(equation['LHS'],0)
				equation = MoveLtoR(equation, originL,variable,0,'^','p')
				newequation=equation
			equation['LHS']=simplify.CombineAllFloats(equation['LHS'])
			equation['RHS']=simplify.CombineAllFloats(equation['RHS'])
			
		

		oldequation = equation
		newequation = {'LHS':"FAKE",'RHS': 'FAKE'}
		while oldequation['LHS'] != newequation['LHS'] or oldequation['RHS']!= newequation['RHS']:
			oldequation=equation
			originR = DivideUp(equation['RHS'],0)
			print equation, 'RtoL'
			equation = MoveRtoL(equation, originR,variable,0,'+','-')
			print equation, 'RtoL'
			newequation=equation
			if oldequation['LHS'] == newequation['LHS'] and oldequation['RHS']== newequation['RHS']:
				oldequation=equation
				originR = DivideUp(equation['RHS'],0)
				equation = MoveRtoL(equation, originR,variable,0,'*','/')
				newequation=equation
			
			if oldequation['LHS'] == newequation['LHS'] and oldequation['RHS']== newequation['RHS']:
				oldequation=equation
				originR = DivideUp(equation['RHS'],0)
				equation = MoveRtoL(equation, originR,variable,0,'^','p')
				newequation=equation
			equation['LHS']=simplify.CombineAllFloats(equation['LHS'])
			equation['RHS']=simplify.CombineAllFloats(equation['RHS'])
	


	print 'LHS:', equation['LHS']
	print 'RHS:', equation['RHS']
	return 0

main()
