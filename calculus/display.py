
def printrow(darray,darrayseq,allnodes):
	for i in range(0,len(darray)):
		if len(darray[i])==3:
			darray[i][2]=darrayseq+darray[i][1]
			allnodes.append(darray[i])
		else:
			darray[i][2]=darrayseq+darray[i][1]
			darray[i][3],allnodes = printrow(darray[i][3],darray[i][2],allnodes)
			allnodes.append(darray[i][:3])
	return darray,allnodes

def getrounds(darray,n,seq):

	for i in range(0,len(darray)):
		if darray[i][2][:-1]==seq:
			if len(darray[i])>3:
				darray[i][3]=str(n)
			else:
				darray[i].append(str(n))

	for i in range(0,len(darray)):
		if len(darray[i][2])==len(seq)+2:
			if darray[i][2][-1]=='a':
				if darray[i][2][:len(seq)]==seq:
					n,darray=getrounds(darray,n+1,darray[i][2][:len(seq)+1])

	return n,darray

def getnodes(allnodes,maxrounds):
	nodes = []
	for i in range(0,len(allnodes)):
		if int(allnodes[i][3])< maxrounds:
			nodes.append(allnodes[i])
	return nodes

def letterbefore(x):
	allletters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for i in range(1,len(allletters)):
		if allletters[i]==x:
			return allletters[i-1]

	

length_lines = []
base_str = '\\begin{tikzpicture}[node distance=100pt]'
nodes = []
my_function = 'x^3+sin(x)+1/x+sin(3x)'
nodes.append('\\node (dec'+str(len(nodes))+') [processlong] {$\displaystyle\int '+my_function+'$};')


dparts = [['\\displaystyle\\int x^3', 'a', '', [['x^4/4', 'a', '']]], ['+', 'b', ''], ['\\displaystyle\\int sin(x)', 'c', '', [['-cos(x)', 'a', '']]], ['+', 'd', ''], ['\\displaystyle\\int sin(3*x)', 'e', '', [['\\displaystyle\\int sin(u)/3', 'a', '', [['1/(3)', 'a', ''], ['*', 'b', ''], ['\\displaystyle\\int sin(u)', 'c', '', [['-cos(u)', 'a', '']]]]]]], ['+', 'f', ''], ['\\displaystyle\\int 1/x', 'g', '', [['ln|x|', 'a', '']]]]
allnodes = []
print printrow(dparts,'',allnodes)

everynode = getrounds(allnodes,0,'')[1]

maxrounds = 5
allnodes = getnodes(everynode,maxrounds)

unsorted = True
while unsorted:
	unsorted = False
	for i in range(0,len(allnodes)-1):
		if len(allnodes[i][2])>len(allnodes[i+1][2]) or (len(allnodes[i][2])==len(allnodes[i+1][2]) and allnodes[i][2]>allnodes[i+1][2]):
			pholder = allnodes[i]
			allnodes[i]=allnodes[i+1]
			allnodes[i+1]=pholder
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
			allnodes[i][4]=allnodes[ii][1]

pnode = 'dec0'

tot_length = str((7-1)*20)+'pt'
for i in allnodes:
	length_lines.append('\\newlength{\myl'+i[2]+'}\settowidth{\myl'+i[2]+'}{$'+i[0]+'$}')
	#tot_length = tot_length+'+\myl'+i[2]
arrows = []
for i in allnodes:
	if i[2][-1]=='a':
		if len(i[2])>1:
			pnode = i[2][:-1]
		else:
			pnode = '0'
		nodes.append('\\node (dec'+i[2]+') [processlong, below of=dec'+pnode+', xshift=-('+i[1]+')/2+\myl'+i[2]+'/2] {$'+i[0]+'$};')
	else:
		snode = i[2][:-1]+letterbefore(i[2][-1])
		nodes.append('\\node (dec'+i[2]+') [processlong, right of=dec'+snode+', xshift=-80pt+(\myl'+snode+'+\myl'+i[2]+')/2] {$'+i[0]+'$};')
	arrows.append('\draw [arrow] (dec'+pnode+'.south) -- node[anchor=north] {} (dec'+i[2]+'.north);')




for i in length_lines:
	print i
for i in range(0,len(allnodes)):
	if allnodes[len(allnodes)-i-1][4]!='':

		print '\\newlength{\\temp'+allnodes[i][2]+'}\setlength{\\temp'+allnodes[i][2]+'}{'+allnodes[len(allnodes)-i-1][4]+'}'
		print '\ifthenelse{\myl'+allnodes[len(allnodes)-i-1][2]+'<\\temp'+allnodes[i][2]+'}{\def\myl'+allnodes[len(allnodes)-i-1][2]+'{\\temp'+allnodes[i][2]+'}}{}'


print base_str
for i in nodes:
	print i
for i in arrows:
	print i

