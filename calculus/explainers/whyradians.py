import sympy
from sympy import *
from sympy.abc import x
import os
import time
from subprocess import Popen
import sys


def tstamp(the_time):
	if the_time == 0:
		return '00:00.0'
	if the_time < 10:
		return '00:0'+str(the_time)
	elif the_time < 60:
		return '00:'+str(the_time)
	elif the_time < 70:
		return '01:0'+str(the_time - 60)
	elif the_time < 120:
		return '01:'+str(the_time - 60)
	elif the_time < 130:
		return '02:0'+str(the_time - 120)
	elif the_time < 180:
		return '02:'+str(the_time - 120)
	elif the_time < 190:
		return '03:0'+str(the_time - 180)
	elif the_time < 240:
		return '03:'+str(the_time - 180)
	elif the_time < 250:
		return '04:0'+str(the_time - 240)
	elif the_time < 300:
		return '04:'+str(the_time - 240)
	elif the_time < 310:
		return '05:0'+str(the_time - 300)
	elif the_time < 360:
		return '05:'+str(the_time - 300)
def toJavascript(input_string):
	input_string = input_string.replace('\\','\\\\')
	#input_string = input_string.replace(r'$',r'')
	input_string = r'\\text{'+input_string+'}'

	return input_string

def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval
	
def trigradian(rawfn):
	index = rawfn.find('(')
	if index == -1:
		return rawfn
	elif index < 3:
		return rawfn[:index+1]+trigradian(rawfn[index+1:])
	else:
		if rawfn[index-3:index] in ['sin','cos','tan','cot','sec','csc']:
			indexf = index
			npars = 1
			indexr = -1
			while npars > 0 and index < len(rawfn) - 1:
				index += 1
				if rawfn[index] == '(':
					npars += 1
				elif rawfn[index] == ')':
					npars -= 1
				if npars == 0:
					indexr = index
			if indexr > -1:
				rawfn = rawfn[:indexr]+' r'+rawfn[indexr:]
			return rawfn[:indexf+1]+trigradian(rawfn[indexf+1:])
		else:
			return rawfn[:index+1]+trigradian(rawfn[index+1:])
					

def makegraph(graphpart):
	xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs = graphpart

	graphstr = r'''\Large\begin{tikzpicture}[xscale='''+str(xscale)+r''',yscale='''+str(yscale)+r''']
	'''


	for axisstr in axisstrs:
		graphstr += axisstr+'\n'
	for pointstr in pointstrs:
		graphstr += pointstr+'\n'
	graphstr += r'''\clip ('''+str(cliprect['xmin'])+r''','''+str(cliprect['ymin'])+r''') rectangle ('''+str(cliprect['xmax'])+r''','''+str(cliprect['ymax'])+r''');'''+'\n'
	for plotstr in plotstrs:
		graphstr += plotstr+'\n'


	

	graphstr += r'''
	\end{tikzpicture}'''
	return graphstr

def makeequation(estr,scale):
	equationstr = r'''
	\scalebox{'''+str(scale)+r'''}{\parbox{'''+str(1.0/scale)+r'''\linewidth}{%
	\large
	\begin{align*}'''+estr+r'''
	\end{align*}
	}}
	'''
	return equationstr.replace('+-','-')

def maketext(tstr):
	textstr = r'''
	\Huge
	\vspace{5pt}
	\noindent
	'''+tstr
	return textstr

def maketable(a,b,n,fn,framen,rtype):
	duration = .5
	audioStr = ''
	allValues = []
	allX = []
	if framen == 1:
		duration = 5.0
	else:
		duration = 4.0
	if rtype == 'LRAM':
		modifier = 0
	elif rtype == 'RRAM':
		modifier = 1
	elif rtype == 'MRAM':
		modifier = .5
	for i in range(0,n):
		fntemp = fn.evalf(subs={x: a+(i+modifier)*1.0*(b-a)/n})
		allValues.append(fntemp)
		allX.append(a+(i+modifier)*1.0*(b-a)/n)
	if n > 10:
		tablesize = r'\normalsize'
	elif n > 8:
		tablesize = r'\large'
	elif n > 5:
		tablesize = r'\Large'
	else:
		tablesize = ''
	colstr = '|'
	for i in range(0,n+1):
		colstr += 'c|'
	row1str = 'i'
	row2str = '$x_i$'
	row3str = '$f(x_i)$'
	if n == 2:
		tframes = 2
	elif n == 3:
		tframes = 3
	elif n == 4:
		tframes = 4
	elif n > 4:
		tframes = 4

	for i in range(0,n):
		row1str += ' & '+str(i+1)
	for i in range(0,n):
		if framen > min(i,2) and (i != n-1 or n < 4 or framen > 3):
			row2str += ' & '+cleandecimal(allX[i],2)
		else:
			row2str += ' & '
	for i in range(0,n):
		if framen - tframes > min(i,2) and (i != n-1 or n < 4 or framen - tframes > 3):
			row3str += ' & '+cleandecimal(allValues[i],2)
		else:
			row3str += ' & '

	tablestr = r'''\begin{minipage}{.5\linewidth}
	\huge
	\vspace{5pt}
	\begin{center}
	'''+tablesize+r'''
	\begin{tabular}{ '''+colstr+r''' } 
	 \hline
	 '''+row1str+r'''\\ 
	 \hline
	'''+row2str+r'''\\ 
	\hline
	'''+row3str+r'''\\  
	\hline
	\end{tabular}
	\end{center}
	\end{minipage}
	\end{document}'''
	return tablestr, duration, audioStr
