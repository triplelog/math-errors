import time
import copy
##print time.time()
from integral.sumrule import sumrule
from integral.clean import cleanpar
from integral.constantmultiple import pulloutconstant
from integral.powerrule import powerrule
from integral.expolog import expologrule
from integral.trigrule import trigrule
from integral.usub import usub
from integral.ibp import ibp
import json

#from sumrule import sumrule
#from clean import cleanpar
#from constantmultiple import pulloutconstant
#from powerrule import powerrule
#from expolog import expologrule
#from trigrule import trigrule
#from usub import usub
#from ibp import ibp
#import checkcorrect
import sympy
import os
import sys

allletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def toJavascript(input_string):
	input_string = input_string.replace('\\','\\\\')
	#input_string = input_string.replace(r'$',r'')
	input_string = r'\\text{'+input_string+'}'

	return input_string

def trigAudio(input_fn,dvar):
	if input_fn == 'sin('+dvar+')':
		return 'sine'
	elif input_fn == 'cos('+dvar+')':
		return 'cosine'
	else:
		return 'blank'


def myslatex(input_string):
	input_string = sympy.latex(input_string.replace('abs(x)','holdforit')).replace('holdfordydx','\\frac{dy}{dx}').replace('log{','ln{').replace('log^','ln^').replace('holdforit','|x|')
	return input_string
def slatex(f,dvar):
	try:
		return myslatex(sympy.sympify(f,evaluate=True))
	except:
		return myslatex(sympy.sympify(f))
