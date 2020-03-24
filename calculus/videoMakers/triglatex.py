import sympy
from sympy import *
from sympy.abc import x
import sys

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
			
					
startstr = r'''\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

\usetikzlibrary{shapes.geometric, arrows}


\begin{document}
\huge'''

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
	elif denom == 2:
		goodlines = [4,12]
	elif denom == 3:
		goodlines = [3,7,11,15]
	elif denom == 4:
		goodlines = [2,6,10,14]
	elif denom == 6:
		goodlines = [1,5,9,13]
		
	if framen == 0:
		for idx in range(0,len(linestrs)):
			linestrs[idx] = ''
	elif framen > 1:
		for idx in range(0,len(linestrs)):
			if idx not in goodlines:
				linestrs[idx] = ''
				
	if framen < 3:
		for idx in range(0,len(ystrs)):
			ystrs[idx] = ''
	elif framen > 2:
		for idx in range(0,len(ystrs)):
			if idx not in goodlines:
				ystrs[idx] = ''
				
	if framen < 3:
		for idx in range(0,len(ystrs)):
			xstrs[idx] = ''
	elif framen > 2:
		for idx in range(0,len(ystrs)):
			if idx not in goodlines:
				xstrs[idx] = ''


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

def makeequation(fntype,numer,denom,framen,reddeg):
	fnstr = '\\'+fntype
	if numer == 1:
		numerstr = ''
	elif numer == -1:
		numerstr = '-'
	else:
		numerstr = str(numer)
	if reddeg[1]:
		startangle = str(reddeg[1])+r'^{\circ}'
		angle1str = fnstr+r'(\frac{'+numerstr+r'\pi}{'+str(denom)+r'})\\'
		if abs(numer) != 1:
			if (numer-1) % denom == 0:
				pinumer = int((numer-1)/denom)
				angle2str = r'& = '+fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			elif (numer+1) % denom == 0:
				pinumer = int((numer+1)/denom)
				angle2str = r'& = '+fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{-\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{-\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{-\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{-\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			else:
				angle2str = r''
				angle3str = r''
				angle4str = r''
				angle5str = r''
			
		else:
			angle2str = r''
			angle3str = r''
			angle4str = r''
			angle5str = r''
	elif reddeg[0]:
		startangle = r'\frac{'+str(numer*reddeg[0])+r'\pi}{'+str(denom*reddeg[0])+r'}'
		angle1str = fnstr+r'(\frac{'+numerstr+r'\pi}{'+str(denom)+r'})\\'
		if abs(numer) != 1:
			if (numer-1) % denom == 0:
				pinumer = int((numer-1)/denom)
				angle2str = r'& = '+fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			elif (numer+1) % denom == 0:
				pinumer = int((numer+1)/denom)
				angle2str = r'& = '+fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{-\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{-\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{-\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{-\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			else:
				angle2str = r''
				angle3str = r''
				angle4str = r''
				angle5str = r''
			
		else:
			angle2str = r''
			angle3str = r''
			angle4str = r''
			angle5str = r''
	else:
		startangle = r'\frac{'+numerstr+r'\pi}{'+str(denom)+r'}'
		angle1str = r''
		if abs(numer) != 1:
			if (numer-1) % denom == 0:
				pinumer = int((numer-1)/denom)
				angle2str = fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			elif (numer+1) % denom == 0:
				pinumer = int((numer+1)/denom)
				angle2str = fnstr+r'(\frac{'+str(pinumer*denom)+r'\pi}{'+str(denom)+r'}+\frac{-\pi}{'+str(denom)+r'})\\'
				angle3str = r'& = '+fnstr+r'('+str(pinumer)+r'\pi+\frac{-\pi}{'+str(denom)+r'})\\'
				if pinumer % 2 == 0:
					angle4str = r'& = '+fnstr+r'('+str(int(pinumer/2))+r'\cdot (2\pi)+\frac{-\pi}{'+str(denom)+r'})\\'
					angle5str = r'& = '+fnstr+r'(\frac{-\pi}{'+str(denom)+r'})\\'
				else:
					if abs(pinumer) != 1:
						angle4str = r'& = '+fnstr+r'('+str(int((pinumer-1)/2))+r'\cdot (2\pi)+\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
					else:
						angle4str = r'& = '+fnstr+r'(\pi+\frac{-\pi}{'+str(denom)+r'})\\'
						angle5str = r''
			else:
				angle2str = r''
				angle3str = r''
				angle4str = r''
				angle5str = r''
			
		else:
			angle2str = r''
			angle3str = r''
			angle4str = r''
			angle5str = r''
	framelist = [0,0,0,0,0]
	if len(angle1str) > 0:
		framelist[0] = 1
	if len(angle2str) > 0:
		framelist[1] = framelist[0]+1
	else:
		framelist[1] = framelist[0]
	if len(angle3str) > 0:
		framelist[2] = framelist[1]+1
	else:
		framelist[2] = framelist[1]
	if len(angle4str) > 0:
		framelist[3] = framelist[2]+1
	else:
		framelist[3] = framelist[2]
	if len(angle5str) > 0:
		framelist[4] = framelist[3]+1
	else:
		framelist[4] = framelist[3]
	if framen < framelist[0]:
		angle1str = ''
	if framen < framelist[1]:
		angle2str = ''
	if framen < framelist[2]:
		angle3str = ''
	if framen < framelist[3]:
		angle4str = ''
	if framen < framelist[4]:
		angle5str = ''
		
	equationstr = r'''\begin{minipage}{.5\linewidth}
		\scalebox{1.95}{\parbox{.5\linewidth}{%
		\large
		\begin{align*}
	'''+fnstr+r'''('''+startangle+r''') & = '''+angle1str+angle2str+angle3str+angle4str+angle5str+r'''
		\end{align*}
		}}
	\end{minipage}

	\end{document}'''
	return equationstr


fn = 'sin(7pi)'
fntype,numer,denom,reddeg = gettrig(fn)
framen = int(sys.argv[1])
thestr = startstr
gcdnd = gcd(abs(numer),denom)
if gcdnd > 1:
	reddeg[0] = gcdnd
	numer = int(numer/gcdnd)
	denom = int(denom/gcdnd)
	

if framen < 5:
	thestr += '\n'+makegraph(fntype,numer,denom,framen)
elif framen < 10:
	thestr += '\n'+makegraph(fntype,numer,denom,0)
else:
	thestr += '\n'+makegraph(fntype,numer,denom,0)
	
if framen < 10:
	thestr += '\n'+makeequation(fntype,numer,denom,framen,reddeg)
else:
	thestr += '\n'+makeequation(fntype,numer,denom,0,reddeg)
	

print(thestr)