def worker(hashprefix,framen):
	os.system('./outputLatex.sh -c "'+hashprefix+'rie'+str(framen)+'"')
	
def makestr(twopages,startstr,pages,tstr,estr,gstr,framen,tframes):
	thestr = startstr
	if twopages:
		thestr += r'''\begin{minipage}{'''+str(twopages[0])+r'''\linewidth}'''
		for page in pages[0]:
			if page == 'text':
				thestr += maketext(tstr[0][framen])
			if page == 'equation':
				thestr += makeequation(estr[framen],2.0)
			if page == 'graph':
				if len(gstr[framen])>0:
					thestr += makegraph(gstr[framen])
		thestr += r'''\end{minipage}\hfill'''
		thestr += r'''\begin{minipage}{'''+str(twopages[1])+r'''\linewidth}'''
		for page in pages[1]:
			if page == 'text':
				thestr += maketext(tstr[1][framen])
			if page == 'equation':
				thestr += makeequation(estr[framen],2.0)
			if page == 'graph':
				if len(gstr[framen])>0:
					thestr += makegraph(gstr[framen])
		thestr += r'''\end{minipage}'''
	else:
		for page in pages[0]:
			if page == 'text':
				thestr += maketext(tstr[framen])
			if page == 'equation':
				thestr += makeequation(estr[framen],2.0)

	thestr += r'''\end{document}'''

	f = open('/tmp/me/mneri/pnglatex/explainerframe'+str(tframes)+'.tex','w')
	f.write(thestr)
	f.close()

