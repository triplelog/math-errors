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


	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,8.0,8.5,5.0]
		twopages = False
		pages = [['text'],[]]
		headtxt = r'U substitution'
		item1 = r'\setlength\itemsep{4em}\item Undo the chain rule of differentiation.'
		item2 = r'''\item $\displaystyle\int f'(x)g'(f(x))dx=g(f(x))+\text{C}$'''
		item3 = r'''\item $\displaystyle\int g'(u)du=g(u)+\text{C}$'''
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'

		tstr = [tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'U substitution undoes the chain rule. We need to identify the'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'function composition within the integral so that we can integrate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Most functions with composition will require u substitution.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/1a.mp3'\noutpoint 00:"+tstamp(11.0*timescale)+"00\n\n")



	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [.5,5.0,6.0,5.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use u-substitution'
		item1 = r'\setlength\itemsep{1.75em}\item Pick $u=u(x)$.'
		item2 = r"\item Find $du=u'(x)dx$."
		item3 = r'\item Replace $x$ and $dx$ with $u$ and $du$.'
		item4 = r'\item Integrate with respect to $u$. \item Replace $u$ with $u(x)$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,"The first step is finding the right u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"Without the right u the rest of the process doesn't matter"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/2a.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'Once we have u we need to find du.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,'If you cannot replace all of x then you need to return to step 1']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"and select a different u. It's okay to try multiple times until one works."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/2b.mp3'\noutpoint 00:"+tstamp(11.0*timescale)+"00\n\n")

	caption = [3.5*timescale,"Then compute the new integral and substitute the x back in."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/2c.mp3'\noutpoint 00:"+tstamp(3.5*timescale)+"00\n\n")

	for framen in range(0,14):
		color = 'black'
		text = ''
		durations = [.5,2.0,1.0,5.0,5.0,.5,4.0,5.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
		twopages = [.55,.43]
		pages = [['text'],['text']]

		headtxt = r'How to pick $u$'
		item1 = r'\setlength\itemsep{1.5em}\item Look at the inside of parentheses.'
		item2 = r'\item Look at denominators.'
		item3 = r'\item Look inside square roots.'
		item4 = r'\item Look in exponents.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5]
		estr = []

		headtxt = r''
		item1 = r'\setlength\itemsep{.1em}\item $\int \sin(5x)dx$'
		item2 = r'\begin{itemize} \item[] $u=5x$ \end{itemize}'
		item3 = r'\item $\int \frac{\sin(x)}{\cos(x)}dx$'
		item4 = r'\begin{itemize} \item[] $u=\cos(x)$ \end{itemize}'
		item5 = r'\item $\int x^2\sqrt{x^3+1}dx$'
		item6 = r'\begin{itemize} \item[] $u=x^3+1$ \end{itemize}'
		item7 = r'\item $\int xe^{x^2-1}dx$'
		item8 = r'\begin{itemize} \item[] $u=x^2-1$ \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+item7+r'\end{itemize}'
		tstr9 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+item7+item8+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8,tstr9]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,'The u is going to be the inside function of a composition.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'So the inside of a set of parentheses is a good place to look.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"Also denominators, square roots, and exponents."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/3a.mp3'\noutpoint 00:"+tstamp(10.0*timescale)+"00\n\n")
	
	caption = [4.0*timescale,'To integrate sin(5x) we let u=5x.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/3b.mp3'\noutpoint 00:"+tstamp(4.0*timescale)+"00\n\n")

	caption = [4.5*timescale,'To integrate sin(x) over cos(x) we let u=cos(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [5.0*timescale,'Of course, when integrating tan(x) it may not be as obvious to let u=cos(x).']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,"Sometimes rewriting the integral will make the choice of u more obvious."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/3c.mp3'\noutpoint 00:"+tstamp(14.0*timescale)+"00\n\n")

	caption = [6.0*timescale,"To integrate x^2 times the square root of x^3+1, let u=x^3+1."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/3d.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")

	caption = [5.5*timescale,"And to integrate xe^{x^2-1} let u equal x^2-1."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/3e.mp3'\noutpoint 00:"+tstamp(5.5*timescale)+"00\n\n")




	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [3.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use u-substitution'
		item1 = r'\setlength\itemsep{1.75em}\item Pick $u=u(x)$.'
		item2 = r"\item Find $du=u'(x)dx$."
		item3 = r'\item Replace $x$ and $dx$ with $u$ and $du$.'
		item4 = r'\item Integrate with respect to $u$. \item Replace $u$ with $u(x)$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.0*timescale,"If you believe you have a good choice for u, the next step"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"is to differentiate u to find du."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/4a.mp3'\noutpoint 00:"+tstamp(6.0*timescale)+"00\n\n")



	for framen in range(0,11):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.55,.43]
		pages = [['text'],['text']]

		headtxt = r'How to compute $du$'
		item1 = r'''\setlength\itemsep{3em}\item $\frac{du}{dx}$ is the derivative of $u$ with respect to $x$.'''
		item2 = r"\item $\frac{du}{dx}=u'(x)$"
		item3 = r"\item $du=u'(x)dx$"
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr4,tstr4,tstr4,tstr4,tstr4,tstr4,tstr4]
		estr = []

		headtxt = r''
		
		item3 = r'\setlength\itemsep{3em}\item $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx$'
		item4 = r'\begin{itemize} \item[] $u=\cos(x)$ \end{itemize}'
		item4a = r'\begin{itemize} \item[] $u=\cos(x)$ \item[] $du=-\sin(x)dx$  \end{itemize}'
		item1 = r'\item $\displaystyle\int \sin(5x)dx$'
		item2 = r'\begin{itemize} \item[] $u=5x$ \end{itemize}'
		item2a = r'\begin{itemize} \item[] $u=5x$ \item[] $du=5dx$  \end{itemize}'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item3+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4a+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4a+item1+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4a+item1+item2+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4a+item1+item2a+r'\end{itemize}'
		tstrp2 = [r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [4.0*timescale,"Differentiate u to get du. Remember to take the derivative not the integral."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"In particular, it can be easy to automatically integrate simple functions"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"if you are not taking your time and thinking about what you are doing."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"Generally this derivative will be fairly easy."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/5a.mp3'\noutpoint 00:"+tstamp(15.0*timescale)+"00\n\n")

	caption = [7.0*timescale,"The derivative of cos(x) is -sin(x) so du equals -sin(x)dx."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/5b.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [4.5*timescale,"And the derivative of 5x is 5 so du is 5dx."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/5c.mp3'\noutpoint 00:"+tstamp(4.5*timescale)+"00\n\n")


	for framen in range(0,1):
		color = 'black'
		text = ''
		durations = [3.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'How to use u-substitution'
		item1 = r'\setlength\itemsep{1.75em}\item Pick $u=u(x)$.'
		item2 = r"\item Find $du=u'(x)dx$."
		item3 = r'\item Replace $x$ and $dx$ with $u$ and $du$.'
		item4 = r'\item Integrate with respect to $u$. \item Replace $u$ with $u(x)$.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr = [tstr1]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [3.5*timescale,"The next step can be really easy or a bit tricky."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,"In order to integrate, the integral needs to be entirely in terms of u and du"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,'instead of x and dx.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/6a.mp3'\noutpoint 00:"+tstamp(10.0*timescale)+"00\n\n")





	for framen in range(0,12):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.45,.53]
		pages = [['text'],['text']]

		headtxt = r'How to replace $x$ and $dx$'
		item1 = r'''\setlength\itemsep{2em}\item Try to replace $u'(x)dx$ with $du$.'''
		item2 = r"\item Or replace $dx$ with $\frac{du}{u'(x)}$"
		item3 = r"\item Replace $u(x)$ with u."
		item4 = r"\item Replace all remaining $x$'s."
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5,tstr5]
		estr = []

		headtxt = r''
		
		item3 = r'\setlength\itemsep{1em}\item $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx$'
		item4 = r'\begin{itemize} \item[] $u=\cos(x)$ \item[] $du=-\sin(x)dx$ \end{itemize}'
		item3a = r'\setlength\itemsep{1em}\item  $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx=\displaystyle\int \frac{du}{u}$'
		item1 = r'\item $\displaystyle\int \sin(5x)dx$'
		item2 = r'\begin{itemize} \item[] $u=5x$ \item[] $du=5dx$  \end{itemize}'
		item1a = r'\item $\displaystyle\int \sin(5x)dx=\displaystyle\int \frac{1}{5}\sin(u)du$'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize}  '+item3+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3+item4+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3a+item4+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3a+item4+item1+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3a+item4+item1+item2+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item3a+item4+item1a+item2+r'\end{itemize}'

		tstrp2 = [r'',r'',r'',r'',r'',tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7]
		estr = []
		
		makestr(twopages,startstr,pages,[tstrp1,tstrp2],estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [7.0*timescale,"First replace dx. Often replacing the derivative of u times dx with du is possible."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7a.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [3.5*timescale,"If not, you may need to try solving for dx. But this will add more expressions of x"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"to get rid of in the next steps."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7b.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")

	caption = [5.0*timescale,"Once the integral has du instead of dx, then insert u where it came from."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7c.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"At this point, hopefully there are no more x's. But if another x remains,"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"it must be removed before integrating. How to eliminate the last x's depends"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.0*timescale,"on u. Try solving for x in terms of u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7d.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")

	caption = [6.0*timescale,"For the integral of -sin(x) over cos(x), we can replace -sin(x)dx with du"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"and replace cos(x) with u. At this point the integral is entirely in terms of u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7e.mp3'\noutpoint 00:"+tstamp(12.0*timescale)+"00\n\n")

	caption = [6.5*timescale,"For the integral of sin(5x) we replace dx with du over 5. Then replace sin(5x) with sin(u)."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"The integral is in terms of u and all that is left is integration with respect to u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/7f.mp3'\noutpoint 00:"+tstamp(12.5*timescale)+"00\n\n")


	for framen in range(0,11):
		color = 'black'
		text = ''
		durations = [3.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'Examples'
		item1 = r'\setlength\itemsep{1em}\item $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx$'
		item2 = r'\begin{itemize} \item[] $u=\cos(x)$ \item[] $du=-\sin(x)dx$ \end{itemize}'
		item1a = r'\setlength\itemsep{1em}\item  $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx=\displaystyle\int \frac{du}{u}$'
		item1b = r'\setlength\itemsep{1em}\item  $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx=\displaystyle\int \frac{du}{u}=\ln|u|+\text{C}$'
		item1c = r'\setlength\itemsep{1em}\item  $\displaystyle\int \frac{-\sin(x)}{\cos(x)}dx=\displaystyle\int \frac{du}{u}=\ln|u|+\text{C}=\ln|\cos(x)|+\text{C}$'

		item3 = r'\item Why is $\displaystyle\int \tan(x)dx=\ln|\sec(x)|+\text{C}$?'

		item4 = r'\setlength\itemsep{1em}\item $\displaystyle\int xe^{x^2-1}dx$'
		item5 = r'\begin{itemize} \item[] $u=x^2-1$ \item[] $du=2xdx$ \end{itemize}'
		item4a = r'\setlength\itemsep{1em}\item  $\displaystyle\int xe^{x^2-1}dx=\displaystyle\int \frac{1}{2}e^udu$'
		item4b = r'\setlength\itemsep{1em}\item  $\displaystyle\int xe^{x^2-1}dx=\displaystyle\int \frac{1}{2}e^udu=\frac{1}{2}e^u+\text{C}$'
		item4c = r'\setlength\itemsep{1em}\item  $\displaystyle\int xe^{x^2-1}dx=\displaystyle\int \frac{1}{2}e^udu=\frac{1}{2}e^u+\text{C}=\frac{1}{2}e^{x^2-1}+\text{C}$'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1a+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1b+item2+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+item4+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+item4+item5+r'\end{itemize}'
		tstr9 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+item4a+item5+r'\end{itemize}'
		tstr10 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+item4b+item5+r'\end{itemize}'
		tstr11 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1c+item2+item3+item4c+item5+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8,tstr9,tstr10,tstr11]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,framen,tframes)

		ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes += 1

	caption = [4.5*timescale,"To finish this example we need to compute the integral of du over u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8a.mp3'\noutpoint 00:"+tstamp(4.5*timescale)+"00\n\n")

	caption = [5.0*timescale,"The integral is the natural logarithm of the absolute value of u. Plus C."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8b.mp3'\noutpoint 00:"+tstamp(5.0*timescale)+"00\n\n")

	caption = [4.0*timescale,"Only after integration do we reintroduce x. Don't forget this step."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [4.5*timescale,"We just need to look up what u was in terms of x and make the substitution."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8c.mp3'\noutpoint 00:"+tstamp(8.5*timescale)+"00\n\n")

	caption = [7.0*timescale,"So the integral of -sin(x) over cos(x) is the log of the absolute value of cosine of x plus C."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8d.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")

	caption = [6.0*timescale,"As a followup, compute the integral of tan(x) using u-substitution. It seems like a very similar"]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"question, but the answer involves sec(x)? Think about the domain and properties of logarithms "]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [6.0*timescale,"to understand why the integral of tan(x) is the natural log of the absolute value of sec(x) plus C."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8e.mp3'\noutpoint 00:"+tstamp(18.0*timescale)+"00\n\n")

	caption = [6.5*timescale,"To compute the integral of xe^(x^2-1) we need to compute the integral of one-half e^u."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8f.mp3'\noutpoint 00:"+tstamp(6.5*timescale)+"00\n\n")

	caption = [5.5*timescale,"Integrating an exponential is simple as this integral is just one-half e^u. Plus C."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8g.mp3'\noutpoint 00:"+tstamp(5.5*timescale)+"00\n\n")

	caption = [7.0*timescale,"Then replace u with x^2-1 to yield the answer of one-half e^(x^2-1) plus C."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'usubaudio/8h.mp3'\noutpoint 00:"+tstamp(7.0*timescale)+"00\n\n")


	

		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 usub.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
