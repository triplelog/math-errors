import time
#print time.time()
from sumrule import sumrule
from clean import cleanpar
from constantmultiple import pulloutconstant
from powerrulew import powerrulew
from expologw import expologrulew
from trigrule import trigrule
from usub import usub
from ibp import ibp

import checkcorrect
import sympy
import os
import sys
import random

allletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

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
		return input_string
	for i in range(0,len(input_string)):
		if input_string[i]=='(':
			sindex = i
			break
	for i in range(0,len(input_string)):
		if input_string[i]==')':
			eindex = i
	intf = input_string.find('\int')
	if intf>0:
		return '\displaystyle\int '+slatex(input_string[sindex:eindex+1],input_string[:intf])+'d'+input_string[:intf]
	else:
		return slatex(input_string[sindex:eindex+1],input_string[:sindex])

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
		else:
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
	for i in range(0,len(allnodes)):
		if int(allnodes[i][3])< maxrounds:
			if int(allnodes[i][3])== maxrounds-1:
				recentnode = [len(nodes)]
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

	return nodes, extranodes,recentnode

def letterbefore(x):
	allletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for i in range(1,len(allletters)):
		if allletters[i]==x:
			return allletters[i-1]

def createdisplay(dparts,maxrounds,my_function,dvar):

	length_lines = []
	base_str = '\\begin{tikzpicture}[node distance=100pt]'
	nodes = []
	nodes.append('\\node (dec'+str(len(nodes))+') [processlong] {$\displaystyle\int '+slatex(my_function,dvar)+'d'+dvar+'$};')


	allnodes = []
	lastnode = []
	darray,allnodes,lastnode = printrow(dparts,'',allnodes,lastnode)

	everynode = getrounds(allnodes,0,'')[1]

	nodes0 = ''
	allnodes0 = everynode
	maxsp = 0
	recentnode = []
	while nodes0 != allnodes0:
		nodes0 = allnodes0
		maxsp +=1
		allnodes0,extranodes,recentnode = getnodes(allnodes0,10000,maxsp,lastnode)
	allnodes0,extranodes,recentnode = getnodes(allnodes0,maxrounds,maxsp,lastnode)

	allnodes = allnodes0
	for i in allnodes:

		print i
	extranodes = []
	for i in range(0,len(allnodes)):
		allnodes[i][3]=allnodes[i][1]

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
				unsorted = True
	for i in range(0,len(allnodes)):
		if allnodes[i][2][-1]=='a':
			tot_length = str(-20)+'pt'
			for ii in range(i,len(allnodes)):
				if len(allnodes[ii][2])==len(allnodes[i][2]) and allnodes[ii][2][:-1]==allnodes[i][2][:-1]:
					tot_length += '+20pt+\myl'+allnodes[ii][2]
				else:
					break
			allnodes[i][1]=tot_length
	for i in range(0,len(allnodes)):
		allnodes[i].append('')
		for ii in range(i+1,len(allnodes)):
			if allnodes[ii][2]==allnodes[i][2]+'a':
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
					arrows.append('\draw [arrow] (dec'+maxcode+'.south) -- node[anchor=north] {} (dec'+i[2]+'.north);')
					thisnode=thisnode+maxexp
			i[0]=maxdvar+'('+thisnode+')'
		else:
			if pnode == '':
				pnode = '0'
			arrows.append('\draw [arrow] (dec'+pnode+'.south) -- node[anchor=north] {} (dec'+i[2]+'.north);')
		myexp = getlatex(i[0])
		length_lines.append('\\newlength{\myl'+i[2]+'}\settowidth{\myl'+i[2]+'}{$'+myexp+'$}')
		if i[2][-1]=='a':
			if len(i[2])>1:
				pnode = i[2][:-len(i[3])]
			else:
				pnode = '0'
			if pnode =='':
				pnode = '0'

			if idx in recentnode:		
				nodes.append('\\node (dec'+i[2]+') [processop, below of=dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2, yshift=-'+str(-100+100*len(i[3]))+'pt ] {$'+myexp+'$};')
			else:
				nodes.append('\\node (dec'+i[2]+') [processlong, below of=dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2, yshift=-'+str(-100+100*len(i[3]))+'pt ] {$'+myexp+'$};')
		else:
			snode = i[2][:-1]+letterbefore(i[2][-1])
			if idx in recentnode:
				nodes.append('\\node (dec'+i[2]+') [processop, right of=dec'+snode+', xshift=-80pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+myexp+'$};')
			else:
				nodes.append('\\node (dec'+i[2]+') [processlong, right of=dec'+snode+', xshift=-80pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+myexp+'$};')
		
		

	for i in length_lines:
		print i
	for i in range(0,len(allnodes)):
		if allnodes[len(allnodes)-i-1][5]!='':

			print '\\newlength{\\temp'+allnodes[i][2]+'}\setlength{\\temp'+allnodes[i][2]+'}{'+allnodes[len(allnodes)-i-1][5]+'}'
			print '\ifthenelse{\myl'+allnodes[len(allnodes)-i-1][2]+'<\\temp'+allnodes[i][2]+'}{\def\myl'+allnodes[len(allnodes)-i-1][2]+'{\\temp'+allnodes[i][2]+'}}{}'


	print base_str
	for i in nodes:
		print i


	for i in arrows:
		print i


