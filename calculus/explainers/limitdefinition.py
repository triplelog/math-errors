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
			if page == 'graph':
				if len(estr[framen])>0:
					thestr += makegraph(estr[framen])
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


	for framen in range(0,5):
		color = 'black'
		text = ''
		durations = [1.0,5.0,1.0,1.0,1.0]
		twopages = [1.0,1.0]
		pages = [['text'],['graph']]
		headtxt = r'Limit Definition of Derivative'
		item1 = r'\item $\displaystyle\frac{d}{dx}[f(x)]=\displaystyle\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}$'

		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge\begin{itemize} '+item1+r'\end{itemize}'
		tstr = [tstr1,tstr2,tstr2,tstr2,tstr2]


		yscale = 1.0
		xscale = 4.0
		xmin = -1
		xmax = 2
		ymin = -2
		ymax = 5
		fn = '(x-.5)**3+1'
		h = 1.5-framen*.25
		x0 = 1
		m = (((x0+h)-.5)**3+1-(((x0)-.5)**3+1))/(h)
		axisstrs = []
		axisstrs.append(r'''\draw[->] ('''+str(xmin)+r''',0) -- ('''+str(xmax)+r''',0) node[right] {};''')
		axisstrs.append(r'''\draw[->] (0,'''+str(ymin)+r''') -- (0,'''+str(ymax)+r''') node[above] {};''')

		pointstrs = []
		pointstrs.append(r'''\draw[-] ('''+str(x0)+r''','''+str(.15/yscale)+r''') -- ('''+str(x0)+r''','''+str(-.15/yscale)+r''') node[below] {$'''+str('x')+r'''$};''')
		pointstrs.append(r'''\draw[-] ('''+str(x0+h)+r''','''+str(.15/yscale)+r''') -- ('''+str(x0+h)+r''','''+str(-.15/yscale)+r''') node[below] {$'''+str('x+h')+r'''$};''')
		pointstrs.append(r'''\draw[-] ('''+str(.15/xscale)+r''','''+str(((x0)-.5)**3+1)+r''') -- ('''+str(-.15/xscale)+r''','''+str(((x0)-.5)**3+1)+r''') node[left] {$'''+str('f(x)')+r'''$};''')
		pointstrs.append(r'''\draw[-] ('''+str(.15/xscale)+r''','''+str(((x0+h)-.5)**3+1)+r''') -- ('''+str(-.15/xscale)+r''','''+str(((x0+h)-.5)**3+1)+r''') node[left] {$'''+str('f(x+h)')+r'''$};''')

		plotstrs = []
		plotstrs.append(r'''\draw[domain='''+str(xmin)+r''':'''+str(xmax)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)').replace('**','^'))+r'''});''')
		plotstrs.append(r'''\draw[domain='''+str(xmin)+r''':'''+str(xmax)+r''',smooth,variable=\x,red] plot ({\x},{'''+str(m)+r'''*(\x-'''+str(x0)+r''')+'''+str(((x0)-.5)**3+1)+r'''});''')
		
		
		cliprect = {'xmin':xmin,'xmax':xmax,'ymin':ymin,'ymax':ymax}
		estr = [[],[],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs],[xscale,yscale,axisstrs,pointstrs,cliprect,plotstrs]]

		makestr(twopages,startstr,pages,[tstr],estr,framen,tframes)
		

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

	caption = [3.5*timescale,'function composition within the integral so that we can integrate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Most functions with composition will require u substitution.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")


	for framen in range(0,4):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0]
		twopages = False
		pages = [['text'],[]]
		headtxt = r'The Power Rule'
		item1 = r'\setlength\itemsep{3em}\item $\displaystyle\frac{d}{dx}[x]=\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}=\lim_{h\rightarrow 0}\frac{x+h-x}{h}=\lim_{h\rightarrow 0}\frac{h}{h}=\lim_{h\rightarrow 0}1=1$'
		item2 = r'''\item $\displaystyle\frac{d}{dx}[x^2]=\lim_{h\rightarrow 0}\frac{(x+h)^2-x^2}{h}=\lim_{h\rightarrow 0}\frac{x^2+2xh+h^2-x^2}{h}=\lim_{h\rightarrow 0}\frac{2xh+h^2}{h}=\lim_{h\rightarrow 0}2x+h=2x$'''
		item3 = r'''\item $\displaystyle\frac{d}{dx}[\sqrt{x}]=\lim_{h\rightarrow 0}\frac{\sqrt{x+h}-\sqrt{x}}{h}=\lim_{h\rightarrow 0}\frac{\sqrt{x+h}-\sqrt{x}}{h}\cdot\frac{\sqrt{x+h}+\sqrt{x}}{\sqrt{x+h}+\sqrt{x}}=\lim_{h\rightarrow 0}\frac{x+h-x}{h(\sqrt{x+h}+\sqrt{x})}=\lim_{h\rightarrow 0}\frac{1}{\sqrt{x+h}+\sqrt{x}}=\frac{1}{2\sqrt{x}}$'''
		
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+item2+r'\end{itemize}'
		tstr4 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+item2+item3+r'\end{itemize}'

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

	caption = [3.5*timescale,'function composition within the integral so that we can integrate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Most functions with composition will require u substitution.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")


	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0]
		twopages = False
		pages = [['text'],[]]
		headtxt = r'Sums and Constant Multiples'
		item1 = r'\setlength\itemsep{5em}\item $\displaystyle\frac{d}{dx}[f(x)+g(x)]=\lim_{h\rightarrow 0}\frac{f(x+h)+g(x+h)-f(x)-g(x)}{h}=\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}+\frac{g(x+h)-g(x)}{h}=\frac{d}{dx}[f(x)]+\frac{d}{dx}[g(x)]$'
		item2 = r'''\item $\displaystyle\frac{d}{dx}[cf(x)]=\lim_{h\rightarrow 0}\frac{cf(x+h)-cf(x)}{h}=c\cdot\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}=c\cdot\frac{d}{dx}[f(x)]$'''
		
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+item2+r'\end{itemize}'

		tstr = [tstr1,tstr2,tstr3]
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

	caption = [3.5*timescale,'function composition within the integral so that we can integrate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Most functions with composition will require u substitution.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")

	for framen in range(0,3):
		color = 'black'
		text = ''
		durations = [1.0,5.0,5.5,5.0]
		twopages = False
		pages = [['text'],[]]
		headtxt = r'Product Rule'
		item1 = r'\setlength\itemsep{5em}\item $\displaystyle\frac{d}{dx}[f(x)+g(x)]=\lim_{h\rightarrow 0}\frac{f(x+h)+g(x+h)-f(x)-g(x)}{h}=\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}+\frac{g(x+h)-g(x)}{h}=\frac{d}{dx}[f(x)]+\frac{d}{dx}[g(x)]$'
		item2 = r'''\item $\displaystyle\frac{d}{dx}[cf(x)]=\lim_{h\rightarrow 0}\frac{cf(x+h)-cf(x)}{h}=c\cdot\lim_{h\rightarrow 0}\frac{f(x+h)-f(x)}{h}=c\cdot\frac{d}{dx}[f(x)]$'''
		
		tstr1 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Huge'
		tstr2 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+r'\end{itemize}'
		tstr3 = r'\Huge\begin{center}'+headtxt+r'\end{center}\Large\begin{itemize} '+item1+item2+r'\end{itemize}'

		tstr = [tstr1,tstr2,tstr3]
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

	caption = [3.5*timescale,'function composition within the integral so that we can integrate.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	caption = [3.5*timescale,'Most functions with composition will require u substitution.']
	ffs.write('00:'+tstamp(fullduration)+'00 --> 00:'+tstamp(fullduration+caption[0])+'00\n')
	ffs.write(caption[1]+"\n\n")
	fullduration += caption[0]

	ffa.write("file 'chainaudio/1a.mp3'\noutpoint 00:"+tstamp(10.5*timescale)+"00\n\n")



	



	

		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i inputs.ffconcat -f concat -i inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 8 limitdefinition.mp4 -y')
	#os.system('rm inputsAudio.ffconcat')
	#os.system('rm inputs.ffconcat')
	
	#jsoncolors = []

	#for i in colors:
	#	jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	#return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

run_it()
