import sympy
from sympy import *
from sympy.abc import x
import sys
import os

def tstamp(the_time):
	if the_time < 10:
		return '00:0'+str(the_time)
	elif the_time < 60:
		return '00:'+str(the_time)
	elif the_time < 70:
		return '01:0'+str(the_time - 60)
	elif the_time < 120:
		return '01:'+str(the_time - 60)
	elif the_time < 180:
		return '02:'+str(the_time - 120)
	elif the_time < 240:
		return '03:'+str(the_time - 180)
	elif the_time < 300:
		return '04:'+str(the_time - 240)
	elif the_time < 360:
		return '05:'+str(the_time - 300)
def toJavascript(input_string):
	input_string = input_string.replace('\\','\\\\')
	#input_string = input_string.replace(r'$',r'')
	input_string = r'\\text{'+input_string+'}'

	return input_string

def getTrigValue(fntype,numersign,numerpi,denom):
	if fntype == 'sin':
		if denom == 6:
			if (numersign == '-' and numerpi == 1) or (numersign == '' and numerpi == 0):
				return r'\frac{1}{2}'
			else:
				return r'\frac{-1}{2}'
		elif denom == 4:
			if (numersign == '-' and numerpi == 1) or (numersign == '' and numerpi == 0):
				return r'\frac{\sqrt{2}}{2}'
			else:
				return r'\frac{-\sqrt{2}}{2}'
		elif denom == 3:
			if (numersign == '-' and numerpi == 1) or (numersign == '' and numerpi == 0):
				return r'\frac{\sqrt{3}}{2}'
			else:
				return r'\frac{-\sqrt{3}}{2}'
		elif denom == 2:
			if (numersign == '-' and numerpi == 1) or (numersign == '' and numerpi == 0):
				return r'1'
			else:
				return r'-1'
		elif denom == 1:
			return r'0'
	return '0'
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x
    
def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval

def gettrig(fn):
	reddeg = [False,False]
	fntype = "unk"
	if fn[:3] == 'sin':
		fntype = "sin"
	elif fn[:3] == 'cos':
		fntype = "cos"
	elif fn[:3] == 'tan':
		fntype = "tan"
	elif fn[:3] == 'cot':
		fntype = "cot"
	elif fn[:3] == 'sec':
		fntype = "sec"
	elif fn[:3] == 'csc':
		fntype = "csc"
	

	if fntype != "unk" and len(fn) > 4:
		insidefn = "unk"
		if fn[3] =='(' and fn[-1] == ')' and len(fn)>5:
			insidefn = fn[4:-1]
		elif fn[3] !='(':
			insidefn = fn[3:]
	numer = "unk"
	denom = "unk"
	if insidefn != "unk":
		if insidefn == "0":
			numer = 0
			denom = 1
			return fntype,numer,denom,reddeg
		if insidefn[-2:] == 'pi':
			try:
				numer = int(insidefn[:-2])
				denom = 1
			except:
				if len(insidefn) == 2:
					numer = 1
					denom = 1
				else:
					numer = "unk"
					denom = 1
			return fntype,numer,denom,reddeg
		indexpi = (insidefn.lower()).find('pi/')
		if indexpi > 0:
			try:
				numer = int(insidefn[:indexpi])
				denom = int(insidefn[indexpi+3:])
			except:
				numer = "unk"
				denom = "unk"
			return fntype,numer,denom,reddeg
		elif indexpi == 0:
			try:
				numer = 1
				denom = int(insidefn[3:])
			except:
				numer = "unk"
				denom = "unk"
			return fntype,numer,denom,reddeg
		try:
			numerdeg = int(insidefn)
			if numerdeg % 180 == 0:
				numer = int(numerdeg/180)
				denom = 1
			elif numerdeg % 90 == 0:
				numer = int(numerdeg/90)
				denom = 2
			elif numerdeg % 60 == 0:
				numer = int(numerdeg/60)
				denom = 3
			elif numerdeg % 45 == 0:
				numer = int(numerdeg/45)
				denom = 4
			elif numerdeg % 30 == 0:
				numer = int(numerdeg/30)
				denom = 6
			reddeg[1] = numerdeg
			return fntype,numer,denom,reddeg
		except:
			numer = "unk"
			denom = "unk"
			
		return fntype,numer,denom,reddeg
			
					


