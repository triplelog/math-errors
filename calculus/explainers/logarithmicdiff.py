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
	timescale = 1.0


	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [1.0,8.0,8.5]
		twopages = False
		pages = [['text','equation'],[]]
		tstrc = r'\Huge\begin{center}Logarithmic Differentiation.\end{center}\Huge'
		tstr = [tstrc,tstrc,tstrc]
		estr = [r'',r'''\frac{d}{dx}[\ln(f(x))]&=\frac{f'(x)}{f(x)}''',r'''\frac{d}{dx}[\ln(f(x))]&=\frac{f'(x)}{f(x)}\\ f'(x)&=f(x)\frac{d}{dx}[\ln(f(x))]''']
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Logarithmic differentiation offers an alternative function to differentiate.'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'From the chain rule we know the derivative of the ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"natural logarithm of f(x) in terms of f(x) and f'(x)."] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	caption = [3.5*timescale,'If differentiating the natural log of f(x) is easier,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'then use logarithmic differentiation.']
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

		headtxt = r'When to use logarithmic differentiation?'
		item1 = r'\setlength\itemsep{4em}\item Required: $f(x)=a(x)^{b(x)}$'
		item2 = r'\item Recommended: $f(x)=\frac{a(x)b(x)c(x)}{d(x)}$'
		item3 = r'\item Discouraged: $f(x)=\ln(x)$'
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

	caption = [3.5*timescale,'If the function is a power and neither the base nor the exponent'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'are constant, then logarithmic differentiation is your only option.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'If the function is a product or quotient of several factors,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'then logarithmic differentiation will be faster and easier.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'The product rule gets messier with more factors,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'while the sum rule does not.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2b.mp3'\noutpoint 00:"+tstamp(14.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Despite the name, logarithmic differentiation is not used to']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'differentiate logarithms. It will work on any function,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'but using it will just make the differentiation harder.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/2c.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [.5,20.0,6.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use logarithmic differentiation'
		item1 = r'\setlength\itemsep{3em}\item Take the natural logarithm of the function. \item Apply properties of logarithms.'
		item2 = r'\item Differentiate the new function. \item Multiply by the original function. '
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"The first step is taking the natural logarithm of f(x)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Then the entire reason for using logarithmic differentiation is ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'that logarithms have some nice properties.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3a.mp3'\noutpoint 00:"+tstamp(10.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Bring exponents to the front of the logarithm and break']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'up products into sums of logarithms.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"If you don't use any logarithm properties, then you"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'have simply made the differentiation harder.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3b.mp3'\noutpoint 00:"+tstamp(13.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'Only later will we worry about differentiating.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	for framen in range(0,12):
		color = 'black'
		text = ''
		durations = [.5,2.0,1.0,5.0,5.0,.5,4.0,5.0,1.0,1.0,1.0,1.0]
		twopages = [.45,.53]
		pages = [['text'],['text']]

		headtxt = r'What are the properties of logarithms?'
		item1 = r'\Large\setlength\itemsep{2em}\item $f(x)=a(x)^{b(x)}$'
		item2 = r'\begin{itemize} \item[] $\ln(f(x))=\ln(a(x)^{b(x)})$ \end{itemize}'
		item3 = r'\begin{itemize} \item[] $\ln(f(x))=\ln(a(x)^{b(x)})$ \item[] $\ln(f(x))=b(x)\ln(a(x))$ \end{itemize}'
		item4 = r'''\item $f(x)=\frac{a(x)b(x)c(x)}{d(x)}$'''
		item5 = r'\begin{itemize} \item[] $\ln(f(x))=\ln\left(\frac{a(x)b(x)c(x)}{d(x)}\right)$ \end{itemize}'
		item6 = r'\begin{itemize} \item[] $\ln(f(x))=\ln\left(\frac{a(x)b(x)c(x)}{d(x)}\right)$ \item[] $\ln(f(x))=\ln(a(x))+\ln(b(x))+\ln(c(x))-\ln(d(x))$ \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item3+item4+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item3+item4+item5+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item3+item4+item6+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr7,tstr7,tstr7,tstr7,tstr7]
		estr = []

		headtxt = r''
		item1 = r'\Large\setlength\itemsep{2em}\item $f(x)=x^x$'
		item2 = r'\begin{itemize} \item[] $\ln(f(x))=\ln(x^x)$ \item[] $\ln(f(x))=x\ln(x)$ \end{itemize}'
		item3 = r'''\item $f(x)=\frac{(x+1)(2x+1)(x-3)}{x-4}$'''
		item4 = r'\begin{itemize} \item[] $\ln(f(x))=\ln\left(\frac{(x+1)(2x+1)(x-3)}{x-4}\right)$ \item[] $\ln(f(x))=\ln(x+1)+\ln(2x+1)+\ln(x-3)-\ln(x-4)$ \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'We really want to get rid of the exponent, so']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'we take the logarithm and then bring the b(x) in front.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"We really don't want to apply the product and quotient rule multiple times,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	
	caption = [4.5*timescale,'so we take the logarithm and then take the sum of log of a(x) plus log of']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'b(x) plus log of c(x) minus log of d(x) because it was in the denominator.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4b.mp3'\noutpoint 00:"+tstamp(13.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'In these examples we see the same properties are used,']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'and the result is functions that are easy to differentiate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/4c.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")



	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [16.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use logarithmic differentiation'
		item1 = r'\setlength\itemsep{3em}\item Take the natural logarithm of the function. \item Apply properties of logarithms.'
		item2 = r'\item Differentiate the new function. \item Multiply by the original function. '
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr = [tstr3]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"After applying properties of logarithms, your function"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'might look uglier but it will be easier to differentiate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'We will be able to use the product or sum rules.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'The hardest part is keeping track of every step so']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'make sure you know exactly what you are doing and why at all times.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/5.mp3'\noutpoint 00:"+tstamp(16.0*timescale)+"00\n\n")



	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [.5,2.5,4.0,4.0,.5,3.0,3.5,3.5]
		twopages = False
		pages = [['equation']]

		headtxt = r''

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr = [tstr1,tstr1,tstr1,tstr1,tstr1,tstr1,tstr1]
		estr = [r'''\frac{d}{dx}[a(x)^{b(x)}]&=a(x)^{b(x)}\frac{d}{dx}[\ln(a(x)^{b(x)})]''',r'''\frac{d}{dx}[a(x)^{b(x)}]&=a(x)^{b(x)}\frac{d}{dx}[\ln(a(x)^{b(x)})]\\ &=a(x)^{b(x)}\frac{d}{dx}[b(x)\ln(a(x))]''']
		estr.append(estr[1]+r'''\\ &=a(x)^{b(x)}\left(b(x)\frac{a'(x)}{a(x)}+b'(x)\ln(a(x))\right)''')
		estr.append(estr[2]+r'''\\ \\ \frac{d}{dx}[(x+1)^{2x}]&=(x+1)^{2x}\frac{d}{dx}[\ln((x+1)^{2x})]''')
		estr.append(estr[3]+r'''\\ &=(x+1)^{2x}\frac{d}{dx}[2x\ln(x+1)]''')
		estr.append(estr[4]+r'''\\ &=(x+1)^{2x}\left(\frac{2x}{x+1}+2\ln(x+1)\right)''')

		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,'The derivative of a(x) to the b(x) will be a(x) to the b(x)']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6a.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	caption = [4.0*timescale,'times the derivative of log of a(x) to the b(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"Don't forget to multiply by the original function."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6b.mp3'\noutpoint 00:"+tstamp(8.0*timescale)+"00\n\n")

	caption = [3.5*timescale,'Apply the properties of logarithms.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Then differentiate using the product rule. Be careful because']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'this derivative will be tricky, involving the chain rule for ln(a(x)).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Let's look at (x+1) to the 2x power. Usually the functions will"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"be relatively simple because the derivative will still be complicated."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/6c.mp3'\noutpoint 00:"+tstamp(10.500*timescale)+"00\n\n")


	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [.5,2.5,4.0,4.0,.5,3.0,3.5,3.5]
		twopages = False
		pages = [['equation']]

		headtxt = r'Examples'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large'
		tstr = [tstr1,tstr1,tstr1,tstr1,tstr1,tstr1,tstr1]
		estr = [r'''\frac{d}{dx}\left[\frac{a(x)b(x)c(x)}{d(x)}\right]&=\frac{a(x)b(x)c(x)}{d(x)}\frac{d}{dx}\left[\ln(\frac{a(x)b(x)c(x)}{d(x)})\right]''',r'''\frac{d}{dx}\left[\frac{a(x)b(x)c(x)}{d(x)}\right]&=\frac{a(x)b(x)c(x)}{d(x)}\frac{d}{dx}\left[\ln(\frac{a(x)b(x)c(x)}{d(x)})\right]\\ &=\frac{a(x)b(x)c(x)}{d(x)}\frac{d}{dx}\left[\ln\left(a(x))+\ln(b(x))+\ln(c(x))-\ln(d(x)\right)\right]''']
		estr.append(estr[1]+r'''\\ &=\frac{a(x)b(x)c(x)}{d(x)}(\frac{a'(x)}{a(x)}+\frac{b'(x)}{b(x)}+\frac{c'(x)}{c(x)}-\frac{d'(x)}{d(x)})''')
		estr.append(estr[2]+r'''\\ \\ \frac{d}{dx}\left[\frac{(x+1)(2x+1)(x-3)}{x-4}\right]&=\frac{(x+1)(2x+1)(x-3)}{x-4}\frac{d}{dx}\left[\ln\left(\frac{(x+1)(2x+1)(x-3)}{x-4}\right)\right]''')
		estr.append(estr[3]+r'''\\ &=\frac{(x+1)(2x+1)(x-3)}{x-4}\frac{d}{dx}[\ln(x+1)+\ln(2x+1)+\ln(x-3)-\ln(x-4)]''')
		estr.append(estr[4]+r'''\\ &=\frac{(x+1)(2x+1)(x-3)}{x-4}\left(\frac{1}{x+1}+\frac{2}{2x+1}+\frac{1}{x-3}-\frac{1}{x-4}\right)''')

		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"Let's differentiate a long product and quotient."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Don't forget to multiply by the original function."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Remember to subtract ln(d(x)).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Then correctly apply the chain rule for logarithms four times.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'For this function be careful because the derivative of most, ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'but not all, factors is 1. Never forget the chain rule.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/7.mp3'\noutpoint 00:"+tstamp(14.0*timescale)+"00\n\n")

	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [.5,2.5,4.0,4.0,.5,3.0,3.5,3.5]
		twopages = False
		pages = [['text']]

		headtxt = r'Homework'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge \begin{itemize} \item Use logarithmic differentiation for \frac{d}{dx}[f(x)g(x)]\item Use logarithmic differentiation for \frac{d}{dx}\left[\frac{f(x)}{g(x)}\right]\item Use logarithmic differentiation for \frac{d}{dx}[a^x]\end{itemize} '
		tstr = [tstr1]
		estr = []

		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [2.0*timescale,'Do these correctly and the answers should be familar.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [2.0*timescale,'If you ever forget the quotient rule, ']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,'you can now use logarithmic differentiation instead.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/8.mp3'\noutpoint 00:"+tstamp(13.500*timescale)+"00\n\n")

	


		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 logarithmicdiff.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