def run_it():
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\usepackage{mathtools}
	\usepackage{color}
	\usepackage{ulem}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows}


	\begin{document}
	\LARGE'''
	
	
	ff = open('inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')
	ffs = open('subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')
	ffa = open('inputsAudio.ffconcat','w')
	ffa.write('ffconcat version 1.0\n\n')

	#ffa = open('inputsAudio.ffconcat','w')
	#ffa.write('ffconcat version 1.0\n\n')
	
	colors = []
	tduration = 0
	tframes = 0
	fullduration = 0
	timescale = 1.0


	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0,5.0]
		twopages = [.475,.5]
		pages = [['equation'],['graph']]

		estr = [r'''\sin(\theta)& = \frac{\sqrt{2}}{2}''']
		estr.append(estr[0]+r'''\\ \sin(45^{\circ})& = \frac{\sqrt{2}}{2}''')

		estr.append(estr[1]+r'''\\ \sin\left(\frac{\pi}{4}\right)& = \frac{\sqrt{2}}{2}''')
		estr.append(estr[2]+r'''\\ \sin\left(\frac{\star}{8}\right)& = \frac{\sqrt{2}}{2}''')

		  
		
		yscale = 3.0
		xscale = 3.0
		xmin = -1.5
		xmax = 1.5
		ymin = -1.5
		ymax = 1.5

		axisstrs = []
		axisstrs.append(r'''\draw[->] ('''+str(xmin)+r''',0) -- ('''+str(xmax)+r''',0) node[right] {$x$};''')
		axisstrs.append(r'''\draw[->] (0,'''+str(ymin)+r''') -- (0,'''+str(ymax)+r''') node[above] {$y$};''')

		pointstrs = []
		pointstrs.append(r'''\draw[-] (.7,.7) -- (0,0) node[right,xshift=8,yshift=8] {$\theta$};''')
		pointstrs.append(r'''\draw[-] (.075,.7) -- (-.075,.7) node[left] {$\frac{\sqrt{2}}{2}$};''')
		pointstrs.append(r'''\draw[-] (.7,.7) -- (.7,0);''')
		pointstrs.append(r'''\draw[red] (0,0) circle (1);''')

		plotstrs = []
		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr = [[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs]]

		startstr2 = startstr + r'''\begin{center}
			Why are radians better than degrees for calculus?
		\end{center}'''

		makestr(twopages,startstr2,pages,[],estr,gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [4.5*timescale,'Degrees are a perfectly acceptable unit for trigonometry. 360 might be an'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'arbitrary choice for the number of degrees in a circle, but it does allow']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'for nice round numbers for many important angles.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(11.5*timescale)+"00\n\n")

	caption = [4.5*timescale,'To compute the sine of an angle, all that matters is the height']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'of the opposite leg of the right triangle with hypotenuse of 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Calling theta 45 degrees or pi over 4 radians does not change sine.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1b.mp3'\noutpoint 00:"+tstamp(11.5*timescale)+"00\n\n")

	caption = [5.0*timescale,'In fact we can invent new units and call theta star over 8 because it is one-eigth of the circle. ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1c.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'The unit does not change the value of sine or cosine for a particular angle.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'So why do calculus instructors insist on using an unfamilar unit?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1d.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")


	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0,5.0]
		twopages = [.475,.5]
		pages = [['equation'],['graph']]

		estr = [r'''\frac{\sin(\theta)}{\theta}& = \frac{\sqrt{2}}{2\theta}''']
		estr.append(estr[0]+r'''\\ \frac{\sin(45^{\circ})}{45^{\circ}}& = \frac{\sqrt{2}}{90^{\circ}}''')

		estr.append(estr[1]+r'''\\ \frac{\sin\left(\frac{\pi}{4}\right)}{\pi/4}& = \frac{2\sqrt{2}}{\pi}''')
		estr.append(estr[2]+r'''\\ \frac{\sin\left(\frac{\star}{8}\right)}{\star/8}& = \frac{4\sqrt{2}}{\star}''')

		  
		
		yscale = 3.0
		xscale = 3.0
		xmin = -1.5
		xmax = 1.5
		ymin = -1.5
		ymax = 1.5

		axisstrs = []
		axisstrs.append(r'''\draw[->] ('''+str(xmin)+r''',0) -- ('''+str(xmax)+r''',0) node[right] {$x$};''')
		axisstrs.append(r'''\draw[->] (0,'''+str(ymin)+r''') -- (0,'''+str(ymax)+r''') node[above] {$y$};''')

		pointstrs = []
		pointstrs.append(r'''\draw[-] (.7,.7) -- (0,0) node[right,xshift=8,yshift=8] {$\theta$};''')
		pointstrs.append(r'''\draw[-] (.075,.7) -- (-.075,.7) node[left] {$\frac{\sqrt{2}}{2}$};''')
		pointstrs.append(r'''\draw[-] (.7,.7) -- (.7,0);''')
		pointstrs.append(r'''\draw[red] (0,0) circle (1);''')

		plotstrs = []
		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr = [[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs]]

		startstr2 = startstr + r'''\begin{center}
			Why are radians better than degrees for calculus?
		\end{center}'''

		makestr(twopages,startstr2,pages,[],estr,gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [4.0*timescale,'The function sine of theta over theta is impacted by the choice of units.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2a.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [6.0*timescale,'We see that sine of 45 degrees over 45 degrees is the square root of 2 over 90 degrees.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2b.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'The first issue is how to deal with the degrees unit in the denominator.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'But we could just use a unitless value equivalent to degrees.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2c.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'The bigger issue is that sine of pi/4 over pi/4 is an entirely different value.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'2 square root of 2 divided by pi is many times larger than the result using degrees.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'And any other unit will have its own value for sine theta over theta.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2d.mp3'\noutpoint 00:"+tstamp(14.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'So in trigonometry, the units are not so important but if sine theta over theta']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'is important than so is the choice of units.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2e.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")


	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [5.0]
		
		fullstr = startstr + r'''\begin{center}
			Why is $\frac{\sin(\theta)}{\theta}$ important?
		\end{center}

			\begin{center}
		\begin{tikzpicture}[xscale=1.5,yscale=1.5]
		  \draw[->] (-3.5,0) -- (13,0) node[right] {$\theta$};
		  \draw[->] (0,-1.5) -- (0,1.5) node[above] {$y$};
		  \draw[-] (12.56,.1) -- (12.56,-.1) node[below] {$4\pi$};
		  \draw[-] (3.14,.1) -- (3.14,-.1) node[below] {$\pi$};
		  \draw[-] (-.1,1) -- (.1,1) node[left] {$1$};
		  \draw[<->,red] (-1.5,-1.5) -- (1.5,1.5);
		 

		  \draw[domain=-3.1416:12.56,smooth,variable=\x,blue] plot ({\x},{sin(\x r});
		\end{tikzpicture}
		\begin{tikzpicture}[xscale=1.5,yscale=1.5]
		  \draw[->] (-3.5,0) -- (13,0) node[right] {$\theta$};
		  \draw[->] (0,-1.5) -- (0,1.5) node[above] {$y$};
		  \draw[-] (10,.1) -- (10,-.1) node[below] {$10^{\circ}$};
		  \draw[-] (-.1,1) -- (.1,1) node[left] {$1$};
		 

		  \draw[domain=-3.1416:12.56,smooth,variable=\x,blue] plot ({\x},{sin(\x});
		\end{tikzpicture}
		\end{center}



		\end{document}'''

		f = open('/tmp/me/mneri/pnglatex/explainerframe'+str(tframes)+'.tex','w')
		f.write(fullstr)
		f.close()
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.0*timescale,'In calculus, sin theta over theta is very important.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3a.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'The top graph is the graph of sine of theta where theta is in radians.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'And the bottom graph is sine of theta where theta is in degrees.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3b.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'The slopes of the tangent lines to these two curves will be very different.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [5.0*timescale,'The slopes for the top graph will fluctuate from what looks like -1 to +1,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3d.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'but the slopes for the bottom graph will always be close to zero.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3e.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Functions with different slopes of the tangent lines will have different derivatives.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3f.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The red line in the radian graph is the tangent line when theta equals zero.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'An eyeball approximation of the slope of this line would be 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3g.mp3'\noutpoint 00:"+tstamp(7.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'The tangent line to the degrees graph at theta equals zero would basically']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'overlap the function and have slope only very slightly positive.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3h.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Clearly the units have a significant impact on the derivative of sine of theta.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'But why are radians the best choice?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3i.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")


	for framen in range(0,7):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0,5.0,3.0,3.0]
		twopages = False
		pages = [['equation'],[]]

		estr = [r'''\normalsize\frac{d}{dx}[\sin(x)] & =\normalsize\lim_{h\rightarrow 0}\frac{\sin(x+h)-\sin(x)}{h}''']
		estr.append(estr[0]+r'''\\ & =\normalsize\lim_{h\rightarrow 0}\frac{\sin(x)\cos(h)+\cos(x)\sin(h)-\sin(x)}{h}''')

		estr.append(estr[1]+r'''\\ & =\normalsize\lim_{h\rightarrow 0}\frac{\cos(x)\sin(h)+(\sin(x)\cos(h)-\sin(x))}{h}''')
		estr.append(estr[2]+r'''\\ & =\normalsize\lim_{h\rightarrow 0}\frac{\cos(x)\sin(h)}{h}+\frac{\sin(x)\cos(h)-\sin(x)}{h}''')
		estr.append(estr[3]+r'''\\ & =\normalsize\lim_{h\rightarrow 0}\frac{\cos(x)\sin(h)}{h}+\frac{\sin(x)(\cos(h)-1)}{h}''')
		estr.append(estr[4]+r'''\\ & =\normalsize\cos(x)\lim_{h\rightarrow 0}\frac{\sin(h)}{h}+\sin(x)\lim_{h\rightarrow 0}\frac{\cos(h)-1}{h}''')
		estr.append(estr[5]+r'''\\ & =\normalsize\cos(x)\lim_{h\rightarrow 0}\frac{\sin(h)}{h}''')




		makestr(twopages,startstr,pages,[],estr,gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'To fully understand how units change the derivative we look at the limit '] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'definition of the derivative of sine of x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4a.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")

	caption = [4.5*timescale,'A bit of trigonometric and algebraic manipulation leads to ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'the derivative equaling sin(x) times the limit of sin(h) over h plus']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'cos(x) times the limit of cos(h)-1 over h.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4b.mp3'\noutpoint 00:"+tstamp(13.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'The limit of cos(h)-1 over h will be 0 regardless of the choice of units.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If you look at the graph of cosine, the tangent line at zero having zero slope']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'should be believable. More precise proofs of this limit exist and you should']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'try to understand them, but for now just know that the limit is zero.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4c.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'That leaves sine of x times the limit of sin(h) over h.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4d.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'This limit is a constant and it depends on the unit because sin(h) over h']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'depends on the unit. The ideal constant would be 1 because then the derivative']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'of sin(x) is simply cos(x) rather than some multiple.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4e.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'So what choice of units will make this limit equal 1?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4f.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0,5.0]
		twopages = [.33,.34]
		pages = [['text'],['equation']]

		estr = [r'']
		estr.append(estr[0]+r'''\normalsize\displaystyle\frac{\text{Area2}}{\text{Area1}}&=\frac{\sin(\theta)}{\theta}\cdot \frac{\text{FC}}{2\pi}''')
		estr.append(estr[1]+r'''\\ \\ \normalsize\displaystyle\lim_{\theta\rightarrow 0}\frac{\text{Area2}}{\text{Area1}}&=1''')
		estr.append(estr[2]+r'''\\ \\ \Aboxed{\normalsize\displaystyle\lim_{\theta\rightarrow 0}\frac{\sin(\theta)}{\theta}&=\frac{2\pi}{\text{FC}}}''')

		tstr = [r'''\huge
		
			\begin{center}
		\begin{tikzpicture}[xscale=3,yscale=3]
		  \draw[->] (-1.5,0) -- (1.5,0) node[right] {$x$};
		  \draw[->] (0,-1.5) -- (0,1.5) node[above] {$y$};
		  \filldraw[gray] (0,0) -- (1,0) arc (0:45:1) -- (0,0);
		  \draw[-] (.7,.7) -- (0,0) node[right,xshift=8,yshift=8] {$\theta$};

		  

		  \draw[red] (0,0) circle (1);
		\end{tikzpicture}
		\newline
		Area1 = $\frac{\theta}{\text{FC}}\cdot \pi$
		\end{center}
		
					\end{minipage}
		\begin{minipage}{.33\linewidth}
		\Huge
			\vspace{5pt}
			\noindent
			\huge
			\begin{center}
		\begin{tikzpicture}[xscale=3,yscale=3]
		  \draw[->] (-1.5,0) -- (1.5,0) node[right] {$x$};
		  \draw[->] (0,-1.5) -- (0,1.5) node[above] {$y$};
		  \filldraw[gray] (0,0) -- (.7,.7) -- (1,0) -- cycle;
		  \draw[-] (.7,.7) -- (0,0) node[right,xshift=8,yshift=8] {$\theta$};
		  \draw[-] (.7,.7) -- (.7,0);
		  \draw[-] (.7,.7) -- (1,0);
		  

		  \draw[red] (0,0) circle (1);
		\end{tikzpicture}
		\newline
		Area2 = $\frac{\sin(\theta)}{2}$
		\end{center}''']

		tstr.append(tstr[0])
		tstr.append(tstr[0])
		tstr.append(tstr[0])
		
		
		startstr2 = startstr + r'''\begin{center}
			What is $\displaystyle\lim_{\theta\rightarrow 0}\frac{\sin(\theta)}{\theta}$?
		\end{center}'''

		makestr(twopages,startstr2,pages,[tstr,[]],estr,gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'You probably learned that the limit of sin(theta) over theta as theta approaches 0 is 1.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'But that is only true when theta is in radians.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Let's use a little geometry to see why radians are a good choice."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Compare the areas of the two gray regions. The region on the left is']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'a fraction of a circle, and the region on the right is a triangle.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'To compute the area of the left region, we use the fact that the area of the']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'unit circle is 1 since the radius is 1. To compute the area of the gray region we just']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'need to figure out what percentage of the circle is shaded.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Let FC represent the full circle. So for degrees, FC is 360 degrees. For radians, FC is 2pi.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,r'For other units, FC could be 100% or 1. No matter the choice of units, the angle']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'equivalent to 45 degrees is one-eighth of a full circle so theta over FC will be 1/8.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'The area of a triangle, on the other hand, is one-half of the base times the height.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The height will be sin(theta) and the base is 1 since it is the radius of the unit circle.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Therefore the area is sin(theta) over 2.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'What is the ratio of area2 over area1?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Dividing yields sin(theta) over theta times FC over 2pi.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Why does this ratio help anything?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'As theta approaches 0, this ratio will approach 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The triangle is inside the segment of the circle so the ratio will always be']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'less than 1, and as theta gets smaller the percent of the region outside the']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'triangle gets smaller and smaller. To be more precise use geometry to find another']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'bound and apply the squeeze theorem.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If the limit of the ratio of areas is 1 than the limit of sin(theta) over theta']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'times FC over 2pi is also 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Therefore the limit of sin(theta) over theta will equal 2pi over FC.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If we want the limit of sin(theta) over theta to equal 1 then FC must be 2pi.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Remember that FC is the value of the angle representing the full circle.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'So FC is 360 degrees or 2pi radians. We see that 2pi is actually a very good']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'choice to represent the full circle because the derivative of sine will']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'exactly equal cosine. And the other derivative are also constant-free.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Converting degrees to radians may seem painful, but using radians']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'makes calculus much simpler and easier.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")



	

		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 whyradians.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
