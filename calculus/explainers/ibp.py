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
				thestr += makeequation(estr[framen],2.0)
		thestr += r'''\end{minipage}\hfill'''
		thestr += r'''\begin{minipage}{'''+str(twopages[1])+r'''\linewidth}'''
		for page in pages[1]:
			if page == 'text':
				thestr += maketext(tstr[1][framen])
			if page == 'equation':
				thestr += makeequation(estr[framen],2.0)
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
	\usepackage{color}
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
		durations = [1.0,8.0,8.5]
		twopages = False
		pages = [['text'],[]]
		headtxt = r'Integration by Parts'
		item1 = r'\setlength\itemsep{4em}\item Undo the product rule of differentiation.'
		item2 = r'\item $\displaystyle\int f(x)dx=\displaystyle\int u dv=uv-\displaystyle\int v du$'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'

		tstr = [tstr1,tstr2,tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Integration by parts undoes the product rule. Understanding where'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'integration by parts comes from will make it easier to remember and apply.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/1a.mp3'\noutpoint 00:"+tstamp(7.5*timescale)+"00\n\n")

	caption = [3.5*timescale,"While using the product rule to differentiate is not too hard, it"] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'is generally the hardest to undo because of the two terms.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/1b.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,4.5,10.5,7.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'When to use integration by parts?'
		item1 = r'\setlength\itemsep{4em}\item Nothing else works.'
		item2 = r'\item One of the factors is possible to integrate.'
		item3 = r'\item Might need to be creative about factors.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [4.0*timescale,'Other integration methods are usually easier to identify.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'Composition is probably u-substitution. Multiple or complicated trigonometric']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'functions probably require some trigonometric method.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"Rational functions use partial fractions. If the integral doesn't seem to fit"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'another method, then try integration by parts.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/2a.mp3'\noutpoint 00:"+tstamp(20.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Integration by parts requires integrating one factor of the expression, so']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'if the expression is a product and you know how to integrate at least one']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'of the factors, then integration by parts is likely the right tool.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/2b.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [4.0*timescale,'Sometimes the factorization will not be obvious. One of the factors might']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'simply be 1. Or one factor may require multiplying or dividing in order to']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"make the integration possible. So don't give up on integration by parts just because" ]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'the most obvious choices for u and dv do not work out.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/2c.mp3'\noutpoint 00:"+tstamp(16.0*timescale)+"00\n\n")

	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [.5,5.0,6.0,5.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use integration by parts'
		item1 = r'\setlength\itemsep{1.75em}\item Find $u$ and $dv$.'
		item2 = r'\item Compute $du$. \item Compute $v$.'
		item3 = r'\item Compute $\displaystyle\int v du$. \item Compute $uv - \displaystyle\int v du$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"The first step is finding the right u and dv."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Without good choices for this pair the rest of the process doesn't matter"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/3a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Once we have u and dv we need to find du and v.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'If you cannot get du and v then you need to return to step 1']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"and select a different u and dv. It's okay to try multiple pairs until one works."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/3b.mp3'\noutpoint 00:"+tstamp(13.0*timescale)+"00\n\n")

	caption = [3.5*timescale,"Then compute the new integral and apply integration by parts."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/3c.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	for framen in range(0,10):
		color = 'black'
		text = ''
		durations = [.5,2.0,1.0,5.0,5.0,.5,4.0,5.0,1.0,1.0,1.0,1.0]
		twopages = [.55,.43]
		pages = [['text'],['text']]

		headtxt = r'How to find $u$ and $dv$'
		item1 = r'\setlength\itemsep{.5em}\item Want $u$ to have simplest possible derivative. \item Need $dv$ to be possible to integrate.'
		item2 = r'\item Pick $u$ using ILATE.'
		item3 = r'\begin{itemize} \item[] Inverse trigonometric \item[] Logarithmic \item[] Algebraic \item[] Trigonometric \item[] Exponential \end{itemize}'
		item4 = r'''\item Check that $dv$ can be integrated.'''
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{2em}\item $\displaystyle\int x\ln(x)dx$'
		item2 = r'\begin{itemize} \item[] $u=\ln(x)$ \item[] $dv=xdx$ \end{itemize}'
		item3 = r'''\item $\displaystyle\int x^2\sin(x) dx$'''
		item4 = r'\begin{itemize} \item[] $u=x^2$ \item[] $dv=\sin(x)dx$ \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'We generally look for two things when searching for u and dv.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'Because we will eventually need to integrate vdu, we need to']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"be able to determine what v is by integrating dv and it is helpful if"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]
	
	caption = [4.0*timescale,'du does not make the integral any harder than it already is.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4b.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'The guide that can help pick u is to let u be an inverse trigonometric function']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'if there is one in the integral. Otherwise look for a logarithm and then an algebraic function']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"like a polynomial. If you don't have u yet then it will be either trigonometric or exponential."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4c.mp3'\noutpoint 00:"+tstamp(15.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"Once you have u then dv is the rest of the expression. If you do not know how"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"to integrate dv, then pick a different choice for u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4d.mp3'\noutpoint 00:"+tstamp(7.5*timescale)+"00\n\n")

	caption = [5.5*timescale,"In this example, x is algebraic and ln(x) is logarithmic so let u be ln(x)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"That makes dv=xdx which we know how to integrate so we've probably made the right choice."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4e.mp3'\noutpoint 00:"+tstamp(11.5*timescale)+"00\n\n")

	caption = [4.5*timescale,"In this example x^2 is algebraic and sin(x) is trigonometric so let"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"u be x^2. Then dv is sin(x)dx. Both x^2 and sin(x) are possible to integrate,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"but differentiating x^2 will make the next step easier. That is why algebraic functions"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,"are better chioces for u than trigonometric functions."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4f.mp3'\noutpoint 00:"+tstamp(19.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"Most problems in a calculus class will be designed so that knowing ILATE"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"will make the selection of u and dv fairly easy. Then the fun really begins."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/4g.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")






	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [5.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use integration by parts'
		item1 = r'\setlength\itemsep{1.75em}\item Find $u$ and $dv$.'
		item2 = r'\item Compute $du$. \item Compute $v$.'
		item3 = r'\item Compute $\displaystyle\int v du$. \item Compute $uv - \displaystyle\int v du$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [4.0*timescale,"The next step is to compute du and v. Generally these should be fairly easy,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"but being sloppy with notation or working too fast without thinking about"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'what you are doing will create several opportunities for errors.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/5a.mp3'\noutpoint 00:"+tstamp(11.0*timescale)+"00\n\n")



	for framen in range(0,8):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.45,.53]
		pages = [['text'],['text']]

		headtxt = r'How to compute $du$ and $v$'
		item1 = r'''\setlength\itemsep{3em}\item $\displaystyle\frac{du}{dx}=u'(x)$ so $du=u'(x)dx$'''
		item2 = r'\item $v=\displaystyle\int dv$'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr3,tstr3,tstr3,tstr3,tstr3]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{2em}\item $u=\ln(x)$ and $dv=xdx$'
		item2 = r'\begin{itemize} \item[] $du=\frac{1}{x}dx$ \item[] $v=\int xdx=\frac{x^2}{2}$ \end{itemize}'
		item3 = r'''\item $u=x^2$ and $dv=\sin(x)dx$'''
		item4 = r'\begin{itemize} \item[] $du=2xdx$ \item[] $v=\int \sin(x)dv=-\cos(x)$ \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,"Differentiate u to get du."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/6a.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [3.0*timescale,"Integrate dv to get v."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/6b.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"Be careful to differentiate when you are supposed to differentiate."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"Especially with simple functions it can be easy to automatically see"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,"something like 2x and think x^2, but for this one step differentiation is required."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/6c.mp3'\noutpoint 00:"+tstamp(12.5*timescale)+"00\n\n")

	caption = [5.0*timescale,"Let's use u=ln(x) and dv=xdx as an example."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"The derivative of ln(x) is 1/x so du=1/xdx."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"And the integral of xdx is x^2/2 so that is v."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/6d.mp3'\noutpoint 00:"+tstamp(15.0*timescale)+"00\n\n")

	caption = [5.5*timescale,"Now let u=x^2 and dv=sin(x)dx."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.5*timescale,"The derivative of x^2 is 2x so du=2xdx. The integral of sin(x) is -cos(x)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"Remember that the derivative of sine is cosine, but the integral is negated,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,"so always think about whether you are integrating or differentiating trig functions."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/6e.mp3'\noutpoint 00:"+tstamp(21.0*timescale)+"00\n\n")


	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [5.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use integration by parts'
		item1 = r'\setlength\itemsep{1.75em}\item Find $u$ and $dv$.'
		item2 = r'\item Compute $du$. \item Compute $v$.'
		item3 = r'\item Compute $\displaystyle\int v du$. \item Compute $uv - \displaystyle\int v du$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"All that's left now is integrating the new integral of vdu."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Hopefully the new integral is a simpler function than the old integral."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'You might need to apply integration by parts again or a u-substitution,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'but it should be easier than the original.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/7a.mp3'\noutpoint 00:"+tstamp(13.5*timescale)+"00\n\n")





	for framen in range(0,9):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.72,.25]
		pages = [['equation'],['text']]


		estr = [r'''\displaystyle\int x^n\ln(x)dx&=''']
		estr.append(estr[0]+r'''uv - \displaystyle\int v du''')
		estr.append(estr[1])
		estr.append(estr[1])
		estr.append(estr[1])
		estr.append(estr[4]+r'''\\ &=\ln(x)\frac{x^{n+1}}{n+1} - \displaystyle\int \frac{x^{n+1}}{n+1}\cdot \frac{1}{x}dx''')
		estr.append(estr[5]+r'''\\ &=\ln(x)\frac{x^{n+1}}{n+1} - \displaystyle\int \frac{x^{n}}{n+1}dx''')
		estr.append(estr[6]+r'''\\ &=\ln(x)\frac{x^{n+1}}{n+1} - \frac{x^{n+1}}{(n+1)^2}+\text{C}''')
		estr.append(estr[7]+r'''\\ &=\frac{x^{n+1}}{n+1}(\ln(x)-\frac{1}{n+1})+\text{C}''')

		headtxt = r''
		item1 = r'\setlength\itemsep{1em}\item $u=\ln(x)$'
		item2 = r'\item $du=$'
		item2a = r'\item $du=\frac{1}{x}dx$'

		itemb = r'\item[] '

		item3 = r'''\item $dv=x^ndx$'''
		item4 = r'\item $v=$'
		item4a = r'\item $v=\frac{x^{n+1}}{n+1}$'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2+itemb+itemb+item3+item4+r'\end{itemize}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2a+itemb+itemb+item3+item4+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2a+itemb+itemb+item3+item4a+r'\end{itemize}'
		tstr = [r'',r'',tstr1,tstr2,tstr3,tstr3,tstr3,tstr3,tstr3]

		
		makestr(twopages,startstr,pages,[[],tstr],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,"Let's integrate x^n times ln(x)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"We're going to need to use integration by parts."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8a.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'We set u equal to ln(x) and then dv is x^ndx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8b.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'Thus du is 1/x dx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'And v is x^(n+1) over n+1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8d.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'Then we compute uv minus the integral of vdu.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The integral of a power function is easy to compute.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8e.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [6.0*timescale,'Then we can simplify by factoring out x^(n+1) over n+1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,'By setting n=0 we can see that the integral of ln(x) is x times ln(x)-1.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/8f.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")



	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.72,.25]
		pages = [['equation'],['text']]


		estr = [r'''\displaystyle\int x^n\sin(x)dx&=''']
		estr.append(estr[0]+r'''uv - \displaystyle\int v du''')
		estr.append(estr[1])
		estr.append(estr[1])
		estr.append(estr[1])
		estr.append(estr[4]+r'''\\ &=-x^n\cos(x) - \displaystyle\int -n\cos(x)x^{n-1}dx''')

		headtxt = r''
		item1 = r'\setlength\itemsep{1em}\item $u=x^n$'
		item2 = r'\item $du=$'
		item2a = r'\item $du=nx^{n-1}dx$'

		itemb = r'\item[] '

		item3 = r'''\item $dv=\sin(x)dx$'''
		item4 = r'\item $v=$'
		item4a = r'\item $v=-\cos(x)$'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2+itemb+itemb+item3+item4+r'\end{itemize}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2a+itemb+itemb+item3+item4+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+item2a+itemb+itemb+item3+item4a+r'\end{itemize}'
		tstr = [r'',r'',tstr1,tstr2,tstr3,tstr3]

		
		makestr(twopages,startstr,pages,[[],tstr],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,"Let's integrate x^n times sin(x)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [2.0*timescale,"We're going to need to use integration by parts."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9a.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'We set u equal to x^n this time and then dv is sin(x)dx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9b.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [5.0*timescale,'Thus du is nx^(n-1) dx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9c.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'And v is -cos(x)dx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9d.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	caption = [4.0*timescale,'Then we compute uv minus the integral of vdu.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9e.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'The integral of -ncos(x)x^(n-1) is still hard to determine,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'but the power of x has decreased. Using integration by parts again']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'will reduce the power by 1 more. Assuming n is a positive integer, eventually the ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'exponent will be 0 and we know the integral of both sine and cosine.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9f.mp3'\noutpoint 00:"+tstamp(18.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'What is the integral of x^2 times sin(x)?']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9g.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'To make sure you have the right answer, remember you can take the derivative ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'of your answer to make sure it matches the original function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'ibpaudio/9h.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 ibp.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