def makegraph(fntype,numer,denom,framen):
	linestrs = []
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (1,0) node[right,yshift=15pt] {$\theta=0$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.866025,.5) node[right] {$\theta=\frac{\pi}{6}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.707107,.707107) node[right] {$\theta=\frac{\pi}{4}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.5,.866025) node[right] {$\theta=\frac{\pi}{3}$};')
	
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (0,1) node[above] {$\theta=\frac{\pi}{2}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.866025,.5) node[left] {$\theta=\frac{5\pi}{6}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.707107,.707107) node[left] {$\theta=\frac{3\pi}{4}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.5,.866025) node[left] {$\theta=\frac{2\pi}{3}$};')
	
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-1,0) node[left,yshift=15pt] {$\theta=\pi$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.866025,-.5) node[right] {$\theta=\frac{11\pi}{6}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.707107,-.707107) node[right] {$\theta=\frac{7\pi}{4}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (.5,-.866025) node[right] {$\theta=\frac{5\pi}{3}$};')
	
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (0,-1) node[below] {$\theta=\frac{3\pi}{2}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.866025,-.5) node[left] {$\theta=\frac{7\pi}{6}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.707107,-.707107) node[left] {$\theta=\frac{5\pi}{4}$};')
	linestrs.append(r'\draw[<->,red,thick] (0,0) -- (-.5,-.866025) node[left] {$\theta=\frac{4\pi}{3}$};')
	
	linestrs1 = []
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (1,0) node[right,yshift=15pt] {$\theta=0$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.866025,.5) node[right] {$\theta=\frac{\pi}{6}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.707107,.707107) node[right] {$\theta=\frac{\pi}{4}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.5,.866025) node[right] {$\theta=\frac{\pi}{3}$};')
	
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (0,1) node[above] {$\theta=\frac{\pi}{2}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.866025,.5) node[left] {$\theta=\frac{5\pi}{6}=\pi-\frac{\pi}{6}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.707107,.707107) node[left] {$\theta=\frac{3\pi}{4}=\pi-\frac{\pi}{4}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.5,.866025) node[left] {$\theta=\frac{2\pi}{3}=\pi-\frac{\pi}{3}$};')
	
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-1,0) node[left,yshift=15pt] {$\theta=\pi$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.866025,-.5) node[right] {$\theta=\frac{11\pi}{6}=\frac{-\pi}{6}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.707107,-.707107) node[right] {$\theta=\frac{7\pi}{4}=\frac{-\pi}{4}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (.5,-.866025) node[right] {$\theta=\frac{5\pi}{3}=\frac{-\pi}{3}$};')
	
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (0,-1) node[below] {$\theta=\frac{3\pi}{2}=\frac{-\pi}{2}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.866025,-.5) node[left] {$\theta=\frac{7\pi}{6}=\pi+\frac{\pi}{6}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.707107,-.707107) node[left] {$\theta=\frac{5\pi}{4}=\pi+\frac{\pi}{4}$};')
	linestrs1.append(r'\draw[<->,red,thick] (0,0) -- (-.5,-.866025) node[left] {$\theta=\frac{4\pi}{3}=\pi+\frac{\pi}{3}$};')

	ystrs = []
	ystyle = r'<-,black,thick,dotted'
	ystrs.append(r'\draw['+ystyle+r'] (0,0) -- (1,0) node[below,xshift=-45pt] {$y=0$};')
	ystrs.append(r'\draw['+ystyle+r'] (.866025,0) -- (.866025,.5) node[left,yshift=-50pt] {$y=\frac{1}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (.707107,0) -- (.707107,.707107) node[left,yshift=-75pt] {$y=\frac{\sqrt{2}}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (.5,0) -- (.5,.866025) node[right,yshift=-100pt] {$y=\frac{\sqrt{3}}{2}$};')
	
	ystrs.append(r'\draw['+ystyle+r'] (0,0) -- (0,1) node[left,yshift=-25pt] {$y=1$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.866025,0) -- (-.866025,.5) node[right,yshift=-50pt] {$y=\frac{1}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.707107,0) -- (-.707107,.707107) node[right,yshift=-75pt] {$y=\frac{\sqrt{2}}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.5,0) -- (-.5,.866025) node[left,yshift=-100pt] {$y=\frac{\sqrt{3}}{2}$};')
	
	ystrs.append(r'\draw['+ystyle+r'] (0,0) -- (-1,0) node[above,xshift=45pt] {$y=0$};')
	ystrs.append(r'\draw['+ystyle+r'] (.866025,0) -- (.866025,-.5) node[left,yshift=50pt] {$y=-\frac{1}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (.707107,0) -- (.707107,-.707107) node[left,yshift=75pt] {$y=-\frac{\sqrt{2}}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (.5,0) -- (.5,-.866025) node[right,yshift=100pt] {$y=-\frac{\sqrt{3}}{2}$};')
	
	ystrs.append(r'\draw['+ystyle+r'] (0,0) -- (0,-1) node[right,yshift=25pt] {$y=-1$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.866025,0) -- (-.866025,-.5) node[right,yshift=50pt] {$y=-\frac{1}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.707107,0) -- (-.707107,-.707107) node[right,yshift=75pt] {$y=-\frac{\sqrt{2}}{2}$};')
	ystrs.append(r'\draw['+ystyle+r'] (-.5,0) -- (-.5,-.866025) node[left,yshift=100pt] {$y=-\frac{\sqrt{3}}{2}$};')
	
	xstrs = []
	xstyle = r'<-,black,thick,dotted'
	xstrs.append(r'\draw['+xstyle+r'] (0,0) -- (1,0) node[above,xshift=-45pt] {$x=1$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.5) -- (.866025,.5) node[above,xshift=-60pt] {$x=\frac{\sqrt{3}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.707107) -- (.707107,.707107) node[above,xshift=-50pt] {$x=\frac{\sqrt{2}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.866025) -- (.5,.866025) node[above,xshift=-20pt] {$x=\frac{1}{2}$};')
	
	xstrs.append(r'\draw['+xstyle+r'] (0,0) -- (0,1) node[right,yshift=-25pt] {$x=0$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.5) -- (-.866025,.5) node[above,xshift=60pt] {$x=-\frac{\sqrt{3}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.707107) -- (-.707107,.707107) node[above,xshift=50pt] {$x=-\frac{\sqrt{2}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,.866025) -- (-.5,.866025) node[above,xshift=20pt] {$x=-\frac{1}{2}$};')
	
	xstrs.append(r'\draw['+xstyle+r'] (0,0) -- (-1,0) node[below,xshift=45pt] {$x=-1$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.5) -- (.866025,-.5) node[below,xshift=-60pt] {$x=\frac{\sqrt{3}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.707107) -- (.707107,-.707107) node[below,xshift=-50pt] {$x=\frac{\sqrt{2}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.866025) -- (.5,-.866025) node[below,xshift=-20pt] {$x=\frac{1}{2}$};')
	
	xstrs.append(r'\draw['+xstyle+r'] (0,0) -- (0,-1) node[left,yshift=25pt] {$x=0$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.5) -- (-.866025,-.5) node[below,xshift=60pt] {$x=-\frac{\sqrt{3}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.707107) -- (-.707107,-.707107) node[below,xshift=50pt] {$x=-\frac{\sqrt{2}}{2}$};')
	xstrs.append(r'\draw['+xstyle+r'] (0,-.866025) -- (-.5,-.866025) node[below,xshift=20pt] {$x=-\frac{1}{2}$};')
	
	if denom == 1:
		goodlines = [0,8]
		if numer % 2 == 0:
			goodidx = 0
		else:
			goodidx = 8 
	elif denom == 2:
		goodlines = [4,12]
		if (numer - 1) % 4 == 0:
			goodidx = 4
		else:
			goodidx = 12 
	elif denom == 3:
		goodlines = [3,7,11,15]
		if (numer - 1) % 6 == 0:
			goodidx = 3
		elif (numer - 2) % 6 == 0:
			goodidx = 7
		elif (numer - 4) % 6 == 0:
			goodidx = 15
		else:
			goodidx = 11
	elif denom == 4:
		goodlines = [2,6,10,14]
		if (numer - 1) % 8 == 0:
			goodidx = 2
		elif (numer - 3) % 8 == 0:
			goodidx = 6
		elif (numer - 5) % 8 == 0:
			goodidx = 14
		else:
			goodidx = 10
	elif denom == 6:
		goodlines = [1,5,9,13]
		if (numer - 1) % 12 == 0:
			goodidx = 1
		elif (numer - 5) % 12 == 0:
			goodidx = 5
		elif (numer - 7) % 12 == 0:
			goodidx = 13
		else:
			goodidx = 9
		
	if framen == 0:
		for idx in range(0,len(linestrs)):
			linestrs[idx] = ''
	elif framen == 2:
		for idx in range(0,len(linestrs)):
			if idx not in goodlines:
				linestrs[idx] = ''
	elif framen > 2:
		for idx in range(0,len(linestrs)):
			if idx not in goodlines:
				linestrs[idx] = ''
			else:
				linestrs[idx] = linestrs1[idx]
				
	if framen < 4:
		for idx in range(0,len(ystrs)):
			ystrs[idx] = ''
	elif framen > 3 and fntype!='cos' and fntype!='sec':
		for idx in range(0,len(ystrs)):
			if idx not in goodlines:
				ystrs[idx] = ''
	else:
		for idx in range(0,len(ystrs)):
			ystrs[idx] = ''
				
	if framen < 4:
		for idx in range(0,len(ystrs)):
			xstrs[idx] = ''
	elif framen > 3 and fntype!='sin' and fntype!='csc':
		for idx in range(0,len(ystrs)):
			if idx not in goodlines:
				xstrs[idx] = ''
	else:
		for idx in range(0,len(ystrs)):
			xstrs[idx] = ''

	if framen == 5:
		for idx in range(0,len(ystrs)):
			if idx != goodidx:
				xstrs[idx] = ''
				ystrs[idx] = ''
				linestrs[idx] = ''


	graphstr = r'''\begin{minipage}{.475\linewidth}
		\begin{tikzpicture}[xscale=5,yscale=5]
		  \draw[->] (-1.25,0) -- (1.25,0) node[right] {$x$};
		  \draw[->] (0,-1.25) -- (0,1.25) node[above] {$y$};
  
		  \draw[domain=-1:1,smooth,variable=\x,blue] (0,0) circle (1);
		  '''+linestrs[0]+r'''
		  '''+linestrs[1]+r'''
		  '''+linestrs[2]+r'''
		  '''+linestrs[3]+r'''
		  '''+linestrs[4]+r'''
		  '''+linestrs[5]+r'''
		  '''+linestrs[6]+r'''
		  '''+linestrs[7]+r'''
		  '''+linestrs[8]+r'''
		  '''+linestrs[9]+r'''
		  '''+linestrs[10]+r'''
		  '''+linestrs[11]+r'''
		  '''+linestrs[12]+r'''
		  '''+linestrs[13]+r'''
		  '''+linestrs[14]+r'''
		  '''+linestrs[15]+r'''
		  '''+ystrs[0]+r'''
		  '''+ystrs[1]+r'''
		  '''+ystrs[2]+r'''
		  '''+ystrs[3]+r'''
		  '''+ystrs[4]+r'''
		  '''+ystrs[5]+r'''
		  '''+ystrs[6]+r'''
		  '''+ystrs[7]+r'''
		  '''+ystrs[8]+r'''
		  '''+ystrs[9]+r'''
		  '''+ystrs[10]+r'''
		  '''+ystrs[11]+r'''
		  '''+ystrs[12]+r'''
		  '''+ystrs[13]+r'''
		  '''+ystrs[14]+r'''
		  '''+ystrs[15]+r'''
		  '''+xstrs[0]+r'''
		  '''+xstrs[1]+r'''
		  '''+xstrs[2]+r'''
		  '''+xstrs[3]+r'''
		  '''+xstrs[4]+r'''
		  '''+xstrs[5]+r'''
		  '''+xstrs[6]+r'''
		  '''+xstrs[7]+r'''
		  '''+xstrs[8]+r'''
		  '''+xstrs[9]+r'''
		  '''+xstrs[10]+r'''
		  '''+xstrs[11]+r'''
		  '''+xstrs[12]+r'''
		  '''+xstrs[13]+r'''
		  '''+xstrs[14]+r'''
		  '''+xstrs[15]+r'''

		\end{tikzpicture}
		\end{minipage}\hfill'''
	return graphstr
def makeallstrs(fntype,numer,denom,reddeg):
	fnstr = '\\'+fntype
	if numer == 1:
		numerstr = ''
	elif numer == -1:
		numerstr = '-'
	else:
		numerstr = str(numer)
	if reddeg[1]:
		startangle = str(reddeg[1])+r'^{\circ}'
		angle1str = r'& = '+fnstr+r'(\frac{'+numerstr+r'\pi}{'+str(denom)+r'})\\'
		angle1type = 'degrees'
	elif reddeg[0]:
		startangle = r'\frac{'+str(numer*reddeg[0])+r'\pi}{'+str(denom*reddeg[0])+r'}'
		angle1str = r'& = '+fnstr+r'(\frac{'+numerstr+r'\pi}{'+str(denom)+r'})\\'
		angle1type = 'reduce'
	else:
		startangle = r'\frac{'+numerstr+r'\pi}{'+str(denom)+r'}'
		angle1str = r''
	if abs(numer) != 1:
		pinumer = 0
		if (numer-1) % denom == 0:
			pinumer = int((numer-1)/denom)
			isneg = r''
		elif (numer+1) % denom == 0:
			pinumer = int((numer+1)/denom)
			isneg = r'-'
		else:
			angle2str = r''
			angle3str = r''
			angle4str = r''
			angle5str = r''


		angle2str = r'& = '+fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
		if pinumer ==1:
			angle3str = r'& = '+fnstr+r'(\pi+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
		elif pinumer ==-1:
			angle3str = r'& = '+fnstr+r'(-\pi+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
		else:
			angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'


		if pinumer % 2 == 0:
			angle6str = r'& = '+getTrigValue(fntype,isneg,0,denom)
			if pinumer != 2:
				angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
				angle5str = r'& = '+fnstr+r'(\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
			else:
				angle4str = r''
				angle5str = r'& = '+fnstr+r'(\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
		else:
			angle6str = r'& = '+getTrigValue(fntype,isneg,1,denom)
			if pinumer != 1:
				angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
				angle5str = r'& = '+fnstr+r'(\pi+\frac{'+isneg+r'\pi}{'+str(denom)+r'})\\'
			else:
				angle4str = r''
				angle5str = r''
		
	else:

		angle2str = r''
		angle3str = r''
		angle4str = r''
		angle5str = r''
		if numer < 0:
			angle6str = r'& = '+getTrigValue(fntype,'-',0,denom)
		else:
			angle6str = r'& = '+getTrigValue(fntype,'',0,denom)
	
	allstrs = []

	if len(angle1str) > 0:
		allstrs.append([angle1str,angle1type])
	if len(angle2str) > 0:
		allstrs.append([angle2str,'pifrac'])
	if len(angle3str) > 0:
		allstrs.append([angle3str,'pi'])
	if len(angle4str) > 0:
		allstrs.append([angle4str,'2pi'])
	if len(angle5str) > 0:
		allstrs.append([angle5str,'equiv'])
	if len(angle6str) > 0:
		allstrs.append([angle6str,'answer'])
	
	return allstrs
def makeequation(fntype,numer,denom,framen,reddeg,allstrs):
	equationtype = ''
	fnstr = '\\'+fntype
	if numer == 1:
		numerstr = ''
	elif numer == -1:
		numerstr = '-'
	else:
		numerstr = str(numer)
	if reddeg[1]:
		startangle = str(reddeg[1])+r'^{\circ}'
	elif reddeg[0]:
		startangle = r'\frac{'+str(numer*reddeg[0])+r'\pi}{'+str(denom*reddeg[0])+r'}'
	else:
		startangle = r'\frac{'+numerstr+r'\pi}{'+str(denom)+r'}'
	equationstr = r'''\begin{minipage}{.5\linewidth}
		\scalebox{1.95}{\parbox{.5\linewidth}{%
		\large
		\begin{align*}
	'''+fnstr+r'''('''+startangle+r''') '''
	if len(allstrs[:min(framen,len(allstrs))])==0:
		equationstr += r'& ='
	for astr in allstrs[:min(framen,len(allstrs))]:
		equationstr+=astr[0]
		equationtype = astr[1]
	equationstr+=r'''
		\end{align*}
		}}
	\end{minipage}

	\end{document}'''
	return equationstr,equationtype

def run_it(my_function,hashprefix):
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows}


	\begin{document}
	\huge'''
	fn = my_function.replace('*','')
	fntype,numer,denom,reddeg = gettrig(fn)
	ff = open('images/new/'+hashprefix+'inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')
	ffs = open('images/new/'+hashprefix+'subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')
	gcdnd = gcd(abs(numer),denom)
	if gcdnd > 1:
		reddeg[0] = gcdnd
		numer = int(numer/gcdnd)
		denom = int(denom/gcdnd)
	allstrs = makeallstrs(fntype,numer,denom,reddeg)
	colors = []
	if reddeg[0] or reddeg[1]:
		addframe = 1
	else:
		addframe = 0
	fullduration = 0.0
	for framen in range(0,6+addframe + len(allstrs)+1):
		thestr = startstr
		duration = 1.0
		if framen == 0:
			thestr += '\n'+makegraph(fntype,numer,denom,0)
			duration = 3.0

			ffs.write(str(framen+1)+'\n')
			ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
			ffs.write("We want to find sine of this angle.\n\n")
			fullduration += duration
		elif framen == 1:
			thestr += '\n'+makegraph(fntype,numer,denom,1)
			duration = 5.0
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
			ffs.write("We need to identify which of these 16 angles to use.\n\n")
			fullduration += duration
		elif framen == 1+addframe:
			thestr += '\n'+makegraph(fntype,numer,denom,1)
			fullduration += duration
		elif framen == 2+addframe:
			thestr += '\n'+makegraph(fntype,numer,denom,2)
			duration = 4.0
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
			ffs.write("The denominator is 6 so it is one of these 4 angles.\n\n")
			fullduration += duration
		elif framen == 3+addframe:
			thestr += '\n'+makegraph(fntype,numer,denom,3)
			duration = 4.0
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
			ffs.write("For consistency, write each angle with numerator of plus/minus 1.\n\n")
			fullduration += duration
		elif framen == 4+addframe:
			thestr += '\n'+makegraph(fntype,numer,denom,4)
			duration = 6.0
			ffs.write(str(framen+1)+'a\n')
			ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+3.0)+'00\n')
			ffs.write("For sine, we care about the y-coordinates.\n\n")
			ffs.write(str(framen+1)+'b\n')
			ffs.write('00:'+tstamp(fullduration+3.0)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
			ffs.write("Note that the answer must be plus or minus one half.\n\n")
			fullduration += duration
		elif framen >= 5+addframe+len(allstrs)-1:
			thestr += '\n'+makegraph(fntype,numer,denom,5)
		else:
			thestr += '\n'+makegraph(fntype,numer,denom,4)
			
		if framen < 2:
			rett = makeequation(fntype,numer,denom,0,reddeg,allstrs)
			thestr += '\n'+rett[0]
		elif framen == 2:
			rett = makeequation(fntype,numer,denom,0+addframe,reddeg,allstrs)
			thestr += '\n'+rett[0]
		elif framen < 5+addframe:
			rett = makeequation(fntype,numer,denom,0+addframe,reddeg,allstrs)
			thestr += '\n'+rett[0]
		elif framen < 5+addframe + len(allstrs):
			rett = makeequation(fntype,numer,denom,framen-4,reddeg,allstrs)
			thestr += '\n'+rett[0]
			if rett[1] == 'pifrac':
				duration = 6.0
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
				ffs.write("Find the nearest multiple of pi. The denominator is 6 so use multiples of 6pi in the numerator.\n\n")
				fullduration += duration
			if rett[1] == 'pi':
				duration = 3.0
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
				ffs.write("Reduce the fraction.\n\n")
				fullduration += duration
			if rett[1] == '2pi':
				duration = 3.0
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
				ffs.write("Separate multiples of 2pi.\n\n")
				fullduration += duration
			if rett[1] == 'equiv':
				duration = 3.0
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
				ffs.write("Remove the multiples of 2pi to get an equivalent angle.\n\n")
				fullduration += duration
			if rett[1] == 'answer':
				duration = 3.0
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+duration)+'00\n')
				ffs.write("Answer.\n\n")
				fullduration += duration


		else:
			rett = makeequation(fntype,numer,denom,5+addframe+len(allstrs)-1,reddeg,allstrs)
			thestr += '\n'+rett[0]
		f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'trig'+str(framen)+'.tex','w')
		f.write(thestr)
		f.close()
		if framen == 0:
			ff.write("file '"+hashprefix+'trig'+str(framen)+".png'\nduration "+str(duration+.1)+"\n")
		else:
			ff.write("file '"+hashprefix+'trig'+str(framen)+".png'\nduration "+str(duration+.005)+"\n")

		#worker(hashprefix,framen)
		os.system('./outputLatex.sh -c "'+hashprefix+'trig'+str(framen)+'"')
	ff.close()
	ffs.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -f concat -i images/new/audioinputs.ffconcat -acodec copy -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'trig.mp4 -y')
	os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'trig.mp4 -y')
	jsoncolors = []
	for i in colors:
		jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	return 'new/'+hashprefix+'trig.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
#run_it('sin(13pi/6)','zasz')