def getlatex(input_string):
	if input_string in ['+','-','*','^','/']:
		return input_string, 'blank', 1.0, 'black', '', []
	audioIndex = input_string.find('audio')
	if audioIndex == -1:
		audioIndex = len(input_string)
	for i in range(0,audioIndex):
		if input_string[i]=='(':
			sindex = i
			break
	for i in range(0,audioIndex):
		if input_string[i]==')':
			eindex = i
	intf = input_string[:audioIndex].find('\int')
	if audioIndex < len(input_string)-5:
		audioStr = input_string[audioIndex+5:]
	else:
		if intf>0:
			return '\displaystyle\int '+slatex(input_string[sindex:eindex+1],input_string[:intf])+'d'+input_string[:intf], 'blank', 1.0, 'black', '', []
		else:
			return slatex(input_string[sindex:eindex+1],input_string[:sindex]), 'blank', 1.0, 'black', '', []

	ruleIndex = audioStr.find('rule')
	typeIndex = audioStr.find('type')
	fnIndex = audioStr.find('function')
	dvar = input_string[:1]
	myduration = 1.0
	mycolor = 'green'
	mytext = 'Other'
	mylatex = []
	if audioStr[typeIndex+4:fnIndex] == 'usub':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ using u-sustitution with $u='+slatex(audioStr[fnIndex+8:audioStr.find('newint')],dvar)+r'$'
		line1 = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ using u-sustitution'
		line2 = 'Let $u='+slatex(audioStr[fnIndex+8:audioStr.find('newint')],dvar)+r'$'
		line3 = 'Then $du='+myslatex(sympy.diff(sympy.sympify(cleanpar(audioStr[fnIndex+8:audioStr.find('newint')],dvar)),sympy.sympify(dvar)))+'d'+dvar+r'$'
		line4 = 'We want to find $\\displaystyle\\int '+slatex(audioStr[audioStr.find('newint')+6:],'u')+r'du$'
		mylatex = [line1,line1+'\n\\newline\n'+line2,line1+'\n\\newline\n'+line2+'\n\\newline\n'+line3,line1+'\n\\newline\n'+line2+'\n\\newline\n'+line3+'\n\\newline\n'+line4]
		myduration = [3.5,2.0,2.5,4.0]
		mycolor = 'yellow'
		audioStr = ['usub1','usub2','usub3','usub4']
		
	elif audioStr[typeIndex+4:fnIndex] == 'replace':
		mytext = r'Replace $u$ with $'+slatex(audioStr[fnIndex+8:audioStr.find('newint')],dvar)+r'$'
		myduration = 5.0
		mycolor = 'yellow'
		audioStr = 'replace1'
	elif audioStr[typeIndex+4:fnIndex] == 'trig':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by undoing trigonometric differentiation'
		myduration = 5.0
		mycolor = 'blue'
		audioStr = trigAudio(audioStr[:ruleIndex],dvar)
	elif audioStr[typeIndex+4:fnIndex] == 'multiple':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by bringing the $'+slatex(audioStr[fnIndex+8:],dvar)+r'$ outside the integral'
		myduration = 2.0
		mycolor = 'brown'
		audioStr = 'constant1'
	elif audioStr[typeIndex+4:fnIndex] == 'ibp':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by using integration by parts: $u='+slatex(audioStr[fnIndex+8:audioStr.find('dv')],dvar)+r'$'
		line1 = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ using integration by parts'
		line2 = 'Let $u='+slatex(audioStr[fnIndex+8:audioStr.find('dv')],dvar)+r'$ and $dv='+slatex(audioStr[audioStr.find('dv')+2:audioStr.find('regv')],dvar)+'d'+str(dvar)+r'$'
		line3 = 'Then $du='+slatex(audioStr[audioStr.find('du')+2:],dvar)+'d'+str(dvar)+r'$ and $v='+slatex(audioStr[audioStr.find('regv')+4:audioStr.find('du')],dvar)+r'$'
		line4 = 'We want to find $uv-\\displaystyle\\int vdu$'
		mylatex = [line1,line1+'\n\\newline\n'+line2,line1+'\n\\newline\n'+line2+'\n\\newline\n'+line3,line1+'\n\\newline\n'+line2+'\n\\newline\n'+line3+'\n\\newline\n'+line4]
		myduration = [4.0,4.0,4.0,4.0]
		mycolor = 'orange'
		audioStr = ['blank','blank','blank','blank']
	elif audioStr[typeIndex+4:fnIndex] == 'explog':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by integrating the exponential: $'+slatex(audioStr[fnIndex+8:],dvar)+r'$'
		myduration = 1.0
		mycolor = 'green'
		audioStr = 'blank'
	elif audioStr[typeIndex+4:fnIndex] == 'power':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by integrating the power function: $'+slatex(audioStr[fnIndex+8:],dvar)+r'$'
		myduration = 1.0
		mycolor = 'aqua'
		audioStr = 'blank'
	elif audioStr[typeIndex+4:fnIndex] == 'sum':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by breaking the integral into $'+slatex(audioStr[fnIndex+8:],dvar)+r'$ terms'
		myduration = 1.0
		mycolor =  'purple'
		audioStr = 'blank'
	elif audioStr[typeIndex+4:fnIndex] == 'constant':
		mytext = r'Find $\displaystyle\int '+slatex(audioStr[:ruleIndex],dvar)+r'd'+dvar+r'$ by integrating the constant $'+slatex(audioStr[fnIndex+8:],dvar)+r'$'
		myduration = 1.0
		mycolor = 'red'
		audioStr = 'blank'
	else:
		audioStr = 'blank'
	

	if intf>0:
		return '\displaystyle\int '+slatex(input_string[sindex:eindex+1],input_string[:intf])+'d'+input_string[:intf],  audioStr, myduration, mycolor, mytext, mylatex
	else:
		return slatex(input_string[sindex:eindex+1],input_string[:sindex]), audioStr, myduration, mycolor, mytext, mylatex

		

def justexp(input_string):
	if input_string in ['+','-','*','^','/']:
		return input_string, 'x'
	for i in range(0,len(input_string)):
		if input_string[i]=='(':
			sindex = i
			break
	for i in range(0,len(input_string)):
		if input_string[i]==')':
			eindex = i
	return input_string[sindex:eindex+1], input_string[:sindex]

def printrow(darray,darrayseq,allnodes,lastnode):
	for i in range(0,len(darray)):
		if len(darray[i])==3:
			if darray[i][1]=='usub':
				lastnode.append([darray[i][2],darrayseq])
			else:
				darray[i][2]=darrayseq+darray[i][1]
				allnodes.append(darray[i])
		elif len(darray[i])>3:
			darray[i][2]=darrayseq+darray[i][1]
			darray[i][3],allnodes,lastnode = printrow(darray[i][3],darray[i][2],allnodes,lastnode)
			allnodes.append(darray[i][:3])
	return darray,allnodes,lastnode

def nnonaone(darray,seq):
	myb = 0
	if len(seq)>0:
		if seq[-1]=='a':
			for i in darray:
				if i[2][:-1]==seq[:-1] and i[2][-1]=='b':
					myb=1
		else:
			myb=1
	return myb
