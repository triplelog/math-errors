
import time
#print time.time()
from sumrule import sumrule
from clean import cleanpar
from constantmultiple import pulloutconstant
from productrule import productrule
from powerrule import powerrule
from chainrule import chainrule
from expolog import expologrule
from clean import post_clean
from trigrule import trigrule
from quorule import quorule
from other import othertricks
import sympy
import os
import sys
#print time.time()



def slatex(f):
	return sympy.latex(sympy.sympify(post_clean(f)))
def inversetrigrule(inputexpression,dvar):
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
def derivative(inputexpression,dvar,ycount,allsteps):
	ofunction = cleanpar(inputexpression,dvar)
	##print ofunction
	allsteps.append([ycount, '\\frac{d}{dx}['+sympy.latex(sympy.sympify(ofunction))+']=',ofunction])
	f = cleanpar(inputexpression,dvar)
	###print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		ycount=ycount+1
		d_arr = derivative(h[1],dvar,ycount,allsteps)
		allsteps = d_arr[1]
		f = h[0]+'*('+d_arr[0]+')'
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
					d_arr = derivative(i,dvar,ycount,allsteps)
					allsteps=d_arr[1]
					f=f+d_arr[0]
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
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
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								
								
								
								
								if h[1]=='1'+'sss':
									d_arr = derivative(h[2],dvar,ycount,allsteps)
									f='(-('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr[1]
								elif h[1]==dvar+'sss':
									d_arr = derivative(h[2],dvar,ycount,allsteps)
									f='(('+h[2]+')-('+h[1]+')*('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr[1]
								elif h[2]==dvar+'sss':
									d_arr1 = derivative(h[1],dvar,ycount,allsteps)
									f='(('+h[2]+')*('+d_arr1[0]+')-('+h[1]+'))/('+h[2]+')^2'
									allsteps=d_arr1[1]
								else:
									d_arr1 = derivative(h[1],dvar,ycount,allsteps)
									d_arr = derivative(h[2],dvar,ycount,allsteps)
									f='(('+h[2]+')*('+d_arr1[0]+')-('+h[1]+')*('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr1[1]
									allsteps=d_arr[1]
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if product Rule
									ycount =ycount+1
									d_arr = derivative(h[1],dvar,ycount,allsteps)
									allsteps=d_arr[1]
									d_arr0 = derivative(h[0],dvar,ycount,allsteps)
									allsteps=d_arr0[1]
									f=h[0]+'*('+d_arr[0]+')+'+h[1]+'*('+d_arr0[0]+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										d_arr = derivative(h[2],dvar,ycount,allsteps)
										
										inside_derivative = d_arr[0]
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												allsteps=d_arr[1]
												if inside_derivative==int(inside_derivative):
													f=h[1]+'*'+str(int(inside_derivative))
												else:
													f=h[1]+'*'+str(float(inside_derivative))
										except:
											allsteps=d_arr[1]
											if inside_derivative.find('+',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											else:
												f = h[1]+'*'+inside_derivative
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											d_arr = derivative(h[1],dvar,ycount,allsteps)
											allsteps=d_arr[1]
											f = d_arr[0]
										else:
											f = h[1]
	##print f
	##print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	return [cleanpar(f,dvar),allsteps]

def fullderivative(inputexpression,dvar,ycount):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		ycount=ycount+1
		f = h[0]+'*('+fullderivative(h[1],dvar,ycount)+')'
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
					f=f+fullderivative(i,dvar,ycount)
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
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
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+fullderivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount)+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+fullderivative(h[1],dvar,ycount)+')+'+h[1]+'*('+fullderivative(h[0],dvar,ycount)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = fullderivative(h[2],dvar,ycount)
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												if inside_derivative==int(inside_derivative):
													f=h[1]+'*'+str(int(inside_derivative))
												else:
													f=h[1]+'*'+str(float(inside_derivative))
										except:
											if inside_derivative.find('+',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											else:
												f = h[1]+'*'+inside_derivative
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											d_arr = fullderivative(h[1],dvar,ycount)
											f = d_arr
										else:
											f = h[1]
	##print f
	##print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	#print sympy.latex(sympy.sympify(cleanpar(f,dvar)))
	return cleanpar(f,dvar)
def laststepderivative(inputexpression,dvar,ycount):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		f = sympy.latex(sympy.sympify(h[0]))+'*(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[1],dvar,0)))+'})'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			colors = ['red','blue','magenta','red','blue','magenta','black']
			n_c = -1
			for idx, i in enumerate(h):
				if idx %2==0:
					n_c=n_c+1
					if n_c >= len(colors):
						n_c=len(colors)-1
					##print f, i, h
					f=f+'\mathcolor{'+colors[n_c]+'}{'+sympy.latex(sympy.sympify(fullderivative(i,dvar,0)))+'}'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
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
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1'+'sss':
									f='\\frac{-(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[2],dvar,0)))+'})}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								elif h[1]==dvar+'sss':
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')-('+sympy.latex(sympy.sympify(h[1]))+')*(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[2],dvar,0)))+'})}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								elif h[2]==dvar+'sss':
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')*(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[1],dvar,0)))+'})-('+sympy.latex(sympy.sympify(h[1]))+')}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								else:
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')*(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[1],dvar,0)))+'})-('+sympy.latex(sympy.sympify(h[1]))+')*(\mathcolor{blue}{'+sympy.latex(sympy.sympify(fullderivative(h[2],dvar,0)))+'})}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f0 = sympy.latex(sympy.sympify(h[0]))
									f1 = '\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[1],dvar,0)))+'}'
									f2 = sympy.latex(sympy.sympify(h[1]))
									f3 = '\mathcolor{blue}{'+sympy.latex(sympy.sympify(fullderivative(h[0],dvar,0)))+'}'
									if needspar(f0):
										f0 = '('+f0+')'
									if needspar(f1):
										f1 = '('+f1+')'
									if needspar(f2):
										f2 = '('+f2+')'
									if needspar(f3):
										f3 = '('+f3+')'

										
									f=f0+'*'+f1+'+'+f2+'*'+f3
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										
										f=sympy.latex(sympy.sympify(h[1]))+'*(\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[2],dvar,0)))+'})'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											f = '\mathcolor{red}{'+sympy.latex(sympy.sympify(fullderivative(h[1],dvar,0)))+'}'
										else:
											f = h[1]
	##print f
	##print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return f

