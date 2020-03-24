


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


def RemovePar(source):
	breakeq = -1
	slength = len(source)
	source0 = source
	source = " "
	while source != source0:
		source = source0
		slength = len(source)
		for i in range(0,slength-1):
			if source[i]=='(':
				if source[i+1]=='(':
					for ii in range(i+1,slength-1):
						if fullparen(source[i+1:ii+1])==0:
							if source[ii+1]==')':
								source0=source[0:i]+source[i+1:ii+1]+source[ii+2:len(source)]
							break
				else:
					for ii in range(i,slength):
						if fullparen(source[i:ii+1])==0:
							if i>0:
								if source[i-1]=='+' or source[i-1]=='(':
									source0=source[0:i]+source[i+1:ii]+source[ii+1:len(source)]
								elif source[i-1]=='-':
									origin = DivideUp(source[i+1:ii],0)
									if origin['operation']=='+':
										source0=source[0:i-1]+'-'+source[i+1:origin['location']+i+1]+'-'+source[origin['location']+i+2:ii]+source[ii+1:len(source)]
									elif origin['operation']=='-':
										source0=source[0:i-1]+'-'+source[i+1:origin['location']+i+1]+'+'+source[origin['location']+i+2:ii]+source[ii+1:len(source)]
									else:
										if source[i+1]=='-':
											source0=source[0:i-1]+'+'+source[i+2:ii]+source[ii+1:len(source)]
										else:
											source0=source[0:i-1]+'-'+source[i+1:ii]+source[ii+1:len(source)]
								break
							else:
								if ii==slength-1:
									source0=source[1:len(source)-1]
								else:
									if source[ii+1]=='+' or source[ii+1]=='-':
										source0=source[1:ii]+source[ii+1:len(source)]
								break
	return source0


def ChkDouble(source):
	try:
		source = float(source)
		if source == int(source):
			ToReturn = {'ivalue':int(source),'dvalue':0,'type':'int'}
		else:
			ToReturn = {'ivalue':0,'dvalue':source,'type':'double'}
	except:
		ToReturn = {'ivalue':0,'dvalue':0,'type':'Not'}


	return ToReturn;


def RemoveExtra(source):
	
	source0=''
	while source !=source0:
		source0 = source
		strlength = len(source)
		for i in range(0,strlength-1):
			if source[i:i+2]=="+-":
				source = source[0:i]+source[i+1:]
				break
			if source[i:i+2]=="--":
				source = source[0:i]+'+'+source[i+2:]
				break

	return source