def fullintegralw(inputexpression,dvar,ycount,wrongness,tryudv):
	f = cleanpar(inputexpression,dvar)
	dparts = []
	dvar = str(sympy.sympify(dvar))
	nopart = str(cleanpar(inputexpression,dvar))
	#print f, dvar, nopart
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
			
			return fintegral, dparts
	##print slatex(f)
	h = pulloutconstant(f,dvar)


	if h[0]!=1:
		ycount=ycount+1
		print "Pull out the constant multiple", f
		return_integral = fullintegralw(h[1],dvar,ycount,wrongness,tryudv)
		f = h[0]+'*('+return_integral[0]+')'
		dparts = [[dvar+'('+h[0]+')','a',''],['*','b',''],[dvar+'\int('+h[1]+')','c','',return_integral[1]]]

	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			dparts = []
			##print h
			for idx, i in enumerate(h):
				nletter = allletters[idx]
				if idx %2==0:
					##print f, i, h
					print 'break up the sums', f
					return_integral = fullintegralw(i,dvar,ycount,wrongness,tryudv)
					f=f+return_integral[0]
					dparts.append([dvar+'\int('+i+')',nletter,'',return_integral[1]])
				else:
					if i==0:
						f=f+'+'
						dparts.append(['+',nletter,''])
					else:
						f=f+'-'
						dparts.append(['-',nletter,''])
		else:
			#print f
			h = powerrulew(f,dvar)
			if h[0]:
				randx = random.random()
				idx = 0
				sumx = 0
				for i in range(0,len(h[1])):
					sumx += h[1][i][2]
					if randx < sumx:
						idx = i
						break
				print 'Apply the Power Rule', f
				f = h[1][idx][0]
				dparts = [[dvar+'('+h[1][idx][0]+')','a','']]
			else:
				h=expologrulew(f,dvar)
				if h[0]:
					randx = random.random()
					idx = 0
					sumx = 0
					for i in range(0,len(h[1])):
						sumx += h[1][i][2]
						if randx < sumx:
							idx = i
							break
					print h[2]
					f=h[1][idx][0]
					dparts = [[dvar+'('+h[1][idx][0]+')','a','']]
				else:
					h=trigrule(f,dvar)
					if h[0]:
						print h[2]
						f=h[1]
						dparts = [[dvar+'('+h[1]+')','a','']]
					else:
						h=usub(f,dvar)
						if h[0]:
							print 'Apply u-substitution', f, h
							return_integral = fullintegralw(h[1],'u',ycount,wrongness,tryudv)
							f=return_integral[0].replace('u',h[2])
							fulli = return_integral[1]
							print fulli
							fulli.append([slatex(f,dvar),'usub',dvar+'('+f+')'])
							dparts = [['u'+'\int('+h[1]+')','a','',fulli]]
						else:
							if tryudv < 3:
								h=ibp(f,dvar)
								tryudv=tryudv+1
								if h[0]:
									foundudv = 0
									for iu in h[1]:
										#print iu
										u=iu[1]
										du=iu[3]
										dv=iu[4]
										try:
											return_integral = fullintegralw(dv,dvar,ycount,wrongness,3)
											v=return_integral[0] # change if want double ibp

											#print 'vvv', dv, v
											if str(v) != 'NOD':
												if sympy.sympify('('+str(v)+')*('+str(du)+')')!=sympy.sympify(f):
													#print 'what', '('+str(v)+')*('+str(du)+')', u, v, du, dv
													return_integral = fullintegralw('('+str(v)+')*('+str(du)+')',dvar,ycount,wrongness,tryudv)
													tfi = return_integral[0] # change if want double ibp
													#print 'tfi', tfi
													if sympy.sympify('('+str(u)+')*('+str(v)+')-('+str(tfi)+')')!=sympy.sympify(f):
														if str(tfi) != 'NOD':
															#tryudv =tryudv+1
															#print tfi, u, v, du, dv, f, '('+str(u)+')*('+str(v)+')-('+str(tfi)+')'

															f='('+str(u)+')*('+str(v)+')-('+str(tfi)+')'
															fulli = return_integral[1]
															dparts = [[dvar+'('+str(u)+')','a',''],['*','b',''],[dvar+'('+str(v)+')','c',''],['-','d',''],[dvar+'\int('+'('+str(v)+')*('+str(du)+')'+')','e','',fulli]]
															print 'Apply integration by parts',f, u, v, du, dv
															foundudv = 1
															#print inputexpression, ycount
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


	if str(f).find('NOD') ==-1:
		return cleanpar(f,dvar), dparts
	else:
		return 'NOD', []

input_fn = 'ln(x)'
output_fn = sys.argv[2]
dvar = 'x'
for iruns in range(0,100):
	return_integral = fullintegralw(input_fn,'x',0,[1],0)
	if checkcorrect.checksame(cleanpar(output_fn,dvar),cleanpar(return_integral[0],dvar),dvar):
		print 'MATCH',return_integral[0], output_fn
		dparts = return_integral[1]
		print dparts
		break

createdisplay(dparts,7,sys.argv[1],'x')