def onestepderivative(inputexpression,dvar,ycount):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		f = sympy.latex(sympy.sympify(h[0]))+'*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[1]))+']}'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			colors = ['red','blue','magenta','red','blue','magenta','black']
			n_c = -1
			for idx, i in enumerate(h):
				if idx %2==0:
					n_c =n_c+1
					if n_c >= len(colors):
						n_c=len(colors)-1
					##print f, i, h
					f=f+'\\mathcolor{'+colors[n_c]+'}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(i))+']}'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
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
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1'+'sss':
									f='\\frac{-'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[2]))+']}}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								elif h[1]==dvar+'sss':
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')-('+sympy.latex(sympy.sympify(h[1]))+')*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[2]))+']}}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								elif h[2]==dvar+'sss':
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[1]))+']}-('+sympy.latex(sympy.sympify(h[1]))+')}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
								else:
									f='\\frac{('+sympy.latex(sympy.sympify(h[2]))+')*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[1]))+']}-('+sympy.latex(sympy.sympify(h[1]))+')*'+'\\mathcolor{blue}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[2]))+']}}{('+sympy.latex(sympy.sympify(h[2]))+')^2}'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if product Rule
									ycount =ycount+1
									f=sympy.latex(sympy.sympify(h[0]))+'*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[1]))+']}+'+sympy.latex(sympy.sympify(h[1]))+'*'+'\\mathcolor{blue}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[0]))+']}'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										
										f=sympy.latex(sympy.sympify(h[1]))+'*'+'\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[2]))+']}'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											f = '\\mathcolor{red}{\\frac{d}{dx}['+sympy.latex(sympy.sympify(h[1]))+']}'
										else:
											f = h[1]
	##print f
	##print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return f

