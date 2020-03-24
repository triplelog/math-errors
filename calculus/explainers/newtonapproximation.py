import sympy
from sympy import *
from sympy.abc import x
import os
import time
from subprocess import Popen
import sys
import math

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

	graphstr += r'''\clip ('''+str(cliprect['xmin'])+r''','''+str(cliprect['ymin'])+r''') rectangle ('''+str(cliprect['xmax'])+r''','''+str(cliprect['ymax'])+r''');'''+'\n'
	for axisstr in axisstrs:
		graphstr += axisstr+'\n'

	for pointstr in pointstrs:
		graphstr += pointstr+'\n'
	
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


	
	colors = []
	tduration = 0
	tframes = 0
	fullduration = 0
	timescale = 1.0


	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [3.0,3.0,3.0,3.0]
		twopages = False
		pages = [['text'],[]]

		headtxt = r'Newton Approximation'
		item1 = r'\setlength\itemsep{3em}\item Find approximate solutions to $f(x)=0$.'
		item2 = r"\item Approximate square roots."
		item3 = r'\item Approximate logarithms.'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4]
		estr = []
		
		makestr(twopages,startstr,pages,tstr,estr,[],framen,tframes)

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

	ffa.write("file 'chainaudio/3.mp3'\noutpoint 00:"+tstamp(10.0*timescale)+"00\n\n")

	caption = [3.0*timescale,'Once we have u and dv we need to find du and v.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'If you cannot get u and dv then you need to return to step 1']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.0*timescale,"and select a different u and dv. It's okay to try multiple pairs until one works."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3b.mp3'\noutpoint 00:"+tstamp(10.0*timescale)+"00\n\n")

	caption = [3.5*timescale,"Then compute the new integral and apply integration by parts."]
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")


	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [5.0,5.0,5.5,5.0,5.0,5.0]
		twopages = [.625,.35]
		pages = [['text'],['graph']]


		item1 = r'\setlength\itemsep{2.5em}\item Make an initial approximation.'
		item2 = r"\item Compute the tangent line at that point."
		item3 = r'\item Use tangent line to make a better approximation.'
		item4 = r'\item Repeat until approximation is good enough.'

		tstr1 = r'\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr4 = r'\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr4,tstr4]

		  
		
		yscale = 3.0
		xscale = 3.0
		xmin = -1.0
		xmax = 2.0
		ymin = -1.5
		ymax = 1.5
		x0 = -.5
		m = math.log(2.5)*2.5**x0
		yl = m*(xmin-x0)+2.5**x0-1.5
		yr = m*(xmax-x0)+2.5**x0-1.5
		x1 = -1*(2.5**x0-1.5)/m+x0

		m1 = math.log(2.5)*2.5**x1
		yl1 = m1*(xmin-x1)+2.5**x1-1.5
		yr1 = m1*(xmax-x1)+2.5**x1-1.5
		x2 = -1*(2.5**x1-1.5)/m1+x1

		m2 = math.log(2.5)*2.5**x2
		yl2 = m2*(xmin-x2)+2.5**x2-1.5
		yr2 = m2*(xmax-x2)+2.5**x2-1.5
		x3 = -1*(2.5**x2-1.5)/m2+x2

		axisstrs = []
		axisstrs.append(r'''\draw[->] ('''+str(xmin)+r''',0) -- ('''+str(xmax)+r''',0) node[right] {$x$};''')
		axisstrs.append(r'''\draw[->] (0,'''+str(ymin)+r''') -- (0,'''+str(ymax)+r''') node[above] {$y$};''')

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')

		plotstrs = []
		plotstrs.append(r'''\draw[domain=-1.5:1.5,variable=\x,blue] plot ({\x},{2.5^\x-1.5});''')
		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr = [[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs]]


		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl)+''') -- ('''+str(xmax)+','+str(yr)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])



		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl)+''') -- ('''+str(xmax)+','+str(yr)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl1)+''') -- ('''+str(xmax)+','+str(yr1)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x2)+''',.05) -- ('''+str(x2)+''',-.05) node[below] {$x_2$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl1)+''') -- ('''+str(xmax)+','+str(yr1)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x2)+''',.05) -- ('''+str(x2)+''',-.05) node[below] {$x_2$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x3)+''',-.05) -- ('''+str(x3)+''',.05) node[above] {$x_3$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl2)+''') -- ('''+str(xmax)+','+str(yr2)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		startstr2 = startstr + r'''\Huge\begin{center}
			How to compute a Newton approximation
		\end{center}'''

		makestr(twopages,startstr2,pages,[tstr,[]],[],gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Degrees are a perfectly acceptable unit for trigonometry. 360 might be an'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	for framen in range(0,10):
		color = 'black'
		text = ''
		durations = [5.0,5.0,5.5,5.0,5.0,5.0,5.0,5.0,5.0,5.0]
		twopages = [.5,.475]
		pages = [['text'],['text']]


		item1 = r"\setlength\itemsep{2em}\item $f'(x_0)=\frac{y_1-y_0}{x_1-x_0}$"
		item2 = r"\item $f'(x_0)=\frac{0-f(x_0)}{x_1-x_0}$"
		item3 = r"\item $x_1=x_0-\frac{f(x_0)}{f'(x_0)}$"
		item4 = r'''\item \noindent\fbox{%
				\parbox{.5\textwidth}{%
			        $x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}$
			    }%
			}'''

		tstr1 = r'\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr4 = r'\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr4,tstr4,tstr4,tstr4,tstr4,tstr4]

		item1 = r"\setlength\itemsep{.5em}\item $f(x)=x^2-2$"
		item2a = r"\item $f'(x)=2x$ "
		item2b = r'''\item \noindent\fbox{%
				\parbox{.5\textwidth}{%
			        $x_{n+1}=x_n-\frac{x_n^2-2}{2x_n}$
			    }%
			}'''

		item3 = r"\item $f(x)=e^x-2$"
		item4a = r"\item $f'(x)=e^x$ "
		item4b = r'''\item \noindent\fbox{%
				\parbox{.5\textwidth}{%
			        $x_{n+1}=x_n-\frac{e^{x_n}-2}{e^{x_n}}$
			    }%
			}'''

		#item2c = r"\begin{itemize} \item[] $f'(x)=2x$ \item[] $x_{n+1}=x_n-\frac{x_n^2-2}{2x_n}$ \item[$1.$] $x_1 = 1.5-\frac{1.5^2-2}{3}=1.4166666$\end{itemize}"

		tstr1 = r'\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{itemize} '+item1+item2a+r'\end{itemize}'
		tstr3 = r'\Huge\begin{itemize} '+item1+item2a+item2b+r'\end{itemize}'
		tstr4 = r'\Huge\begin{itemize} '+item1+item2a+item2b+r'\item[] '+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{itemize} '+item1+item2a+item2b+r'\item[] '+item3+item4a+r'\end{itemize}'
		tstr6 = r'\Huge\begin{itemize} '+item1+item2a+item2b+r'\item[] '+item3+item4a+item4b+r'\end{itemize}'
		#tstr4 = r'''\Huge\noindent\fbox{%
		#		\parbox{.5\textwidth}{%
		#		\begin{itemize} '''+item1+item2a+item2b+r'''\end{itemize}
		#		}%
		#	}'''
		#tstr4 = r'\Huge\begin{itemize} '+item1+item2c+r'\end{itemize}'
		tstrp2 = ['','','','',tstr1,tstr2,tstr3,tstr4,tstr5,tstr6]


		estr = []
		
		

		startstr2 = startstr + r'''\Huge\begin{center}
			What's the formula?
		\end{center}'''

		makestr(twopages,startstr2,pages,[tstrp1,tstrp2],estr,[],framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Degrees are a perfectly acceptable unit for trigonometry. 360 might be an'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")

	for framen in range(0,16):
		color = 'black'
		text = ''
		durations = [5.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0]
		twopages = [.5,.475]
		pages = [['text'],['text']]


		headtxt = r'What is $\sqrt{5}$?'
		item1 = r'\setlength\itemsep{3em}\item Let $f(x)=x^2-5$.'
		item2 = r"\item $f'(x)=2x$"
		item3 = r'\item $x_{n+1}=x_n-\frac{x_n^2-5}{2x_n}$'
		item4 = r'\item $x_0=2$'
		item5 = r'\item $x_1=2-\frac{2^2-5}{2\cdot 2}=2.25$'
		item6 = r'\item $x_2=2.25-\frac{2.25^2-5}{2\cdot 2.25}=2.23611111$'
		item7 = r'\item $x_3=2.23611111-\frac{2.23611111^2-5}{2\cdot 2.23611111}=2.23606798$'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+item7+r'\end{itemize}'

		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8]

		headtxt = r'What is $\ln{5}$?'
		item1 = r'\setlength\itemsep{3em}\item Let $f(x)=e^x-5$.'
		item2 = r"\item $f'(x)=e^x$"
		item3 = r'\item $x_{n+1}=x_n-\frac{e^{x_n}-5}{e^{x_n}}$'
		item4 = r'\item $x_0=1.5$'
		item5 = r'\item $x_1=1.5-\frac{e^{1.5}-5}{e^{1.5}}=1.61565$'
		item6 = r'\item $x_2=1.61565-\frac{e^{1.61565}-5}{e^{1.61565}}=1.61045717$'
		item7 = r'\item $x_3=1.61045717-\frac{e^{1.61045717}-5}{e^{1.61045717}}=1.60943843$'
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr5 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr6 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+r'\end{itemize}'
		tstr7 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+r'\end{itemize}'
		tstr8 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+item2+item3+item4+item5+item6+item7+r'\end{itemize}'

		tstrp1 = [tstr1,tstr2,tstr3,tstr4,tstr5,tstr6,tstr7,tstr8]


		estr = []
		
		

		startstr2 = startstr

		makestr(twopages,startstr2,pages,[tstrp1,tstrp2],estr,[],framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Degrees are a perfectly acceptable unit for trigonometry. 360 might be an'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")


	for framen in range(0,6):
		color = 'black'
		text = ''
		durations = [5.0,5.0,5.5,5.0,5.0,5.0]
		twopages = [.625,.35]
		pages = [['text'],['graph']]


		item1 = r'\setlength\itemsep{2.5em}\item Convergence may never happen.'
		item2 = r"\item Convergence may lead to a different solution."
		item3 = r'\item Use tangent line to make a better approximation.'
		item4 = r'\item Repeat until approximation is good enough.'

		tstr1 = r'\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr2 = r'\Huge\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr3 = r'\Huge\begin{itemize} '+item1+item2+item3+r'\end{itemize}'
		tstr4 = r'\Huge\begin{itemize} '+item1+item2+item3+item4+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr3,tstr4,tstr4,tstr4]

		  
		
		yscale = 3.0
		xscale = 3.0
		xmin = -1.0
		xmax = 2.0
		ymin = -1.5
		ymax = 1.5
		x0 = -.5
		m = math.log(2.5)*2.5**x0
		yl = m*(xmin-x0)+2.5**x0-1.5
		yr = m*(xmax-x0)+2.5**x0-1.5
		x1 = -1*(2.5**x0-1.5)/m+x0

		m1 = math.log(2.5)*2.5**x1
		yl1 = m1*(xmin-x1)+2.5**x1-1.5
		yr1 = m1*(xmax-x1)+2.5**x1-1.5
		x2 = -1*(2.5**x1-1.5)/m1+x1

		m2 = math.log(2.5)*2.5**x2
		yl2 = m2*(xmin-x2)+2.5**x2-1.5
		yr2 = m2*(xmax-x2)+2.5**x2-1.5
		x3 = -1*(2.5**x2-1.5)/m2+x2

		axisstrs = []
		axisstrs.append(r'''\draw[->] ('''+str(xmin)+r''',0) -- ('''+str(xmax)+r''',0) node[right] {$x$};''')
		axisstrs.append(r'''\draw[->] (0,'''+str(ymin)+r''') -- (0,'''+str(ymax)+r''') node[above] {$y$};''')

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')

		plotstrs = []
		plotstrs.append(r'''\draw[domain=-1.5:1.5,variable=\x,blue] plot ({\x},{2.5^\x-1.5});''')
		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr = [[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs]]


		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl)+''') -- ('''+str(xmax)+','+str(yr)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])



		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl)+''') -- ('''+str(xmax)+','+str(yr)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl1)+''') -- ('''+str(xmax)+','+str(yr1)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x2)+''',.05) -- ('''+str(x2)+''',-.05) node[below] {$x_2$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl1)+''') -- ('''+str(xmax)+','+str(yr1)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+''',.05) -- ('''+str(x0)+''',-.05) node[below] {$x_0$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x1)+''',.05) -- ('''+str(x1)+''',-.05) node[below] {$x_1$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x2)+''',.05) -- ('''+str(x2)+''',-.05) node[below] {$x_2$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x3)+''',-.05) -- ('''+str(x3)+''',.05) node[above] {$x_3$};''')
		pointstrs.append(r'''\draw[-,red] ('''+str(xmin)+','+str(yl2)+''') -- ('''+str(xmax)+','+str(yr2)+''');''')


		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		gstr.append([xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs])

		startstr2 = startstr + r'''\Huge\begin{center}
			What's the deal with convergence?
		\end{center}'''

		makestr(twopages,startstr2,pages,[tstr,[]],[],gstr,framen,tframes)
		

		if tframes > 0:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.0001)+"\n")
		else:
			ff.write("file 'explainerframe"+str(tframes)+".png'\nduration "+str(durations[framen]*timescale+.05)+"\n")
		os.system('./outputLatex.sh -c "explainerframe'+str(tframes)+'"')
		tframes+=1
	
	caption = [3.5*timescale,'Degrees are a perfectly acceptable unit for trigonometry. 360 might be an'] 
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/3c.mp3'\noutpoint 00:"+tstamp(3.0*timescale)+"00\n\n")
	

		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 newtonapproximation.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