def nnona(darray,seq):
	myb = 0
	if len(seq)>0:
		for i in range(0,len(seq)):
			myb+=nnonaone(darray,seq[:i+1])
	return myb
def getrounds(darray,n,seq):

	for i in range(0,len(darray)):
		if darray[i][2][:-1]==seq:
			if len(darray[i])>3:
				darray[i][3]=str(n)
			else:
				darray[i].append(str(n))
			if len(darray[i])>4:
				darray[i][4]=nnona(darray,darray[i][2])
			else:
				darray[i].append(nnona(darray,darray[i][2]))



	for i in range(0,len(darray)):
		if len(darray[i][2])==len(seq)+2:
			if darray[i][2][-1]=='a':
				if darray[i][2][:len(seq)]==seq:
					n,darray=getrounds(darray,n+1,darray[i][2][:len(seq)+1])

	return n,darray

def getnodes(allnodes,maxrounds,maxsp,lastnode):
	extranodes = []
	nodes = []
	nextnodes = []
	recentnode = []
	integralnode = []
	for i in range(0,len(allnodes)):
		if int(allnodes[i][3])< maxrounds:
			nodes.append(allnodes[i])
		if int(allnodes[i][3])== maxrounds:
			nextnodes.append(allnodes[i])
	if len(nextnodes)== 1:
		recentnode = []
		
		for i in range(0,len(nodes)):
			if nodes[i][2][:len(nextnodes[0][2])-len(nextnodes[0][1])]==nextnodes[0][2][:-len(nextnodes[0][1])] and len(nodes[i][2])==len(nextnodes[0][2])-len(nextnodes[0][1])+1:
				maxlength = 0
				maxcode = i
				for ii in range(0,len(nodes)):
					if nodes[ii][2][:len(nodes[i][2])]==nodes[i][2] and len(nodes[ii][2])<len(nextnodes[0][2]):
						if len(nodes[ii][2])>maxlength:
							maxlength = len(nodes[ii][2])
							maxcode = ii
				recentnode.append(maxcode)
	if len(nextnodes)>= 1:
		integralnode = []
		for i in range(0,len(nodes)):
			if nodes[i][2]==nextnodes[0][2][:-1] and len(nextnodes[0][1])==1:
				integralnode.append(i)

	allterminates = True
	for i in nodes:
		nonterminal = False
		for ii in allnodes:
			if ii[2][:len(i[2])+1]==i[2]+'b':
				nonterminal = True
		if nonterminal:
			terminates = True
			maxadd = 0
			maxlength = 0
			maxcode = ''
			for ii in allnodes:
				if ii[2][:len(i[2])]==i[2] and int(ii[3])>=maxrounds:
					terminates = False
				if ii[2][:len(i[2])]==i[2] and ii[4]>i[4]+maxadd:
					maxadd = ii[4]-i[4]
				if ii[2][:len(i[2])]==i[2]:
					if len(ii[2])>maxlength:
						maxlength = len(ii[2])
						maxcode = ii[2][len(i[2]):]
			if terminates:
				donotdoanyting = 1
			else:
				allterminates = False
			if maxadd==maxsp:
				maxr = 0
				dou = False
				for ii in lastnode:
					if ii[1]==i[2]:
						urep = ii[0]
						dou = True
				if dou:
					for ii in allnodes:
						if ii[2][:len(i[2])]==i[2]:
							if int(ii[3])>maxr:
								maxr = int(ii[3])
					for iii in range(0,len(nodes)):
						if int(nodes[iii][3])>maxr:
							nodes[iii][3]=str(int(nodes[iii][3])+2)
					nodes.append([i[0],maxcode+'a',i[2]+maxcode+'a',str(maxr+1),i[4]])
					nodes.append([urep,'a',i[2]+maxcode+'aa',str(maxr+2),i[4]+1])

				else:
					for ii in allnodes:
						if ii[2][:len(i[2])]==i[2]:
							if int(ii[3])>maxr:
								maxr = int(ii[3])
					for iii in range(0,len(nodes)):
						if int(nodes[iii][3])>maxr:
							nodes[iii][3]=str(int(nodes[iii][3])+1)
					nodes.append([i[0],maxcode+'a',i[2]+maxcode+'a',str(maxr+1),i[4]])


	if allterminates:
		i = ['','','','0',0]
		nonterminal = False
		for ii in allnodes:
			if ii[2][:len(i[2])+1]==i[2]+'b':
				nonterminal = True
		if nonterminal:
			terminates = True
			maxadd = 0
			maxlength = 0
			maxcode = ''
			for ii in allnodes:
				if ii[2][:len(i[2])]==i[2] and int(ii[3])>=maxrounds:
					terminates = False
				if ii[2][:len(i[2])]==i[2] and ii[4]>i[4]+maxadd:
					maxadd = ii[4]-i[4]
				if ii[2][:len(i[2])]==i[2]:
					if len(ii[2])>maxlength:
						maxlength = len(ii[2])
						maxcode = ii[2][len(i[2]):]
			if terminates:
				donotdoanyting = 1
			else:
				allterminates = False
			if maxadd==maxsp:
				maxr = 0
				for ii in allnodes:
					if ii[2][:len(i[2])]==i[2]:
						if int(ii[3])>maxr:
							maxr = int(ii[3])
				for iii in range(0,len(nodes)):
					if int(nodes[iii][3])>maxr:
						nodes[iii][3]=str(int(nodes[iii][3])+1)
				nodes.append([i[0],maxcode+'a',i[2]+maxcode+'a',str(maxr+1),i[4]])



	return nodes, extranodes,recentnode,integralnode