def audioonestep(inputexpression,dvar,ycount):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		audio = "Pull out the constant"
		f = h[0]+'*('+'\\frac{d}{dx}('+h[1]+'))'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			audio = "Apply the Sum Rule"
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			for idx, i in enumerate(h):
				if idx %2==0:
					##print f, i, h
					f=f+'\\frac{d}{dx}('+i+')'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
			if h[0]:
				audio = "Apply the Power Rule"
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					audio = "Apply the Exponential Rule"
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						audio = "Apply the Trig Rule"
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrule(f,dvar)
						if h[0]:
							audio = "Apply the Inverse Trig Rule"
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								audio = "Apply the Quotient Rule"
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+'\\frac{d}{dx}('+h[1]+')'+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+'\\frac{d}{dx}('+h[1]+')'+')-('+h[1]+')*('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									audio = "Apply the Product Rule"
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+'\\frac{d}{dx}('+h[1]+')'+')+'+h[1]+'*('+'\\frac{d}{dx}('+h[0]+')'+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										audio = "Apply the Chain Rule"
										#Here if chain rule works
										ycount =ycount+1
										
										f=h[1]+'*'+'\\frac{d}{dx}('+h[2]+')'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											audio = "Apply the special rule!"
											ycount =ycount+1
											f = '\\frac{d}{dx}('+sympy.latex(sympy.sympify(h[1]))+')'
										else:
											audio = "I don't know what to do"
											f = h[1]
	##print f
	##print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return audio




def allof(show_all):
	mystr = ''
	for i in show_all:
		mystr=mystr+i
	return mystr

def solve_steps(allsteps,solveid,show_children,dvar,show_all,audio_file,all_ordered,previous_stuff):
	##print solveid, 'xxxxx'
	#print solveid
	#print allsteps
	colors = ['red','blue','magenta','red','blue','magenta','black']
	#print time.time()
	for idx,i in enumerate(show_all):
		for ii in colors:
			i=i.replace('athcolor{'+ii+'}','athcolor{black}')
		show_all[idx]=i
	if allsteps[0][3]=='solved':
		show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+sympy.latex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0)))+'$'
		audio_file.append(audioonestep(allsteps[0][2],dvar,0))
		#print allof(show_all)+'\\newpage '
		all_ordered.append(allof(show_all)+'\\newpage ')
	if allsteps[solveid][3]!='solved':
		tstring = '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0)+'$'
		if show_all[solveid]!= tstring:
			for ii in colors:
				tstring=tstring.replace('athcolor{'+ii+'}','athcolor{black}')
			if show_all[solveid]!= tstring:
				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0)+'$'
				audio_file.append(audioonestep(allsteps[solveid][2],dvar,0))
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
	level = allsteps[solveid][0]
	rangemin= solveid+1
	if allsteps[solveid][4] !="":
		rangemax = allsteps[solveid][4]
	else:
		rangemax=len(allsteps)
	run_this = 0
	
	for i in allsteps[rangemin:rangemax]:
		if i[3]=="not":
			run_this=1
	if run_this ==1:
		has_d = 0
		dvis=[]
		##print 'h'
		n_c=-1
		
		for idx,i in enumerate(allsteps[rangemin:rangemax]):
			if i[0]==level+1:
				n_c=n_c+1
				if n_c < len(colors):
					the_color = colors[n_c]
				else:
					the_color = 'black'
				if i[3]=="solved":
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
					audio_file.append('We need to find the derivative of the this part')
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0),evaluate=False))+'$'
					audio_file.append(audioonestep(i[2],dvar,0))
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					if sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0),evaluate=False)).replace(' ','') != sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0),evaluate=True)).replace(' ',''):
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0),evaluate=True))+'$'
						audio_file.append('Simplify')
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
				else:
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
					audio_file.append('We need to find the derivative of the this part')
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					
				
		solve_steps(allsteps,allsteps[solveid][5][0],1,dvar,show_all,audio_file,all_ordered,previous_stuff)


	else:
		##print 'j'
		if allsteps[solveid][3]!="solved":
			if show_children==1:
				n_c = -1
				for idx,i in enumerate(allsteps[rangemin:rangemax]):
					if i[0]==level+1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
						audio_file.append('We need to find the derivative of the this part')
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0),evaluate=True))+'$'
						audio_file.append(audioonestep(i[2],dvar,0))
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
			allsteps[solveid][3]="solved"
			n_c=-1
			needtorecolor=False
			for idx,i in enumerate(allsteps[rangemin:rangemax]):
				if i[0]==level+1:
					n_c=n_c+1
					if n_c < len(colors):
						the_color = colors[n_c]
					else:
						the_color = 'black'
					if show_all[idx+rangemin].find('athcolor{'+the_color+'}',0)== -1:
						needtorecolor=True
			if needtorecolor:
				n_c=-1
				for idx,i in enumerate(allsteps[rangemin:rangemax]):
					if i[0]==level+1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{black}','athcolor{'+the_color+'}')

						for ii in colors:
							show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
						show_all[idx+rangemin]='\mathcolor{'+the_color+'}{'+show_all[idx+rangemin]+'}'
						#print "here",solveid, show_all[idx+rangemin]

				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0)+'$'
				audio_file.append("We're going to substitute this in")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
			
			show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+laststepderivative(allsteps[solveid][2],dvar,0)+'$'
			audio_file.append("Combine those steps to get this")
			#print allof(show_all)+'\\newpage '
			all_ordered.append(allof(show_all)+'\\newpage ')
			for idx,i in enumerate(show_all):
				for ii in colors:
					i=i.replace('athcolor{'+ii+'}','athcolor{black}')
				show_all[idx]=i
			#n_c=-1
			#for idx,i in enumerate(allsteps[rangemin:rangemax]):
			#	if i[0]==level+1:
			#		n_c=n_c+1
			#		if n_c < len(colors):
			#			the_color = colors[n_c]
			#		else:
			#			the_color = 'black'
			#		show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{black}','athcolor{'+the_color+'}')
