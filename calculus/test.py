#from clean import cleanpar
#from main import fullderivative_y
#from sumrule import sumrule
#import time

def solve_for_dydx(my_question):
	equal_index = my_question.find('=')
	lhs = my_question[:equal_index]
	rhs = my_question[equal_index+1:]
	lhs = cleanpar(lhs,'x')
	lhs = cleanpar(lhs,'y')
	rhs = cleanpar(rhs,'x')
	rhs = cleanpar(rhs,'y')

	ycount = []
	for i in range(0,38):
		ycount.append(0)
	fdsl = fullderivative_y(lhs,'x',ycount,'y')
	ycount = fdsl[1]
	ycount_intl = ''
	for i in range(0,38):
		ycount_intl = ycount_intl+str(ycount[i])
	fdsl = fdsl[0]

	ycount = []
	for i in range(0,38):
		ycount.append(0)
	fdsr = fullderivative_y(rhs,'x',ycount,'y')
	ycount = fdsr[1]
	ycount_intr = ''
	for i in range(0,38):
		ycount_intr = ycount_intr+str(ycount[i])
	fdsr = fdsr[0]

	lhsbreak = sumrule(fdsl,[],'x')

	rightstring=''
	leftstring =''
	if len(lhsbreak) >1:
		for idx, ih in enumerate(lhsbreak):
			if idx%2==0:
				if ih.find('holdfordydx')==-1:
					if idx>0:
						if lhsbreak[idx-1]==0:
							rightstring = rightstring+'-'+ih
						else:
							rightstring = rightstring+'+'+ih
					else:
						rightstring = rightstring+'-'+ih
				else:
					if idx>0:
						if lhsbreak[idx-1]==0:
							leftstring=leftstring+'+'+ih
						else:
							leftstring=leftstring+'-'+ih

					else:
						leftstring=leftstring+ih
	else:
		leftstring=lhsbreak[0]

	rhsbreak = sumrule(fdsr,[],'x')
	rightstringr=''
	leftstringr =''
	if len(rhsbreak) >1:
		for idx, ih in enumerate(rhsbreak):
			if idx%2==0:
				if ih.find('holdfordydx')>-1:
					if idx>0:
						if rhsbreak[idx-1]==0:
							leftstringr = leftstringr+'-'+ih
						else:
							leftstringr = leftstringr+'+'+ih
					else:
						leftstringr = leftstringr+'-'+ih
				else:
					if idx>0:
						if rhsbreak[idx-1]==0:
							rightstringr=rightstringr+'+'+ih
						else:
							rightstringr=rightstringr+'-'+ih

					else:
						rightstringr=rightstringr+ih
	else:
		rightstringr=rhsbreak[0]
	lhs=leftstring+leftstringr
	rhs=rightstring+rightstringr
	if len(lhs)>0:
		if lhs[0]=='+':
			lhs=lhs[1:]
	if len(rhs)>0:
		if rhs[0]=='+':
			rhs=rhs[1:]
	lhs.replace('+-','-')
	lhs.replace('--','+')
	rhs.replace('+-','-')
	rhs.replace('--','+')

	dby = lhs.replace('holdfordydx*','').replace('holdfordydx','1')
	return '('+rhs+')/('+dby+')'
#from checkcorrect import checksame
import urllib.parse
my_question = 'y=(e^x+8)^(7)'
#fds = solve_for_dydx(my_question)
#c_fds = cleanpar(fds,'x')
#c_my_answer = cleanpar('7(e^x+8)^6e^x','x')
#print(checksame(c_my_answer,c_fds,'x'))
my_function= {'var':'x','q':my_question}
my_function = urllib.parse.urlencode(my_function)
print(my_function)