def letterbefore(x):
	allletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for i in range(1,len(allletters)):
		if allletters[i]==x:
			return allletters[i-1]

def createdisplay(dparts,maxrounds,my_function,dvar):
	duration = 1.0
	color = 'black'
	textstr = ''
	allnodes = []
	lastnode = []
	latexstr = []
	audiostr = 'blank'
	darray,allnodes,lastnode = printrow(dparts,'',allnodes,lastnode)

	everynode = getrounds(allnodes,0,'')[1]

	nodes0 = ''
	allnodes0 = everynode
	
	maxsp = 0
	recentnode = []
	while nodes0 != allnodes0:
		nodes0 = allnodes0
		maxsp +=1
		allnodes0,extranodes,recentnode, integralnode = getnodes(allnodes0,10000,maxsp,lastnode)

	max3 = 4
	for i in range(0,len(allnodes0)):
		try:
			if len(allnodes0[i][2]) > max3:
				max3 = len(allnodes0[i][2])
		except:
			pass
	allnodes0,extranodes,recentnode, integralnode = getnodes(allnodes0,maxrounds,maxsp,lastnode)

	allnodes = allnodes0
	
	#for i in allnodes:
	#	thestr += i
	extranodes = []

	for i in range(0,len(allnodes)):
		allnodes[i][3]=allnodes[i][1]



	margin = 20
	nodedy = int(390/max3)
	nodedx = 50
	if max3 < 9:
		thestr = r'\LARGE'
	else:
		thestr = r'\Large'
	length_lines = []
	if max3 < 10:
		base_str = '\\begin{minipage}{.575\linewidth}\n\\LARGE\n\\begin{tikzpicture}[node distance = '+str(nodedy)+'pt]'
	else:
		base_str = '\\begin{minipage}{.575\linewidth}\n\\Large\n\\begin{tikzpicture}[node distance = '+str(nodedy)+'pt]'
	nodes = []
	nodes.append('\\node (dec'+str(len(nodes))+') [processlong] {$\displaystyle\int '+slatex(cleanpar(my_function,dvar),dvar)+'d'+dvar+'$};')
	parentstr = dvar+'\int('+cleanpar(my_function,dvar)+')'+'audio'+cleanpar(my_function,dvar)+'rule'+fullintegral(cleanpar(my_function,dvar),dvar,-1,0,0)
	if len(allnodes)==0:
		myexp, myaudio, myduration, mycolor, mytext, mylatex = getlatex(parentstr)
		duration = myduration
		color = mycolor
		textstr = mytext
		latexstr = mylatex
		audiostr = myaudio


	unsorted = True

	while unsorted:
		unsorted = False
		for i in range(0,len(allnodes)-1):
			if len(allnodes[i][2])>len(allnodes[i+1][2]) or (len(allnodes[i][2])==len(allnodes[i+1][2]) and allnodes[i][2]>allnodes[i+1][2]):
				pholder = allnodes[i]
				allnodes[i]=allnodes[i+1]
				allnodes[i+1]=pholder
				if i in recentnode:
					if i+1 not in recentnode:
						recentnode.remove(i)
						recentnode.append(i+1)
				else:
					if i+1 in recentnode:
						recentnode.remove(i+1)
						recentnode.append(i)
				if i in integralnode:
					if i+1 not in integralnode:
						integralnode.remove(i)
						integralnode.append(i+1)
				else:
					if i+1 in integralnode:
						integralnode.remove(i+1)
						integralnode.append(i)
				unsorted = True
	for i in range(0,len(allnodes)):
		if allnodes[i][2][-1]=='a':
			tot_length = str(-1*margin)+'pt'
			for ii in range(i,len(allnodes)):
				if len(allnodes[ii][2])==len(allnodes[i][2]) and allnodes[ii][2][:-1]==allnodes[i][2][:-1]:
					tot_length += '+'+str(margin)+'pt+\myl'+allnodes[ii][2]
				else:
					break
			allnodes[i][1]=tot_length
	for i in range(0,len(allnodes)):
		allnodes[i].append('')
		for ii in range(i+1,len(allnodes)):
			if allnodes[ii][2][:-len(allnodes[ii][3])]==allnodes[i][2] and len(allnodes[ii][2])==len(allnodes[i][2])+1  and 'a'==allnodes[ii][2][-1]:
				allnodes[i][5]=allnodes[ii][1]

	

	

	pnode = 'dec0'
	arrows = []

	for idx,i in enumerate(allnodes):
		pnode = i[2][:-len(i[3])]
		if len(i[3])>1:
			thisnode = ''
			maxdvar = 'x'
			for ii in allnodes:
				if ii[2][:len(pnode)]==pnode and len(ii[2])==len(pnode)+1:
					maxlength = 0
					for iii in allnodes:
						if iii[2][:len(ii[2])]==ii[2]:
							if iii[2][:len(i[2])]!=i[2]:
								if len(iii[2])>maxlength:
									maxlength = len(iii[2])
									maxcode = iii[2]
									maxexp, maxdvar = justexp(iii[0])
					arrows.append('\draw [<-,thick] (dec'+maxcode+') |- (dec'+i[2]+'.north);')
					thisnode=thisnode+maxexp
			i[0]=maxdvar+'('+thisnode+')'
			if pnode[:-1] == '':
				uIndex = parentstr.find('usubfunction')
				if uIndex>-1 and i[0].find('audio') == -1:
					i[0] += 'audioruletypereplacefunction'+parentstr[uIndex+12:]
					#donot = 0
			else:
				for ii in allnodes:
					if ii[2] == pnode[:-1]:
						uIndex = ii[0].find('usubfunction')
						if uIndex>-1 and i[0].find('audio') == -1:
							i[0] += 'audioruletypereplacefunction'+ii[0][uIndex+12:]
				
		else:
			if pnode == '':
				pnode = '0'
			arrows.append('\draw [->,thick] (dec'+pnode+'.south) -| (dec'+i[2]+'.north);')
			
		myexp, myaudio, myduration, mycolor, mytext, mylatex = getlatex(i[0])
		length_lines.append('\\newlength{\myl'+i[2]+'}\settowidth{\myl'+i[2]+'}{$'+myexp+'$}')
		if i[2][-1]=='a':
			if len(i[2])>1:
				pnode = i[2][:-len(i[3])]
			else:
				pnode = '0'
			if pnode =='':
				pnode = '0'

			if idx in recentnode:		
				nodes.append('\\node (dec'+i[2]+') [processop, below of= dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2, yshift=-'+str(-1*nodedy+nodedy*len(i[3]))+'pt ] {$'+myexp+'$};')
				#thestr += 'Combine'
				duration = 1.0
				color = 'black'
				textstr = 'Combine'
				latexstr = ['Combine these parts back together.']
				audiostr = 'blank'
			elif idx in integralnode:		
				nodes.append('\\node (dec'+i[2]+') [processop2, below of= dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2, yshift=-'+str(-1*nodedy+nodedy*len(i[3]))+'pt ] {$'+myexp+'$};')
				#thestr += myaudio
				duration = myduration
				color = mycolor
				textstr = mytext
				latexstr = mylatex
				audiostr = myaudio
			else:
				nodes.append('\\node (dec'+i[2]+') [processlong, below of= dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2, yshift=-'+str(-1*nodedy+nodedy*len(i[3]))+'pt ] {$'+myexp+'$};')
		else:
			snode = i[2][:-1]+letterbefore(i[2][-1])
			if idx in recentnode:
				nodes.append('\\node (dec'+i[2]+') [processop, right of= dec'+snode+', xshift='+str(-1*nodedy+margin)+'pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+myexp+'$};')
				#thestr += 'Combine'
				duration = 1.0
				color = 'black'
				textstr = 'Combine'
				latexstr = ['Combine these parts back together.']
				audiostr = 'blank'
			elif idx in integralnode:
				nodes.append('\\node (dec'+i[2]+') [processop2, right of= dec'+snode+', xshift='+str(-1*nodedy+margin)+'pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+myexp+'$};')
				#thestr += myaudio
				duration = myduration
				color = mycolor
				textstr = mytext
				latexstr = mylatex
				audiostr = myaudio
			else:
				nodes.append('\\node (dec'+i[2]+') [processlong, right of= dec'+snode+', xshift='+str(-1*nodedy+margin)+'pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+myexp+'$};')
		
		

	for i in length_lines:
		thestr += i+'\n'
	for i in range(0,len(allnodes)):
		if allnodes[len(allnodes)-i-1][5]!='':

			thestr += '\\newlength{\\temp'+allnodes[i][2]+'}\setlength{\\temp'+allnodes[i][2]+'}{'+allnodes[len(allnodes)-i-1][5]+'}'+'\n'
			thestr += '\ifthenelse{\myl'+allnodes[len(allnodes)-i-1][2]+'<\\temp'+allnodes[i][2]+'}{\def\myl'+allnodes[len(allnodes)-i-1][2]+'{\\temp'+allnodes[i][2]+'}}{}'+'\n'


	thestr += base_str
	for i in nodes:
		thestr += i+'\n'


	for i in arrows:
		thestr += i+'\n'
	return thestr, duration, color, textstr, latexstr, audiostr