#
#					for ii in colors:
#						show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
#					show_all[idx+rangemin]='\mathcolor{'+the_color+'}{'+show_all[idx+rangemin]+'}'

			if laststepderivative(allsteps[solveid][2],dvar,0).replace(' ','') != sympy.latex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0),evaluate=True)).replace(' ',''):
				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+sympy.latex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0),evaluate=True))+'$'
				audio_file.append("Simplify")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')

		if allsteps[solveid][6]!='':
			solve_steps(allsteps,allsteps[solveid][6],1,dvar,show_all,audio_file,all_ordered,previous_stuff)
		else:
			if allsteps[solveid][7]!=0:
				if solveid !=0:
					solve_steps(allsteps,allsteps[solveid][7],0,dvar,show_all,audio_file,all_ordered,previous_stuff)
			else:
				n_c=-1
				for idx,i in enumerate(allsteps):
					if i[0]==1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx]=show_all[idx].replace('athcolor{black}','athcolor{'+the_color+'}')

						for ii in colors:
							show_all[idx]=show_all[idx].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
						show_all[idx]='\mathcolor{'+the_color+'}{'+show_all[idx]+'}'
						#print "here",solveid, show_all[idx+rangemin]

				show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+onestepderivative(allsteps[0][2],dvar,0)+'$'
				audio_file.append("We're going to substitute this in")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')

				show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+laststepderivative(allsteps[0][2],dvar,0)+'$'
				audio_file.append("And finally we arrive at our derivative!")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
				n_c=-1
				for idx,i in enumerate(allsteps):
					if i[0]==1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx]=show_all[idx].replace('athcolor{black}','athcolor{black}')

						for ii in colors:
							show_all[idx]=show_all[idx].replace('athcolor{'+ii+'}','athcolor{black}')
						show_all[idx]='\mathcolor{black}{'+show_all[idx]+'}'
				if laststepderivative(allsteps[0][2],dvar,0).replace(' ','') != sympy.latex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0),evaluate=True)).replace(' ',''):
					#print sympy.latex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0),evaluate=True))
					#print laststepderivative(allsteps[0][2],dvar,0)
					show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+sympy.latex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0),evaluate=True))+'$'
					audio_file.append("Simplify")
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')