def CombineFloats(source):

	origin = {'location': 0, 'operation': ''}
	SPoint = 0
	while origin['location'] != -1:
		origin = DivideUp(source,SPoint)
		if origin['operation']=='+' or origin['operation']=='-':
			ChkTerm = ChkDouble(source[SPoint:origin['location']+SPoint])
			originn = DivideUp(source,SPoint+origin['location']+1)
			if originn['operation']=='+' or originn['operation']=='-':
				ChkNTerm = ChkDouble(source[SPoint+origin['location']+1:originn['location']+SPoint+origin['location']+1])
			else:
				ChkNTerm = ChkDouble(source[SPoint+origin['location']+1:])
			if ChkTerm['type']=="int":
				if ChkTerm['ivalue']==0:
					if SPoint > 0:
						NewSource = source[0:SPoint-1]+source[SPoint+1:]
						if NewSource[0]=='+':
							NewSource = NewSource[1:]
						return NewSource
					else:
						NewSource = source[SPoint+1:]
						if NewSource[0]=='+':
							NewSource = NewSource[1:]
						return NewSource
				if ChkNTerm['type']=="int":
					cvalue = ChkTerm['ivalue']
					nvalue = ChkNTerm['ivalue']
					if SPoint>0:
						if source[SPoint-1:SPoint]=="-":
							if source[SPoint+origin['location']:1+SPoint+origin['location']]=="-":
								if originn['location'] != -1:
									NewSource = source[0:SPoint-1]+source[SPoint+origin['location']+1+originn['location']:]+"+"+str(-1*cvalue-nvalue)
									return NewSource
								else:
									NewSource = source[0:SPoint-1]+"+"+str(-1*cvalue-nvalue)
									return NewSource
							else:
								if originn['location'] != -1:
									NewSource = source[0:SPoint-1]+source[SPoint+origin['location']+1+originn['location']:]+"+"+str(-1*cvalue+nvalue)
									return NewSource
								
								else:
									NewSource = source[0:SPoint-1]+"+"+str(-1*cvalue+nvalue)
									return NewSource
						else:
							if source[SPoint+origin['location']:SPoint+origin['location']+1]=="-":
								if originn['location'] != -1:
									NewSource = source[0:SPoint-1]+source[SPoint+origin['location']+1+originn['location']:]+"+"+str(cvalue-nvalue)
									return NewSource
								
								else:
									NewSource = source[0:SPoint-1]+"+"+str(cvalue-nvalue)
									return NewSource
							else:
								if originn['location'] != -1:
									NewSource = source[0:SPoint-1]+source[SPoint+origin['location']+1+originn['location']:]+"+"+str(cvalue+nvalue)
									return NewSource
								
								else:
									NewSource = source[0:SPoint-1]+"+"+str(cvalue+nvalue)
									return NewSource
					else:
						originnn = DivideUp(source,SPoint+origin['location']+originn['location']+1)
						if originnn['operation'] != '+' and originnn['operation'] != '-':
							if origin['operation']=='-':
								NewSource = str(cvalue-nvalue)
							else:
								NewSource = str(cvalue+nvalue)
							return NewSource

						if source[0:1]=="-":
							if origin['operation']=='-':
								NewSource = source[origin['location']:]+source[0:origin['location']]
								return NewSource
							
							else:
								NewSource = source[origin['location']+1:]+source[0:origin['location']]
								return NewSource

						else:
							if origin['operation']=='-':
								NewSource = source[origin['location']:]+"+"+source[0:origin['location']]
								return NewSource
							
							else:
								NewSource = source[origin['location']+1:]+"+"+source[0:origin['location']]
								return NewSource
				else:
					if SPoint>0:
						if source[SPoint-1:SPoint]=="-":
							NewSource = source[0:SPoint-1]+source[SPoint+origin['location']:]+"-"+source[SPoint:origin['location']+SPoint]
							return NewSource
						
						else:
							NewSource = source[0:SPoint-1]+source[SPoint+origin['location']:]+"+"+source[SPoint:origin['location']+SPoint]
							return NewSource
					
					
					else:
						if source[0:1]=="-":
							if origin['operation']=='-':
								NewSource = source[origin['location']:]+source[0:origin['location']]
								return NewSource
							
							else:
								NewSource = source[origin['location']+1:]+source[0:origin['location']]
								return NewSource
							
						
						else:
							if origin['operation']=='-':
								NewSource = source[origin['location']:]+"+"+source[0:origin['location']]
								return NewSource
							
							else:
								NewSource = source[origin['location']+1:]+"+"+source[0:origin['location']]
								return NewSource
		else:
			#ChkTerm = ChkDouble(source[SPoint:])
			#if ChkTerm['type']=="int":
			#	if SPoint>0:
			#		if source[SPoint-1:SPoint]=="-":
			#			print -1*ChkTerm['ivalue']
			#		
			#		else:
			#			print ChkTerm['ivalue']
			#	else:
			#		print ChkTerm['ivalue']
			break
		SPoint=SPoint+origin['location']+1

	return source
def CombineAllFloats(source):
	source0 = ''
	while source != source0:
		source0 = source
		source = RemovePar(source)

		source=CombineFloats(source)
		if source[-2:]=='-0' or source[-2:]=='+0':
			source = source[:-2]
		source = RemoveExtra(source)
	return source


source = CombineAllFloats('7*6+3')

print source
'''
int main(void) {

	string source;
	cout << "Enter Equation: ";
	char variable;
	variable='x';
	cin >> source;
	source = RemovePar(source);
	cout << source;
	cout << "HH";
	source = CombineFloats(source);
	cout << source;
	cout << "AA";
	source = RemoveExtra(source);
	cout << source;

	return 0;
}
'''