def fullintegral(inputexpression,dvar,ycount,wrongness,tryudv):
	f = cleanpar(inputexpression,dvar)
	dparts = []
	dvar = str(sympy.sympify(dvar))
	nopart = str(cleanpar(inputexpression,dvar))
	badword = 0
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		if dvar.find(sstr)>-1:
			badword = 1
		nopart=nopart.replace(sstr,'')
	if nopart.find(dvar)==-1:
		if badword==0:
			fintegral = '('+nopart+')'+'*('+dvar+')'
			dparts = [[dvar+'('+fintegral+')','a','']]
			fintegral = str(sympy.sympify(fintegral))
			if ycount == -1:
				return 'typeconstantfunction'+f
			return fintegral, dparts
	h = pulloutconstant(f,dvar)


	if h[0]!=1:
		if ycount == -1:
			return 'typemultiplefunction'+h[0]
		ycount=ycount+1
		
		#print "Pull out the constant multiple", f
		f = h[0]+'*('+fullintegral(h[1],dvar,ycount,wrongness,tryudv)[0]+')'
		dparts = [[dvar+'('+h[0]+')','a',''],['*','b',''],[dvar+'\int('+h[1]+')'+'audio'+h[1]+'rule'+fullintegral(h[1],dvar,-1,wrongness,tryudv),'c','',fullintegral(h[1],dvar,ycount,wrongness,tryudv)[1]]]

	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			if ycount == -1:
				return 'typesumfunction'+str(int((len(h)+1)/2))
			ycount =ycount+1
			f = ''
			dparts = []
			###print h
			
			for idx, i in enumerate(h):
				nletter = allletters[idx]
				if idx %2==0:
					###print f, i, h
					#print 'break up the sums', f
					f=f+fullintegral(i,dvar,ycount,wrongness,tryudv)[0]
					dparts.append([dvar+'\int('+i+')'+'audio'+i+'rule'+fullintegral(i,dvar,-1,wrongness,tryudv),nletter,'',fullintegral(i,dvar,ycount,wrongness,tryudv)[1]])
				else:
					if i==0:
						f=f+'+'
						dparts.append(['+',nletter,''])
					else:
						f=f+'-'
						dparts.append(['-',nletter,''])
		else:
			##print f
			h = powerrule(f,dvar)
			if h[0]:
				if ycount == -1:
					return 'typepowerfunction'+f
				#print 'Apply the Power Rule', f
				f = h[1]
				dparts = [[dvar+'('+h[1]+')','a','']]
			else:
				h=expologrule(f,dvar)
				if h[0]:
					if ycount == -1:
						return 'typeexplogfunction'+f
					#print h[2]
					f=h[1]
					dparts = [[dvar+'('+h[1]+')','a','']]
				else:
					h=trigrule(f,dvar)
					if h[0]:
						if ycount == -1:
							return 'typetrigfunction'+f
						#print h[2]
						f=h[1]
						dparts = [[dvar+'('+h[1]+')','a','']]
					else:
						h=usub(f,dvar)
						if h[0]:
							#print 'Apply u-substitution', f, h
							if ycount == -1:
								return 'typeusubfunction'+h[2]+'newint'+h[1]
							f=fullintegral(h[1],'u',ycount,wrongness,tryudv)[0].replace('u',h[2])
							fulli = fullintegral(h[1],'u',ycount,wrongness,tryudv)[1]
							#print fulli
							fulli.append([slatex(f,dvar),'usub',dvar+'('+f+')'])
							dparts = [['u'+'\int('+h[1]+')'+'audio'+h[1]+'rule'+fullintegral(h[1],'u',-1,wrongness,tryudv),'a','',fulli]]
						else:
							if tryudv < 3:
								h=ibp(f,dvar)
								tryudv=tryudv+1
								if h[0]:
									foundudv = 0
									for iu in h[1]:
										##print iu
										u=iu[1]
										du=iu[3]
										dv=iu[4]
										try:
											if ycount > -1:
												v=fullintegral(dv,dvar,ycount,wrongness,3)[0] # change if want double ibp
											else:
												v=fullintegral(dv,dvar,0,wrongness,3)[0]

											##print 'vvv', dv, v
											if str(v) != 'NOD':
												if sympy.sympify('('+str(v)+')*('+str(du)+')')!=sympy.sympify(f):
													##print 'what', '('+str(v)+')*('+str(du)+')', u, v, du, dv
													tfi = fullintegral('('+str(v)+')*('+str(du)+')',dvar,ycount,wrongness,tryudv)[0] # change if want double ibp
													##print 'tfi', tfi
													if sympy.sympify('('+str(u)+')*('+str(v)+')-('+str(tfi)+')')!=sympy.sympify(f):
														if str(tfi) != 'NOD':
															#tryudv =tryudv+1
															##print tfi, u, v, du, dv, f, '('+str(u)+')*('+str(v)+')-('+str(tfi)+')'

															f='('+str(u)+')*('+str(v)+')-('+str(tfi)+')'
															fulli = fullintegral('('+str(v)+')*('+str(du)+')',dvar,ycount,wrongness,tryudv)[1]
															dparts = [[dvar+'('+str(u)+')','a',''],['*','b',''],[dvar+'('+str(v)+')','c',''],['-','d',''],[dvar+'\int('+'('+str(v)+')*('+str(du)+')'+')'+'audio'+'('+str(v)+')*('+str(du)+')'+'rule'+fullintegral('('+str(v)+')*('+str(du)+')',dvar,-1,wrongness,tryudv),'e','',fulli]]
															#print 'Apply integration by parts',f, u, v, du, dv
															if ycount == -1:
																return 'typeibpfunction'+str(u)+'dv'+str(dv)+'regv'+str(v)+'du'+str(du)
															foundudv = 1
															##print inputexpression, ycount
															return cleanpar(f,dvar),dparts
										except:
											pass
									if foundudv == 0:

										f = 'NOD'
										return 'NOD'
								else:

									f='NOD'
									return 'NOD'
							else:

								f='NOD'

								return 'NOD'

	if ycount == -1:
		return 'NOD'
	if str(f).find('NOD') ==-1:
		return cleanpar(f,dvar), dparts
	else:
		return 'NOD', []