def run_it(inputexpression,hashprefix):
	allsteps=[]
	show_all = []
	audio_file = ["We want to find the derivative of this function"]
	all_ordered = []
	previous_stuff = ''
	
	dvar = 'x'
	ycount = 0
	stopnow = 0
	
	#print time.time(), "A"
	the_derivative_arr = derivative(inputexpression,dvar,0,allsteps)
	#print time.time(), 'B'
	the_derivative = the_derivative_arr[0]
	allsteps=the_derivative_arr[1]
	#print sympy.latex(sympy.sympify(the_derivative))
	for i in allsteps:
		##print i
		my_str = ''
		for ii in range(0,i[0]):
			my_str=my_str+'   '
		##print my_str+i[1]+onestepderivative(i[2],dvar,0)

	for idx,i in enumerate(allsteps):
		if onestepderivative(i[2],dvar,0).find('\\frac{d}{dx}',0)==-1:
			i.append('solved')
		else:
			i.append("not")
		i.append("")
		i.append([])
		i.append("")
		i.append("")
		for iidx,ii in enumerate(allsteps[idx+1:]):
			if ii[0]==i[0]+1:
				i[5].append(idx+iidx+1)
			if ii[0]==i[0]:
				i[6]=idx+iidx+1
				i[4]=idx+iidx+1
				break
			if ii[0]<i[0]:
				i[4]=idx+iidx+1
				break
		for iidx,ii in enumerate(allsteps[:idx]):
			if ii[0]<i[0]:
				i[7]=iidx



	#print time.time(), 'C'
	numruns = 0
	##print "let's see"
	for i in allsteps:
		show_all.append(' \\newline ')

	previous_stuff = '$'+allsteps[0][1]+'$\\newline $'
	show_all[0]='$'+allsteps[0][1]+'$'
	#print allof(show_all)+'\\newpage '
	#print time.time(), 'D'
	all_ordered.append(allof(show_all)+'\\newpage ')
	#print time.time(), 'E'
	##print '$'+allsteps[0][1]+'$\\newpage '
	

	solve_steps(allsteps,0,1,dvar,show_all,audio_file,all_ordered,previous_stuff)
	#print time.time(), 'F'

	#print audio_file
	##print all_ordered
	##print './testlm2p.py -f "'+all_ordered[0]+'" -o "ex1"'
	#myteststr = '$\\hspace*{0em} d[2 \\left(2 x + 2\\right)^{5} + \\log{\\left (x \\right )}]=x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x$'
	#os.system('./testlm2p.py -f "'+myteststr+'" -o "ex'+str(111)+'"')
	#return_str = ''
	#print "working"
	#print allsteps
	#print asdfsdh
	for i in range(0,len(all_ordered)):
		#print time.time()
		#print './testlm2p.py -f "'+all_ordered[i]+'" -o "images/ex'+str(i)+'"\n'
		if all_ordered[i][0:9]=='\\newline ':
			all_ordered[i]=all_ordered[i][9:]
		os.system('./testlm2p.py -f "'+all_ordered[i]+'" -o "images/new/'+hashprefix+'ex'+str(i)+'.png"')
		#print all_ordered[i]
		#os.system('espeak "'+audio_file[i]+'" --stdout > images/audio/'+hashprefix+'ex'+str(i)+'.mp3')
		#print audio_file[i]
	##print previous_stuff
	#print time.time(), 'G'
	tstr = []
	tstr.append(len(all_ordered))
	tstr.append(inputexpression)
	return [tstr,sympy.latex(sympy.sympify(fullderivative(inputexpression,dvar,0))),sympy.latex(sympy.sympify(cleanpar(inputexpression,dvar)))]
def index_fn(inputexpression,dvar):
	return [sympy.latex(sympy.sympify(fullderivative(inputexpression,dvar,0))),sympy.latex(sympy.sympify(cleanpar(inputexpression,dvar)))]




#import uuid
my_fs = []
my_fs.append(run_it('-2x^3+3x^2','worksheet1/f1')[0])
my_fs.append(run_it('3x^(-2)','worksheet1/f2')[0])
my_fs.append(run_it('5(x+1)^(1/3)','worksheet1/f3')[0])
my_fs.append(run_it('x^2+5x-11','worksheet1/f4')[0])
my_fs.append(run_it('2x^6+4x^3-3x+5','worksheet1/f5')[0])
my_fs.append(run_it('x^5+5/x','worksheet1/f6')[0])
my_fs.append(run_it('2sin(x^2+1)','worksheet1/f7')[0])
my_fs.append(run_it('ln(x)+1/x','worksheet1/f8')[0])
my_fs.append(run_it('xln(x)-x','worksheet1/f9')[0])
my_fs.append(run_it('e^x+x^e','worksheet1/f10')[0])
my_fs.append(run_it('e^(x^3+1)','worksheet1/f11')[0])
my_fs.append(run_it('cos(x)/x','worksheet1/f12')[0])
print(my_fs)
#print time.time(), 'H'
#print run_it('x^x',str(uuid.uuid4()))[1]
#run_it('x^2+1')
#from sympy import Symbol
#x=Symbol('x',commutative=False)
#inputstr = 'x*1/x+log(x)*1'

#from sympy.core.sympify import kernS
#print sympy.latex(sympy.sympify(inputstr,evaluate=True))
#print sympy.latex(sympy.sympify(inputstr,evaluate=False))
#print sympy.latex(inputstr)
#print 
#if sympy.latex(sympy.sympify(inputstr,evaluate=True))==sympy.latex(sympy.sympify(inputstr,evaluate=False)):
#	print "True"
#else:
#	print "False"

