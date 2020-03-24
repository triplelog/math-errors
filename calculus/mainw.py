
import time
#print time.time()
from sumrulew import sumrulew
from clean import cleanpar
from constantmultiplew import pulloutconstant
from productrulew import productrulew
from powerrulew import powerrulew
from chainrulew import chainrulew
from expologw import expologrulew
from clean import post_clean
from trigrulew import trigrulew
from quorulew import quorulew
from otherw import othertricksw

from sumrule import sumrule
from productrule import productrule
from powerrule import powerrule
from chainrule import chainrule
from expolog import expologrule
from trigrule import trigrule
from quorule import quorule
from other import othertricks

import checkcorrect
import sympy
import os
import sys
#print time.time()


def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))
def inversetrigrulew(inputexpression,dvar):
	#This is unncessary if also remove the uneccsary calls
	return [False,inputexpression]
def needspar(input_string):
	needsapar = False
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
			if i=='+':
				needsapar=True
			if i=='-':
				needsapar=True
			cancel_it = 1
			isbreak = idx
			break
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			if i=='+':
				needsapar=True
			if i=='-':
				needsapar=True
	return needsapar
	if isbreak == len(input_string)-1:
		#don't need parentheses
		return True
	else:
		return False
def fullderivativec(inputexpression,dvar,ycount,idvar,wrongness):
	f = cleanpar(inputexpression,dvar)
	dvar = str(sympy.sympify(dvar))
	nopart = str(cleanpar(inputexpression,dvar))
	#print f, dvar, nopart
	badword = 0
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		if dvar.find(sstr)>-1:
			badword = 1
		nopart=nopart.replace(sstr,'')
	if nopart.find(dvar)==-1 and nopart.find(idvar)==-1:
		if badword==0:
			return '0'
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar,wrongness)

	if h[0]!=1:
		ycount=ycount+1
		f = h[0]+'*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			for idx, i in enumerate(h):
				if idx %2==0:
					##print f, i, h
					f=f+fullderivativec(i,dvar,ycount,idvar,wrongness)
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
			if h[0]:
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrulew(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+fullderivativec(h[2],dvar,ycount,idvar,wrongness)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+fullderivativec(h[2],dvar,ycount,idvar,wrongness)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')-('+h[1]+')*('+fullderivativec(h[2],dvar,ycount,idvar,wrongness)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f='('+h[0]+')*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')+('+h[1]+')*('+fullderivativec(h[0],dvar,ycount,idvar,wrongness)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = fullderivativec(h[2],dvar,ycount,idvar,wrongness)
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												if inside_derivative==int(inside_derivative):
													f='('+h[1]+')*'+str(int(inside_derivative))
												else:
													f='('+h[1]+')*'+str(float(inside_derivative))
										except:
											if inside_derivative.find('+',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											else:
												f = '('+h[1]+')*'+inside_derivative
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											d_arr = fullderivativec(h[1],dvar,ycount,idvar,wrongness)
											f = d_arr
										else:
											f = 'IDK'
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	#print myslatex(sympy.sympify(cleanpar(f,dvar)))
	return cleanpar(f,dvar)

def fullderivative(inputexpression,dvar,ycount,idvar,wrongness,cw):
	f = cleanpar(inputexpression,dvar)
	#print f, dvar
	dvar = str(sympy.sympify(dvar))
	f_arr = []
	#print f, dvar
	nopart = str(cleanpar(inputexpression,dvar))
	#print nopart
	badword = 0
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		nopart=nopart.replace(sstr,'')
		if dvar.find(sstr)>-1:
			badword = 1
	if nopart.find(dvar)==-1 and nopart.find(idvar)==-1:
		if badword == 0:
			return [['0','Correct']]
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar,wrongness)

	if h[0]!=1:
		ycount=ycount+1
		fds = fullderivative(h[1],dvar,ycount,idvar,wrongness,1)
		for fdsi in fds:
			f_arr.append([h[0]+'*('+fdsi[0]+')',fdsi[1]])
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrulew(f,[],dvar,wrongness)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			fd = []
			fdl = []
			for idx, i in enumerate(h):
				fd.append(fullderivative(str(i),dvar,ycount,idvar,wrongness,0))
				fdl.append(len(fd[idx]))

			for ii in range(0,max(fdl)):
				f=''
				error = 'Correct'
				for idx, i in enumerate(h):
					if idx %2==0:
						##print f, i, h
						#print fd, idx
						if len(fd[idx])>ii:
							f=f+fd[idx][ii][0]

							if fd[idx][ii][1]!='Correct':
								error=fd[idx][ii][1]
						else:
							f=f+fd[idx][0][0]
							if fd[idx][0][1]!='Correct':
								error=fd[idx][0][1]
					else:
						if i==0:
							f=f+'+'
						else:
							f=f+'-'
				#print 'fff',f
				f_arr.append([f,error])
		else:
			#Here if cannot use sum rule
			h = powerrulew(f,dvar,idvar,wrongness)
			if h[0]:
				#Here if can use power rule
				if wrongness[3]==1:
					for h1i in h[1]:
						f_arr.append([h1i[0],h1i[1]])
					wrongness[3]=1-cw
				else:
					if wrongness[3]>1:
						wrongness[3]=wrongness[3]-cw
						f=h[1][0][0]
					else:
						f= h[1][0][0]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrulew(f,dvar,wrongness)
				if h[0]:
					if wrongness[4]==1:
						for h1i in h[1]:
							f_arr.append([h1i[0],h1i[1]])
						wrongness[4]=1-cw
					else:
						if wrongness[4]>1:
							wrongness[4]=wrongness[4]-cw
							f=h[1][0][0]
						else:
							f= h[1][0][0]
				else:
					f = h[1]
					h = trigrulew(f,dvar,wrongness)
					if h[0]:
						if wrongness[5]==1:
							for h1i in h[1]:
								f_arr.append([h1i[0],h1i[1]])
							wrongness[5]=1-cw
						else:
							if wrongness[5]>1:
								wrongness[5]=wrongness[5]-cw
								f=h[1][0][0]
							else:
								f= h[1][0][0]
					else:
						f = h[1]
						h = inversetrigrulew(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorulew(f,dvar,wrongness)
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if wrongness[2]==1:
									fd1 = fullderivativec(h[1],dvar,ycount,idvar,wrongness)
									fd2 = fullderivativec(h[2],dvar,ycount,idvar,wrongness)
									f_arr.append(['('+fd1+')/('+fd2+')','Remember the quotient rule. The derivative of <div class="katex_div_il">'+slatex(f)+'</div> is not simply <div class="katex_div_il">'+slatex('('+fd1+')/('+fd2+')')+'</div>.'])
									f_arr.append(['(('+h[2]+')*('+fd1+')-('+h[1]+')*('+fd2+'))/('+h[2]+')','Do not forget to square the denominator when applying the qotient rule.'])
									f_arr.append(['(('+h[1]+')*('+fd2+')-('+h[2]+')*('+fd1+'))/('+h[2]+')^2','Remember the order of the terms in  the numerator of the quotient rule.'])
									f_arr.append(['('+h[2]+')*('+fd1+')-('+h[1]+')*('+fd2+')','Remember the denominator of the quotient rule.'])
									f_arr.append(['(('+h[2]+')*('+fd1+')-('+h[1]+')*('+fd2+'))/('+h[1]+')^2','When applying the quotient rule, divide by the square of the denomiinator not the numerator.'])
									wrongness[2]=1-cw
								else:
									if wrongness[2]>1:
										wrongness[2]=wrongness[2]-cw
									fd1 = fullderivative(h[1],dvar,ycount,idvar,wrongness,1)
									fd2 = fullderivative(h[2],dvar,ycount,idvar,wrongness,1)
									#print len(fd1), len(fd2), h[1], h[2]
									for fd1i in fd1:
										for fd2i in fd2:
											if h[1]=='1':
												f='(-('+fd2i[0]+'))/('+h[2]+')^2'
												error = fd2i[1]
											else:
												f='(('+h[2]+')*('+fd1i[0]+')-('+h[1]+')*('+fd2i[0]+'))/('+h[2]+')^2'
												if fd1i[1] != 'Correct':
													error = fd1i[1]
												elif fd2i[1] != 'Correct':
													error = fd2i[1]
												else:
													error = 'Correct'
											f_arr.append([f,error])
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrulew(f,[],dvar,wrongness)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									if wrongness[0]==1:
										wrongness[0]=1-cw
										f_arr.append(['('+fullderivativec(h[0],dvar,ycount,idvar,wrongness)+')*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')','Remember the product rule. The derivative of <div class="katex_div_il">'+slatex(f)+'</div> is not simply <div class="katex_div_il">'+slatex('('+fullderivativec(h[0],dvar,ycount,idvar,wrongness)+')*('+fullderivativec(h[1],dvar,ycount,idvar,wrongness)+')')+'</div>.'])
									else:
										if wrongness[0]>1:
											wrongness[0]=wrongness[0]-cw
										fd1 = fullderivative(h[1],dvar,ycount,idvar,wrongness,1)
										fd2 = fullderivative(h[0],dvar,ycount,idvar,wrongness,1)
										for fd1i in fd1:
											for fd2i in fd2:
												if fd1i[1] != 'Correct':
													error = fd1i[1]
												elif fd2i[1] != 'Correct':
													error = fd2i[1]
												else:
													error = 'Correct'

												f_arr.append(['('+h[0]+')*('+fd1i[0]+')+('+h[1]+')*('+fd2i[0]+')',error])
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrulew(f,dvar,idvar,wrongness)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = fullderivativec(h[2][1],dvar,ycount,idvar,wrongness)
										inside_derivative_arr = fullderivative(h[2][1],dvar,ycount,idvar,wrongness,1)
										if wrongness[1]==1:
											try:
												if float(inside_derivative)==1:
													f=h[1][0][0]
												elif float(inside_derivative)==0:
													f='0'
												else:
													fd1=float(inside_derivative)
													f_arr.append([h[1][0][0],'While applying the chain rule you did not multiply by the derivative of the inside function. When taking the derivative of <div class="katex_div_il">'+slatex(f)+'</div> remember to multiply by <div class="katex_div_il">'+slatex(inside_derivative)+'</div>.'])
													f_arr.append([fullderivativec(h[2][0]+'('+fd1+')',fd1,ycount,idvar,wrongness),'Chain-Took derivative of inside function on inside'])
													f_arr.append(['('+fullderivativec(h[2][0]+'('+dvar+')',dvar,ycount,idvar,wrongness)+')*('+fd1+')','Chain-Just multiplied derivatives'])
													#print 'here'
													wrongness[1]=1-cw
											except:
												fd1 = fullderivativec(h[2][1],dvar,ycount,idvar,wrongness)
												f_arr.append([h[1][0][0],'While applying the chain rule you did not multiply by the derivative of the inside function. When taking the derivative of <div class="katex_div_il">'+slatex(f)+'</div> remember to multiply by <div class="katex_div_il">'+slatex(inside_derivative)+'</div>.'])
												#print h[2][0]+'('+fd1+')',fd1, fullderivativec(h[2][0]+'('+fd1+')',fd1,ycount,idvar,wrongness)
												f_arr.append([fullderivativec(h[2][0]+'('+fd1+')',fd1,ycount,idvar,wrongness),'Chain-Took derivative of inside function on inside'])
												f_arr.append(['('+fullderivativec(h[2][0]+'('+dvar+')',dvar,ycount,idvar,wrongness)+')*('+fd1+')','Chain-Just multiplied derivatives'])
												#print 'here'
												wrongness[1]=1-cw
										else:

											for idi in inside_derivative_arr:
												try:
													idi[0] = float(idi[0])
													for h1i in h[1]:
														if idi[0]==int(idi[0]):
															f='('+h1i[0]+')*'+str(int(idi[0]))
															if idi[1] != 'Correct':
																error = idi[1]
															elif h1i[1] != 'Correct':
																error = h1i[1]
															else:
																error = 'Correct'
														else:
															f='('+h1i[0]+')*'+str(float(idi[0]))
															if idi[1] != 'Correct':
																error = idi[1]
															elif h1i[1] != 'Correct':
																error = h1i[1]
															else:
																error = 'Correct'
														f_arr.append([f,error])
												except:
													for h1i in h[1]:
														inside_derivative = idi
														if inside_derivative[0].find('+',0)>-1:
															f = '('+h1i[0]+')*('+inside_derivative[0]+')'
														elif inside_derivative[0].find('-',0)>-1:
															f = '('+h1i[0]+')*('+inside_derivative[0]+')'
														else:
															f = '('+h1i[0]+')*'+inside_derivative[0]
														if idi[1] != 'Correct':
															error = idi[1]
														elif h1i[1] != 'Correct':
															error = h1i[1]
														else:
															error = 'Correct'
														f_arr.append([f,error])
											if wrongness[1]>1:
												wrongness[1]=wrongness[1]-cw

									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricksw(f,dvar,wrongness)
										if h[0]:
											ycount =ycount+1
											d_arr = fullderivativec(h[1],dvar,ycount,idvar,wrongness)
											f = d_arr
										else:
											f = 'IDK'
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	#print myslatex(sympy.sympify(cleanpar(f,dvar)))
	if len(f_arr)>0:
		for i in range(0,len(f_arr)):
			f_arr[i][0]=cleanpar(f_arr[i][0],dvar)
		return f_arr
	else:
		return [[cleanpar(f,dvar),'Correct']]





def run_it(inputexpression,hashprefix,dvar,idvar,wrongness0,guess):
	allsteps=[]
	show_all = []
	audio_file = ["We want to find the derivative of this function"]
	all_ordered = []
	previous_stuff = ''
	ycount = 0
	stopnow = 0
	nopart = inputexpression
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		nopart=nopart.replace(sstr,'')
	if nopart.find(dvar) ==-1 and nopart.find(idvar)==-1:
		os.system('./testlm2p.py -f "\$\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(cleanpar(inputexpression,dvar)))+']=0\$" -o "images/new/'+hashprefix+'ex0.png"')
		return [1,myslatex(sympy.sympify('0')),myslatex(sympy.sympify(cleanpar(inputexpression,dvar)))]
	else:
		#print fullderivative(inputexpression,dvar,0,idvar,wrongness0,1)
		fds = fullderivative(inputexpression,dvar,0,idvar,wrongness0,1)
		#print fds
		for i in fds:
			if checkcorrect.checksame(cleanpar(guess,dvar),cleanpar(i[0],dvar),dvar):
				return i[1]
		return 'NoMatch'
		#return [len(all_ordered),myslatex(sympy.sympify(fullderivative(inputexpression,dvar,0,idvar,wrongness0))),myslatex(sympy.sympify(cleanpar(inputexpression,dvar))),audio_file]
def index_fn_w(inputexpression,dvar,idvar,guess):
	tfunction = inputexpression
	ri1 = run_it(tfunction,'asdfsdf','x','y',[0,0,0,0,0,0,0,0,0,0],guess)
	if ri1 == 'NoMatch':
		ri2 = run_it(tfunction,'asdfsdf','x','y',[1,0,0,0,0,0,0,0,0,0],guess)
		if ri2 == 'NoMatch':
			ri3 = run_it(tfunction,'asdfsdf','x','y',[0,1,0,0,0,0,0,0,0,0],guess)
			if ri3 == 'NoMatch':
				ri4 = run_it(tfunction,'asdfsdf','x','y',[0,0,1,0,0,0,0,0,0,0],guess)
				if ri4 == 'NoMatch':
					ri5 = run_it(tfunction,'asdfsdf','x','y',[0,0,0,1,0,0,0,0,0,0],guess)
					if ri5 == 'NoMatch':
						ri6 = run_it(tfunction,'asdfsdf','x','y',[0,0,0,0,1,0,0,0,0,0],guess)
						if ri6 == 'NoMatch':
							ri7 = run_it(tfunction,'asdfsdf','x','y',[0,0,0,0,0,1,0,0,0,0],guess)
							if ri7 == 'NoMatch':
								error = 'No Match Found'
							else:
								error = ri7
						else:
							error = ri6
					else:
						error = ri5
				else:
					error = ri4
			else:
				error = ri3
		else:
			error = ri2
	else:
		error = ri1

	return error

#print(index_fn_w('sin(x)+cos(x)','x','y','sin(x)+cos(x)'))
#print myslatex(sympy.sympify(cleanpar('x^(-2)','x')))
#print index_fn('x^(-2)','x')[1]
#import uuid
#print time.time()

#run_it('sin(ln(x))/x','asdfsdf','x','y',[0,0,0,0,0,0,0,0,0,0],'cos(x^2)/sin(x^2)')
#guess = '-cos(x)/sin(x)'
#tfunction = 'ln(sin(x))'
#print cleanpar('(x)*2^(x-1)','x')
#print index_fn_w('e^(-x)','x','y','1')
#print time.time()

#print sympy.sympify('x^2+1').subs('x',2)
#from sympy import Symbol
#x=Symbol('x',commutative=False)
#inputstr = 'x*1/x+log(x)*1'

#from sympy.core.sympify import kernS
#print myslatex(sympy.sympify(inputstr,evaluate=True))
#print myslatex(sympy.sympify(inputstr,evaluate=False))
#print myslatex(inputstr)
#print 
#if myslatex(sympy.sympify(inputstr,evaluate=True))==myslatex(sympy.sympify(inputstr,evaluate=False)):
#	print "True"
#else:
#	print "False"