def run_it(my_function,hashprefix):
	
	ff = open('images/new/'+hashprefix+'inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')

	ffa = open('landing/static/audio/'+hashprefix+'inputsAudio.ffconcat','w')
	ffa.write('ffconcat version 1.0\n\n')

	ffs = open('images/new/'+hashprefix+'subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')
	ffs.write('1\n')
	ffs.write('00:00:00.500 --> 00:00:04.000\n')
	ffs.write('Integrate\n')
	ffs.close()
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{calc}
	\usepackage{ifthen}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows, positioning}

	\tikzstyle{startstop} = [rectangle, minimum width=6cm, minimum height=1cm,text centered, draw=black, fill=red!30]
	\tikzstyle{process} = [rectangle, rounded corners, minimum width=6.05cm, minimum height=1cm, text centered, text width=6.05cm, draw=black, fill=orange!30]
	\tikzstyle{processlong} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=green!30]
	\tikzstyle{processop} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=orange!30]
	\tikzstyle{processop2} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=blue!30]
	\tikzstyle{processfn} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=red!30]
	\tikzstyle{processbegin} = [rectangle, minimum width=6cm, minimum height=1cm, text centered, text width=6cm, draw=black, fill=green!30]
	\tikzstyle{processred} = [rectangle, minimum width=6cm, minimum height=1cm, text centered, text width=6cm, draw=black, fill=red!30]
	\tikzstyle{decision} = [diamond, minimum width=6cm, minimum height=1cm, text centered, draw=black, fill=green!30]
	\tikzstyle{arrow} = [thick,->,>=stealth]

	\begin{document}
	\LARGE
	'''
	oldstr = ''
	thestr = 'not'
	framen = -1
	dparts = fullintegral(my_function,'x',0,0,0)[1]
	colors = []

	while thestr != oldstr:
		oldstr = thestr
		framen +=1
		dpartsc = copy.deepcopy(dparts)
		
		thestr, duration, color, textstr, latexstr, audiostr = createdisplay(dpartsc,framen,my_function,'x')
		
		if thestr !=oldstr:
			
			
			graphstr = startstr+thestr+'\n'+r'''\end{tikzpicture}
				\end{minipage}'''
			if len(latexstr) > 0:
				for idx, lstr in enumerate(latexstr):
					if isinstance(duration,list):
						framedur = duration[idx]
						colors.append([framedur,color,textstr])
						ffa.write("file 'integral/"+audiostr[idx]+".mp3'\noutpoint 00:00:0"+str(framedur)+"\n\n")
					else:
						framedur = duration
						colors.append([framedur,color,textstr])
						ffa.write("file 'integral/"+audiostr+".mp3'\noutpoint 00:00:0"+str(framedur)+"\n\n")
					f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'int'+str(framen)+'-'+str(idx)+'.tex','w')
					equationstr = r'''
					\begin{minipage}{.375\linewidth}
					\LARGE
					'''
					equationstr +=lstr
					equationstr += r'''
					\end{minipage}'''
					f.write(graphstr+equationstr+r'''
						\end{document}''')
					f.close()
					ff.write("file '"+hashprefix+'int'+str(framen)+'-'+str(idx)+".png'\nduration "+str(framedur+.01)+"\n\n")

					os.system('./outputLatex.sh -c "'+hashprefix+'int'+str(framen)+'-'+str(idx)+'"')
			else:
				colors.append([duration,color,textstr])
				ffa.write("file 'integral/"+audiostr+".mp3'\noutpoint 00:00:0"+str(duration)+"\n\n")
				f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'int'+str(framen)+'.tex','w')
				equationstr = ''
				f.write(graphstr+equationstr+r'''
					\end{document}''')
				f.close()
				ff.write("file '"+hashprefix+'int'+str(framen)+".png'\nduration "+str(duration+.01)+"\n\n")
				os.system('./outputLatex.sh -c "'+hashprefix+'int'+str(framen)+'"')

			
		else:
			ff.write("file '"+hashprefix+'int'+str(framen-1)+".png'\n\n")
	#print(startstr+thestr+'\n'+r'''\end{tikzpicture}\end{document}''')

	ff.close()
	ffa.close()
	os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -f concat -i landing/static/audio/'+hashprefix+'inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 images/new/'+hashprefix+'integral.mp4 -y')
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -pix_fmt yuv420p -preset ultrafast -r 8 images/new/'+hashprefix+'integral.mp4 -y')
	os.system('rm landing/static/audio/'+hashprefix+'inputsAudio.ffconcat')
	jsoncolors = []

	for i in colors:
		jsoncolors.append({'type':i[1],'time':i[0],'text':toJavascript(i[2])})
	return 'new/'+hashprefix+'integral.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
	#os.system('./testintegral2p.py -f "placehere" -o "images/new/'+hashprefix+'ex0.png"')

#run_it('sin(2*x)','azaaz')
def index_fn(inputexpression,dvar):
	fd = fullintegral(inputexpression,dvar,0,0,0)

	return [myslatex(sympy.sympify(fd[0])),myslatex(sympy.sympify(cleanpar(inputexpression,dvar))),0,fd[0]]
#index_fn('sin(2*x)','x')