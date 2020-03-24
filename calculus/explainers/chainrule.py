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
	timescale = 2.0


	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [1.0,8.0,5.0]
		twopages = False
		pages = [['text','equation'],[]]
		tstrc = r'\Huge\begin{center}The Chain Rule.\end{center}\Huge'
		tstr = [tstrc,tstrc,tstrc]
		estr = [r'',r'''\frac{d}{dx}[f(g(x))]&=\frac{d}{dg(x)}[f(g(x))]\frac{d}{dx}[g(x)]''',r'''\frac{d}{dx}[f(g(x))]&=\frac{d}{dg(x)}[f(g(x))]\frac{d}{dx}[g(x)]\\ \frac{d}{dx}[f(g(x))]&=f'(g(x))g'(x)''']
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'The definition of the chain rule is the most complicated because'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'we have to differentiate with respect to something other than x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'There is simply no friendly way to formally define the chain rule,'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'but think derivative of outside times derivative of inside.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1b.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,4.5,10.5,7.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'When to use the chain rule?'
		item1 = r'\setlength\itemsep{4em}\item No other rule works.'
		item2 = r'\item The function can be written as $f(g(x))$.'
		item3 = r'\item Do not use the chain rule until absolutely necessary.'
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

	caption = [2.0*timescale,'Try using all the other rules first.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If you really cannot use anything else, then the chain rule is there for you.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2a.mp3'\noutpoint 00:"+tstamp(5.500*timescale)+"00\n\n")

	caption = [3.5*timescale,'Any function can be written in this form by letting g(x)=x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'But we want both functions to be non-trivial. If you cannot find']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'such an f and g then the chain rule is not the right tool.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2b.mp3'\noutpoint 00:"+tstamp(10.500*timescale)+"00\n\n")

	caption = [3.5*timescale,'The chain rule is an example where putting off the hard part as long']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'as possible actually makes your life easier in the long-run.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2c.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [.5,4.5,4.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use the chain rule'
		item1 = r'\setlength\itemsep{1em}\item Identify the outside function.'
		item2 = r'\item Determine the inside function. \item Optional: Let $u=$ inside function and $f(u)=$ outside function. \item Differentiate the outside function. \item Differentiate the inside function. \item Multiply the two derivatives. '
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"The first step is most important so don't worry about anything else"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'until you know how to break up the function composition to find the ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [2.0*timescale,'outside and inside functions.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3.mp3'\noutpoint 00:"+tstamp(9.0*timescale)+"00\n\n")

	for framen in range(0,9):
		color = 'black'
		text = ''
		durations = [.5,4.0,4.5,11.5,7.0,.5,4.0,9.0,5.0]
		twopages = [.6,.375]
		pages = [['text'],['text']]

		headtxt = r'The \textcolor{red}{outside} function'
		item1 = r'\setlength\itemsep{2em}\item Function is not a sum, product, or quotient.'
		item2 = r'\item The outside function must be one of: '
		item3 = r'\begin{itemize} \item[] $f(u)=u^n$ \item[] $f(u)=a^u$ \item[] $f(u)=\log(u)$ \item[] $f(u)=\text{trig}(u)$ \end{itemize}'
		item4 = r'''\item Plug in 2, what's the last thing you do?'''
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr5,tstr5,tstr5,tstr5]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{2em} \item $h(x)=\sin(e^x-\ln(x))$ \item $h(x)=\ln(\sin(x)+x^2-7)$'
		item1a = r'\setlength\itemsep{1em} \item $h(x)=\sin(e^x-\ln(x))$ \begin{itemize} \color{blue}\item[] $f(u)=\sin(u)$\end{itemize} \item $h(x)=\ln(\sin(x)+x^2-7)$ \begin{itemize} \color{blue}\item[] $f(u)=\ln(u)$\end{itemize}'
		item2 = r'\item $h(x)=(x^2+e^x-\sin(x))^4$ \item $h(x)=2^{3x}$ '
		item2a = r'\item $h(x)=(x^2+e^x-\sin(x))^4$ \begin{itemize} \color{blue}\item[] $f(u)=u^4$\end{itemize} \item $h(x)=2^{3x}$ \begin{itemize} \color{blue}\item[] $f(u)=2^u$\end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'The hardest part of the chain rule is often undoing the composition. ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'Waiting to apply the chain rule and then looking for the outside function']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'makes this process quite easy. Because there are limited possibilities.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4a.mp3'\noutpoint 00:"+tstamp(11.500*timescale)+"00\n\n")

	caption = [4.5*timescale,'The outside function must be a power function, exponential function, ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'logarithmic function, or trigonometric function like sine, cosine, or tangent inverse.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4b.mp3'\noutpoint 00:"+tstamp(9.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'If you cannot determine the outside function, then try evaluating the function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The last step of the computation is the outside function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4c.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'Look at 4 examples. First look for trig functions and logarithms on the outside.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4d.mp3'\noutpoint 00:"+tstamp(4.500*timescale)+"00\n\n")

	caption = [3.5*timescale,'If it is neither, then it will be something raised to something.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If x is in the base, then it is a power function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If x is in the exponent, then it is an exponential function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If x is in both, then you need to use logarithmic differentiation.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4e.mp3'\noutpoint 00:"+tstamp(14.0*timescale)+"00\n\n")


	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [7.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use the chain rule'
		item1 = r'\setlength\itemsep{1.25em}\item Identify the outside function.'
		item2 = r'\item Determine the inside function. \item Optional: Let $u=$ inside function and $f(u)=$ outside function. \item Differentiate the outside function. \item Differentiate the inside function. \item Multiply the two derivatives. '
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'Now that we know the outside function, determine the inside function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'For simplicity we will replace the inside function with the letter u.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/5.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")


	for framen in range(0,8):
		color = 'black'
		text = ''
		durations = [.5,2.5,4.0,4.0,.5,3.0,3.5,3.5]
		twopages = [.6,.375]
		pages = [['text'],['text']]

		headtxt = r'The \textcolor{red}{inside} function'
		item1 = r'\setlength\itemsep{4em}\item Power function: inside is the base.'
		item2 = r'\item Exponential function: inside is the exponent. '
		item3 = r'\item Log or trig function: inside is the inside.'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr4,tstr4,tstr4,tstr4]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{2em} \item $h(x)=\sin(e^x-\ln(x))$ \item $h(x)=\ln(\sin(x)+x^2-7)$'
		item1a = r'\setlength\itemsep{1em} \item $h(x)=\sin(e^x-\ln(x))$ \begin{itemize} \color{blue}\item[] $u=e^x-\ln(x)$\end{itemize} \item $h(x)=\ln(\sin(x)+x^2-7)$ \begin{itemize} \color{blue}\item[] $u=\sin(x)+x^2-7$\end{itemize}'
		item2 = r'\item $h(x)=(x^2+e^x-\sin(x))^4$ \item $h(x)=2^{3x}$ '
		item2a = r'\item $h(x)=(x^2+e^x-\sin(x))^4$ \begin{itemize} \color{blue}\item[] $u=x^2+e^x-\sin(x)$\end{itemize} \item $h(x)=2^{3x}$ \begin{itemize} \color{blue}\item[] $u=3x$\end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,'The inside function is going to be the rest of the function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6a.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'For power and exponential functions, the inside is the non-constant part.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'For trig and logs, the inside function should be in parentheses.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6b.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'For these examples the inside functions should be easy to spot once']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'you know the outside function. If the inside function is not clear,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'you may have picked the wrong outside function.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6c.mp3'\noutpoint 00:"+tstamp(10.500*timescale)+"00\n\n")


	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [14.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use the chain rule'
		item1 = r'\setlength\itemsep{1.25em}\item Identify the outside function.'
		item2 = r'\item Determine the inside function. \item Optional: Let $u=$ inside function and $f(u)=$ outside function. \item Differentiate the outside function. \item Differentiate the inside function. \item Multiply the two derivatives. '
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'Now it is time to start differentiating.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'There are only a few choices for the outside function and the derivative is easy.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The inside function can be anything so differentiate it carefully.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Once you have differentiated both functions, multiply the derivatives.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/7.mp3'\noutpoint 00:"+tstamp(14.0*timescale)+"00\n\n")

	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [.5,2.0,2.0,.5,6.0,6.5]
		twopages = [.49,.49]
		pages = [['text'],['text']]

		headtxt = r''
		item1 = r'\setlength\itemsep{2em} \item $h(x)=g(x)^n$ \item $h(x)=e^{g(x)}$'
		item1a = r'''\setlength\itemsep{.5em} \item $h(x)=g(x)^n$ \begin{itemize} \color{blue} \item[] $\frac{d}{dx}[h(x)]=ng(x)^{n-1}g'(x)$\end{itemize} \item $h(x)=e^{g(x)}$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=g'(x)e^{g(x)}$\end{itemize}'''
		item2 = r'\item $h(x)=\ln(g(x))$ \item $h(x)=\tan(g(x))$ '
		item2a = r'''\item $h(x)=\ln(g(x))$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=\frac{g'(x)}{g(x)}$\end{itemize} \item $h(x)=\tan(g(x))$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=\sec^2(g(x))g'(x)$\end{itemize}'''
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr3,tstr3,tstr3]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{2em} \item $h(x)=(x^2+1)^{10}$ \item $h(x)=e^{\sin(x)}$'
		item1a = r'\setlength\itemsep{.5em} \item $h(x)=(x^2+1)^{10}$ \begin{itemize} \color{blue} \item[] $\frac{d}{dx}[h(x)]=10(x^2+1)^9(2x)$\end{itemize} \item $h(x)=e^{\sin(x)}$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=\cos(x)e^{\sin(x)}$\end{itemize}'
		item2 = r'\item $h(x)=\ln(x^4-x)$ \item $h(x)=\sec(2x)$ '
		item2a = r'\item $h(x)=\ln(x^4-x)$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=\frac{4x^3-1}{x^4-x}$\end{itemize} \item $h(x)=\sec(2x)$ \begin{itemize} \color{blue}\item[] $\frac{d}{dx}[h(x)]=2\sec(2x)\tan(2x)$\end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2a+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',tstr1,tstr2,tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [2.0*timescale,'There are four types of outside functions.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [2.0*timescale,'We see how the chain rule works for each type.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/8a.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'Just be careful because the inside function is often somewhat messy.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'For logarithms, the entire inside function goes in the denominator, not just x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'For secant, the inside function must be repeated in secant and tangent.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/8b.mp3'\noutpoint 00:"+tstamp(13.500*timescale)+"00\n\n")

	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [5.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'Further Investigations'
		item1 = r'\setlength\itemsep{2.5em}\item What is $\frac{d}{dx}[\ln(ax)]$?'
		item2 = r'\item What is $\frac{d}{dx}\left[\sqrt{\sin^2(x)+1}\right]$? \item Use the chain rule to differentiate $h(x)=3x^2$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [5.0*timescale,'Think about these quesitons.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/9.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")
		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -c:v libx264 -preset veryslow -crf '+str(sys.argv[1])+' -tune stillimage -r 8 chainrule.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
