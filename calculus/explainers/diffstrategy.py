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
	elif the_time < 370:
		return '06:0'+str(the_time - 360)
	elif the_time < 420:
		return '06:'+str(the_time - 360)
	elif the_time < 430:
		return '07:0'+str(the_time - 420)
	elif the_time < 480:
		return '07:'+str(the_time - 420)
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
					


def makegraph(a,b,n,fn,framen,rtype):
	duration = .5
	audioStr = ''
	ymin = min(0,fn.evalf(subs={x: a}))
	ymax = max(0,fn.evalf(subs={x: a}))
	allValues = []
	if rtype == 'LRAM':
		modifier = 0
	elif rtype == 'RRAM':
		modifier = 1
	elif rtype == 'MRAM':
		modifier = .5
	for i in range(0,2*n+1):
		fntemp = fn.evalf(subs={x: a+i*.5*(b-a)/n})
		if rtype == 'LRAM':
			if i % 2 == 0 and i < 2*n:
				allValues.append(fntemp)
		elif rtype == 'RRAM':
			if i % 2 == 0 and i > 0:
				allValues.append(fntemp)
		elif rtype == 'MRAM':
			if i % 2 == 1:
				allValues.append(fntemp)
		if fntemp < ymin:
			ymin = fntemp
		elif fntemp > ymax:
			ymax = fntemp
	if ymax >400:
		ymax = 400
	if ymin < -400:
		ymin = -400

	if framen == 1:
		duration = 10.0
	elif framen == 2:
		duration = 5.0
	elif framen == 3:
		duration = 3.0
	elif framen == n + 1:
		duration = 5.0
	elif framen == n + 2:
		duration = 3.0
	else:
		duration = .5
	rectstr = ''
	for i in range(0,n):
		fillcolor = 'white'
		if i == framen - 2:
			fillcolor = 'blue'
			yvalmin = str(0)
			yvalmax = str(allValues[i])
			rectstr += '\draw[arrows={-triangle 60},ultra thick] ('+str(a+(i+modifier)*1.0*(b-a)/n)+','+yvalmin+') -- ('+str(a+(i+modifier)*1.0*(b-a)/n)+','+yvalmax+');\n'
		elif i <= framen - 2:
			fillcolor = 'black'
		if i <= framen - 2:
			yvalmin = str(0)
			yvalmax = str(allValues[i])
			if allValues[i]<0:
				fillcolor = 'red'
		elif framen == 0:
			yvalmin = str(0)
			yvalmax = str(0)
		else:
			yvalmin = str(ymin-(ymax-ymin)*.1)
			yvalmax = str(ymax+(ymax-ymin)*.1)
		rectstr += '\draw[fill='+fillcolor+', draw=black, fill opacity=0.25] ('+str(a+i*1.0*(b-a)/n)+','+yvalmin+') rectangle ('+str(a+(i+1)*1.0*(b-a)/n)+','+yvalmax+');\n'
	graphstr = r'''\begin{minipage}{.475\linewidth}
	\begin{tikzpicture}[xscale='''+str(12.0/(b-a+2.0))+r''',yscale='''+str(9.0/(1.2*ymax-1.2*ymin))+r''']
	  \draw[->] ('''+str(a-1)+r''',0) -- ('''+str(b+1)+r''',0) node[right] {$x$};
	  \draw[->] (0,'''+str(ymin-(ymax-ymin)*.1)+r''') -- (0,'''+str(ymax+(ymax-ymin)*.1)+r''') node[above] {$y$};
	  \draw[-] ('''+str(a)+r''','''+str((ymax-ymin)*.03)+r''') -- ('''+str(a)+r''','''+str((ymax-ymin)*-.03)+r''') node[below] {$'''+str(a)+r'''$};
	  \draw[-] ('''+str(b)+r''','''+str((ymax-ymin)*.03)+r''') -- ('''+str(b)+r''','''+str((ymax-ymin)*-.03)+r''') node[below] {$'''+str(b)+r'''$};
  	  \clip ('''+str(a-1)+r''','''+str(ymin-(ymax-ymin)*.1)+r''') rectangle ('''+str(b+1)+r''','''+str(ymax+(ymax-ymin)*.1)+r''');
	  \draw[domain='''+str(a-1)+r''':'''+str(b+1)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)').replace('**','^'))+r'''});
	  '''+rectstr+r'''
	\end{tikzpicture}
	\end{minipage}\hfill'''
	return graphstr, duration, audioStr

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
	
def makestr(twopages,startstr,pages,tstr,estr,framen,tframes):
	thestr = startstr
	if twopages:
		thestr += r'''\begin{minipage}{'''+str(twopages[0])+r'''\linewidth}'''
		for page in pages[0]:
			if page == 'text':
				thestr += maketext(tstr[0][framen])
			if page == 'equation':
				thestr += makeequation(estr[framen])
		thestr += r'''\end{minipage}\hfill'''
		thestr += r'''\begin{minipage}{'''+str(twopages[1])+r'''\linewidth}'''
		for page in pages[1]:
			if page == 'text':
				thestr += maketext(tstr[1][framen])
			if page == 'equation':
				thestr += makeequation(estr[framen])
		thestr += r'''\end{minipage}\hfill'''
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
	\usepackage{xcolor}
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


	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [3.5,4.0,7.5]
		twopages = False
		pages = [['text']]
		headtxt = r'Differentiation Strategy'
		item1 = r'\setlength\itemsep{4em}\item Do one thing at a time.'
		item2 = r'\item Keep track of what needs to be differentiated.'
		item3 = r'\item Know the derivative rules.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,"If you struggle with derivatives, then don't try to do too much at once."] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/1a.mp3'\noutpoint 00:"+tstamp(caption[0])+"00\n\n")

	caption = [4.0*timescale,'Meticulous bookkeeping is necessary to end up at the correct answer.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/1b.mp3'\noutpoint 00:"+tstamp(caption[0])+"00\n\n")

	caption = [3.5*timescale,"Of course, you need to know the derivative rules, but "] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"knowing the rules will not do much if you don't know how to apply them."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/1c.mp3'\noutpoint 00:"+tstamp(7.5*timescale)+"00\n\n")

	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [3.5,7.5,7.0,11.5,8.0,9.0]
		twopages = False
		pages = [['text']]
		headtxt = r'One line, one rule'
		item1 = r'\setlength\itemsep{2.5em}\item Write down every function to be differentiated.'
		item2 = r'\item Apply one derivative rule to each function.'
		item3 = r'\item Add new functions to your list as they appear.'
		item4 = r'\item Continue until there are no more functions to differentiate.'
		item5 = r'\item Substitute and simplify until you have the answer.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1

	caption = [3.5*timescale,'The one line, one rule strategy for differentiation keeps the'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'differentiation separate from the algebraic simplifications.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The first step is to create a list of every function that needs to be differentiated.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2b.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'As you build the list apply one derivative rule to each function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2c.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'Applying derivative rules could generate new functions to differentiate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Add those functions to your list.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2d.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The product, quotient, and chain rules will require the differentiation of ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'two simpler functions and the sum rule adds one function for each term.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2e.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Eventually you will have no more functions that need to be differentiated.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'At this point, stop thinking about derivatives and start substituting and simplifying.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2f.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'It may sound complicated or like a lot of work, but you will only be doing one thing']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'at a time so it should be much less confusing and produce significantly fewer errors.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/2g.mp3'\noutpoint 00:"+tstamp(9.0*timescale)+"00\n\n")

	for framen in range(0,17):
		color = 'black'
		text = ''
		durations = [.5,12.0,14.5,16.0,21.0,5.0,8.5,8.5,3.5,3.0,26.0,5.0,8.5,4.0,4.0,8.0,8.5]
		twopages = False
		pages = [['text'],[]]

		headtxt = r''
		item1 = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[3x\sin(x)+x^2]=$'
		item1a = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[3x\sin(x)+x^2]=\frac{d}{dx}[3x\sin(x)]+\frac{d}{dx}[x^2]$'
		item1b = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[3x\sin(x)+x^2]=\begingroup\color{blue}\frac{d}{dx}[3x\sin(x)]\endgroup+\begingroup\color{red}\frac{d}{dx}[x^2]\endgroup=\begingroup\color{blue}3\sin(x)+3x\cos(x)\endgroup+\begingroup\color{red}2x\endgroup$'
		item1c = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[3x\sin(x)+x^2]=\frac{d}{dx}[3x\sin(x)]+\frac{d}{dx}[x^2]=3\sin(x)+3x\cos(x)+2x$'
		item2 = r'\item $\frac{d}{dx}[3x\sin(x)]=$'
		item2a = r'\item $\frac{d}{dx}[3x\sin(x)]=3\frac{d}{dx}[x\sin(x)]$'
		item2b = r'\item $\frac{d}{dx}[3x\sin(x)]=3\begingroup\color{blue}\frac{d}{dx}[x\sin(x)]\endgroup=3(\begingroup\color{blue}\sin(x)+x\cos(x)\endgroup)$'
		item2c = r'\item $\frac{d}{dx}[3x\sin(x)]=3\frac{d}{dx}[x\sin(x)]=3\sin(x)+3x\cos(x)$'
		item3 = r'\item $\frac{d}{dx}[x^2]=$'
		item3a = r'\item $\frac{d}{dx}[x^2]=2x$'
		item4 = r'\item $\frac{d}{dx}[x\sin(x)]=$'
		item4a = r'\item $\frac{d}{dx}[x\sin(x)]=\frac{d}{dx}[x]\sin(x)+x\frac{d}{dx}[\sin(x)]$'
		item4b = r'\item $\frac{d}{dx}[x\sin(x)]=\begingroup\color{blue}\frac{d}{dx}[x]\endgroup\sin(x)+x\begingroup\color{red}\frac{d}{dx}[\sin(x)]\endgroup=(\begingroup\color{blue}1\endgroup)\sin(x)+x(\begingroup\color{red}\cos(x)\endgroup)$'
		item4c = r'\item $\frac{d}{dx}[x\sin(x)]=\frac{d}{dx}[x]\sin(x)+x\frac{d}{dx}[\sin(x)]=\sin(x)+x\cos(x)$'
		item5 = r'\item $\frac{d}{dx}[x]=$'
		item5a = r'\item $\frac{d}{dx}[x]=1$'
		item6 = r'\item $\frac{d}{dx}[\sin(x)]=$'
		item6a = r'\item $\frac{d}{dx}[\sin(x)]=\cos(x)$'





		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3+item4+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+r'\end{itemize}'
		tstr9 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5+item6+r'\end{itemize}'
		tstr10 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6+r'\end{itemize}'
		tstr11 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6a+r'\end{itemize}'
		tstr12 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4b+item5a+item6a+r'\end{itemize}'
		tstr13 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4c+item5a+item6a+r'\end{itemize}'
		tstr14 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2b+item3a+item4c+item5a+item6a+r'\end{itemize}'
		tstr15 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2c+item3a+item4c+item5a+item6a+r'\end{itemize}'
		tstr16 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1b+item2c+item3a+item4c+item5a+item6a+r'\end{itemize}'
		tstr17 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2c+item3a+item4c+item5a+item6a+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8,tstr9,tstr10,tstr11,tstr12,tstr13,tstr14,tstr15,tstr16,tstr17]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [4.5*timescale,"Let's work an example to clarify the process. We're going to differentiate 3xsin(x)+x^2."] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"On the first line just write down the original function."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'For now, of course, there is nothing else to differentiate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3a.mp3'\noutpoint 00:"+tstamp(12.5*timescale)+"00\n\n")

	caption = [6.5*timescale,'Apply one rule to 3xsin(x)+x^2. The function is a sum so we must apply the sum rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3b.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")

	caption = [4.0*timescale,'When we write down the sum rule, use the proper notation and do not do any more']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'than simply write the sum rule. Now we see two new functions to differentiate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3c.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Add these two functions to our list of functions that need to be differentiated.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3d.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Eventually you will be able to skip steps that are obvious. But for now we want to']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'be able to see exactly where every part of our answer comes from.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'Once your list is temporarily complete, differentiate the next function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3e.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'The next function has a 3 multiplied by xsin(x) so apply the rule for constant multiples.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'Because 3xsin(x) is the product of 3 factors, we could have applied the product rule now.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"The answer will end up the same, but I like to use the first, easiest rule I see."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"Usually there is only one option, but when given a choice don't overanalyze, just do something."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3f.mp3'\noutpoint 00:"+tstamp(21.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'So the constant multiple rule produced 1 new function that needs to be added to the list.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3g.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Now differentiate x^2. Applying the rule for power functions, we know this derivative is 2x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,"So we don't have to add any more functions, which is nice."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3h.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [4.5*timescale,'Differentiate xsin(x) now. This is a product so apply the product rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'Again just write down the product rule without differentiating either factor.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3i.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'Then we need to add these two functions to our list.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3j.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [3.0*timescale,'Differentiate x. We know this is 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3k.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Differentiate sin(x). We know this is cos(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3l.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [4.5*timescale,"There is nothing left on our list, so assuming we left nothing off we are done differentiating."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'Now clear your head and get into substitution mode.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3m.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [5.0*timescale,'If you work your way from the bottom up, every answer you need will found in the few lines below.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3n.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'We fully know the bottom two derivatives. But the derivative of xsin(x) is not complete.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'The two derivatives in the answer are solved below so plug them into the equation.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'So the derivative of xsin(x) is sin(x)+xcos(x). That derivative is not hard but']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'if you try to do it in your head in one step it can lead to errors.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'As you get better and more confident, you can skip whatever steps you deem unnecessary.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3o.mp3'\noutpoint 00:"+tstamp(22.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'Then continuing up, the next incomplete derivative is 3xsin(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'That should be really easy since you just wrote down the derivative of xsin(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3p.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Then all that is left is to get our final answer. We can easily plug in the']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'derivatives of 3xsin(x) and x^2 because they are on the next lines.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3q.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [4.5*timescale,'This process works for any derivative. More complicated functions will lead to longer']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'lists, but eventually you will run out of functions to add.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/3r.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")


	for framen in range(0,23):
		color = 'black'
		text = ''
		durations = [.5,6.5,4.5,3.0,3.0,3.5,2.0,27.5,7.0,4.0,4.0,6.5,3.0,10.5,2.5,2.5,3.5,7.5,13.0,3.5,3.5,4.0,40.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r''
		item1 = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[2(e^x+x)^2-x]=$'
		item1a = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[2(e^x+x)^2-x]=\frac{d}{dx}[2(e^x+x)^2]-\frac{d}{dx}[x]$'
		item1b = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[2(e^x+x)^2-x]=\begingroup\color{blue}\frac{d}{dx}[2(e^x+x)^2]\endgroup-\begingroup\color{red}\frac{d}{dx}[x]\endgroup=\begingroup\color{blue}4(e^x+x)(e^x+1)\endgroup-\begingroup\color{red}1\endgroup$'
		item1c = r'\setlength\itemsep{.25em}\item $\frac{d}{dx}[2(e^x+x)^2-x]=\frac{d}{dx}[2(e^x+x)^2]-\frac{d}{dx}[x]=4(e^x+x)(e^x+1)-1$'
		item2 = r'\item $\frac{d}{dx}[2(e^x+x)^2]=$'
		item2a = r'\item $\frac{d}{dx}[2(e^x+x)^2]=2\frac{d}{dx}[(e^x+x)^2]$'
		item2b = r'\item $\frac{d}{dx}[2(e^x+x)^2]=2\begingroup\color{blue}\frac{d}{dx}[(e^x+x)^2]\endgroup=2(\begingroup\color{blue}2(e^x+x)(e^x+1)\endgroup)$'
		item2c = r'\item $\frac{d}{dx}[2(e^x+x)^2]=2\frac{d}{dx}[(e^x+x)^2]=4(e^x+x)(e^x+1)$'
		item3 = r'\item $\frac{d}{dx}[x]=$'
		item3a = r'\item $\frac{d}{dx}[x]=1$'
		item4 = r'\item $\frac{d}{dx}[(e^x+x)^2]=$'
		item4a = r'\item $\frac{d}{dx}[(e^x+x)^2]=\frac{d}{du}[u^2]\frac{d}{dx}[e^x+x]$'
		item4b = r'\item $\frac{d}{dx}[(e^x+x)^2]=\begingroup\color{blue}\frac{d}{du}[u^2]\endgroup\begingroup\color{red}\frac{d}{dx}[e^x+x]\endgroup=(\begingroup\color{blue}2u\endgroup)(\begingroup\color{red}e^x+1\endgroup)$'
		item4c = r'\item $\frac{d}{dx}[(e^x+x)^2]=\frac{d}{du}[u^2]\frac{d}{dx}[e^x+x]=2u(e^x+1)$'
		item4d = r'\item $\frac{d}{dx}[(e^x+x)^2]=\frac{d}{du}[u^2]\frac{d}{dx}[e^x+x]=2(e^x+x)(e^x+1)$'
		item5 = r'\item $\frac{d}{du}[u^2]=$'
		item5a = r'\item $\frac{d}{du}[u^2]=2u$'
		item6 = r'\item $\frac{d}{dx}[e^x+x]=$'
		item6a = r'\item $\frac{d}{dx}[e^x+x]=\frac{d}{dx}[e^x]+\frac{d}{dx}[x]$'
		item6b = r'\item $\frac{d}{dx}[e^x+x]=\begingroup\color{blue}\frac{d}{dx}[e^x]\endgroup+\begingroup\color{red}\frac{d}{dx}[x]\endgroup=\begingroup\color{blue}e^x\endgroup+\begingroup\color{red}1\endgroup$'
		item6c = r'\item $\frac{d}{dx}[e^x+x]=\frac{d}{dx}[e^x]+\frac{d}{dx}[x]=e^x+1$'
		item7 = r'\item $\frac{d}{dx}[e^x]=$'
		item7a = r'\item $\frac{d}{dx}[e^x]=e^x$'
		item8 = r'\item $\frac{d}{dx}[x]=$'
		item8a = r'\item $\frac{d}{dx}[x]=1$'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3+item4+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+r'\end{itemize}'
		tstr9 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5+item6+r'\end{itemize}'
		tstr10 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6+r'\end{itemize}'
		tstr11 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6a+r'\end{itemize}'
		tstr12 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6a+item7+item8+r'\end{itemize}'
		tstr13 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6a+item7a+item8+r'\end{itemize}'
		tstr14 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6a+item7a+item8a+r'\end{itemize}'
		tstr15 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6b+item7a+item8a+r'\end{itemize}'
		tstr16 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4a+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr17 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4b+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr18 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4c+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr19 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+item3a+item4d+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr20 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2b+item3a+item4d+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr21 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2c+item3a+item4d+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr22 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1b+item2c+item3a+item4d+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr23 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2c+item3a+item4d+item5a+item6c+item7a+item8a+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8,tstr9,tstr10,tstr11,tstr12,tstr13,tstr14,tstr15,tstr16,tstr17,tstr18,tstr19,tstr20,tstr21,tstr22,tstr23]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [7.0*timescale,"Let's see an example that requires the chain rule. Differentiate 2(e^x+x)^2-x."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'The first step is the sum/difference rule. In this case subtract the derivatives.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4b.mp3'\noutpoint 00:"+tstamp(4.5*timescale)+"00\n\n")

	caption = [6.0*timescale,'Add the two new functions to the list. Apply the constant multiple rule to the next function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4c.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Add (e^x+x)^2 to our list.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4d.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [4.0*timescale,'Differentiating x should be easy. Then we need to deal with the chain rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"First find the outside function and then the inside function is e^x + x."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4e.mp3'\noutpoint 00:"+tstamp(9.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The easiest notation for our purposes is to call the inside u and then']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'the chain rule gives us the derivative of u^2, the outside function, with respect to u']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'multiplied by the derivative of the inside function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4f.mp3'\noutpoint 00:"+tstamp(12.5*timescale)+"00\n\n")

	caption = [4.0*timescale,'You can write down that u=e^x+x to the side, but it will be clear because']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'e^x+x is inside the derivative directly adjacent.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4g.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Then add the two functions to our list. Make sure the first derivative ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'is with respect to u.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4h.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The derivative of u^2 is 2u by the power rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4i.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'The derivative of e^x+x requires the sum rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4j.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'Add the two functions to our list.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The list has gotten fairly long, but it will not get any longer.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4k.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")

	caption = [5.0*timescale,'The derivative of e^x is e^x. And the derivative of x is 1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4l.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'Now we are done with differentiating, so we just need to substitute and simplify.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'Work our way up from the bottom, completing each incomplete derivative.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4m.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [5.0*timescale,'For the derivative of e^x+x, we get e^x+1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4n.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [7.0*timescale,'Then we get to the chain rule part. Substitute the derivatives of u^2 and e^x+x from below.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4o.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'We have the derivative, but u is a variable we made up. So replace it now with the']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'appropriate function of x. We can see that the inside function was e^x+x because we']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'wrote that as the function we needed to differentiate to complete the chain rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'Now we have the derivative in terms of x and can continue.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4p.mp3'\noutpoint 00:"+tstamp(17.0*timescale)+"00\n\n")

	caption = [7.0*timescale,'Multiplying by 2 is all that is required once we have computed the derivative of (e^x+x)^2.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4q.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'The final answer is simply the difference of the two derivatives directly below.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4r.mp3'\noutpoint 00:"+tstamp(4.5*timescale)+"00\n\n")

	caption = [4.5*timescale,'The chain rule is helped by adding a dummy variable that gets replaced after differentiation,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'but there are other methods that avoid using u. Just make sure you differentiate the outside']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'function with respect to the inside function and not x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4s.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")

	caption = [3.5*timescale,"However you choose to take derivatives, make sure you always know "]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"what rule you are applying and why. Until you've mastered differentiation,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"I strongly recommend writing down every single step."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Derivatives are the heart of calculus so don't focus on"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"anything else until you're comfortable taking derivatives."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'diffstrataudio/4t.mp3'\noutpoint 00:"+tstamp(17.5*timescale)+"00\n\n")

	


		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 diffstrategy.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
