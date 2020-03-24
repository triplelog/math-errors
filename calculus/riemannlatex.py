import sympy
from sympy import *
from sympy.abc import x
import os
import time
from subprocess import Popen
import sys
from clean import cleanpar

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
def myslatex(input_string):
	input_string = sympy.latex(input_string.replace('abs(x)','holdforit')).replace('holdfordydx','\\frac{dy}{dx}').replace('log{','ln{').replace('log^','ln^').replace('holdforit','|x|')
	return input_string
def slatex(f,dvar):
	try:
		return myslatex(sympy.sympify(f,evaluate=True))
	except:
		return myslatex(sympy.sympify(f))

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
					


def makegraph(a,b,n,fn,framen,rtype,alatex,blatex):

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
	  \draw[-] ('''+str(a)+r''','''+str((ymax-ymin)*.03)+r''') -- ('''+str(a)+r''','''+str((ymax-ymin)*-.03)+r''') node[below] {$'''+alatex+r'''$};
	  \draw[-] ('''+str(b)+r''','''+str((ymax-ymin)*.03)+r''') -- ('''+str(b)+r''','''+str((ymax-ymin)*-.03)+r''') node[below] {$'''+blatex+r'''$};
  	  \clip ('''+str(a-1)+r''','''+str(ymin-(ymax-ymin)*.1)+r''') rectangle ('''+str(b+1)+r''','''+str(ymax+(ymax-ymin)*.1)+r''');
	  \draw[domain='''+str(a-1)+r''':'''+str(b+1)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)').replace('**','^'))+r'''});
	  '''+rectstr+r'''
	\end{tikzpicture}
	\end{minipage}\hfill'''
	return graphstr, duration, audioStr

def makeequation(a,b,n,fn,framen,rtype,alatex,blatex):


	duration = 3.0
	audioStr = ''
	allValues = []
	allX = []
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
	w = (float(b)-float(a))/float(n)
	if framen ==0:
		line1str = r''
	elif framen ==1:
		line1str = '\n'+r'\displaystyle\int f(x) dx & \approx\\'
		duration = 3.0
	elif framen ==2:
		line1str = '\n'+r'\displaystyle\int_{'+alatex+r'}^{'+blatex+r'} '+sympy.latex(fn)+r' dx & \approx\\'
		duration = 3.0
	else:
		if n > 4:
			line1str = '\n'+r'\displaystyle\int_{'+alatex+r'}^{'+blatex+r'} '+sympy.latex(fn)+r' dx & \approx A(r_1)+A(r_2)+\dots+A(r_{'+str(n)+r'})\\'
		elif n > 3:
			line1str = '\n'+r'\displaystyle\int_{'+alatex+r'}^{'+blatex+r'} '+sympy.latex(fn)+r' dx & \approx A(r_1)+A(r_2)+A(r_3)+A(r_4)\\'
		elif n > 2:
			line1str = '\n'+r'\displaystyle\int_{'+alatex+r'}^{'+blatex+r'} '+sympy.latex(fn)+r' dx & \approx A(r_1)+A(r_2)+A(r_3)\\'
		else:
			line1str = '\n'+r'\displaystyle\int_{'+alatex+r'}^{'+blatex+r'} '+sympy.latex(fn)+r' dx & \approx A(r_1)+A(r_2)\\'
			
	if framen < 4:
		line2str = r''
	else:
		if n > 4:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+\dots+w\cdot h(r_{'+str(n)+r'})\\'
		elif n > 3:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+w\cdot h(r_3)+w\cdot h(r_4)\\'
		elif n > 2:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)+w\cdot h(r_3)\\'
		else:
			line2str = '\n'+r'& \approx w\cdot h(r_1)+w\cdot h(r_2)\\'
	if framen < 5:
		line3str = r''
	else:
		if n > 4:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+\dots+h(r_{'+str(n)+r'}))\\'
		elif n > 3:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+h(r_3)+h(r_4))\\'
		elif n > 2:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2)+h(r_3))\\'
		else:
			line3str = '\n'+r'& \approx w\cdot (h(r_1)+h(r_2))\\'
	if framen < 6:
		line4str = r''
	elif framen <7:
		if n > 4:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+\dots+h(r_{'+str(n)+r'}))\\'
		elif n > 3:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+h(r_3)+h(r_4))\\'
		elif n > 2:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2)+h(r_3))\\'
		else:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(h(r_1)+h(r_2))\\'
	else:
		if n > 4:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+\dots+f(x_{'+str(n)+r'}))\\'
		elif n > 3:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+f(x_3)+f(x_4))\\'
		elif n > 2:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2)+f(x_3))\\'
		else:
			line4str = '\n'+r'& \approx '+cleandecimal(w,3)+r'(f(x_1)+f(x_2))\\'
	if n == 2:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r')\\'
		if framen < 10:
			line6str = r''
		elif framen < 11:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1],4)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]),4)+r'\\'
	elif n == 3:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+f(x_3))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+f(x_3))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+r')\\'
		if framen < 11:
			line6str = r''
		elif framen < 12:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1]+allValues[2],4)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]+allValues[2]),4)+r'\\'
	elif n == 4:
		if framen < 8:
			line5str = r''
		elif framen < 9:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+f(x_3)+f(x_4))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+f(x_3)+f(x_4))\\'
		elif framen < 11:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+r'+f(x_4))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+'+cleandecimal(allValues[2],2)+'+'+cleandecimal(allValues[3],2)+r')\\'
		if framen < 12:
			line6str = r''
		elif framen < 13:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0]+allValues[1]+allValues[2]+allValues[3],4)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*(allValues[0]+allValues[1]+allValues[2]+allValues[3]),4)+r'\\'
	elif n > 4:
		if framen < 8:
			line5str = r''
		elif framen < 9:

			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+f(x_2)+\dots+f(x_{'+str(n)+r'}))\\'
		elif framen < 10:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+\dots+f(x_{'+str(n)+r'}))\\'
		else:
			line5str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(allValues[0],2)+r'+'+cleandecimal(allValues[1],2)+r'+\dots+'+cleandecimal(allValues[-1],2)+r')\\'
		if framen < 11:
			line6str = r''
		elif framen < 12:
			line6str = '\n'+r'& \approx '+cleandecimal(w,3)+r'('+cleandecimal(sum(allValues),4)+r')\\'
		else:
			line6str = '\n'+r'& \approx '+cleandecimal(w*sum(allValues),4)+r'\\'
	equationstr = r'''\begin{minipage}{.5\linewidth}
	\scalebox{1.45}{\parbox{.5\linewidth}{%
	\large
	\begin{align*}'''+line1str+line2str+line3str+line4str+line5str+line6str+r'''
	\end{align*}
	}}
	\end{minipage}'''
	return equationstr.replace('+-','-'), duration, audioStr

def maketext(a,b,n,fn,framen,rtype,alatex,blatex):

	duration = 5.0
	audioStr = ''
	if framen > 0:
		texta = str(a)
		duration = 3.0
	else:
		texta = '??'
	if framen > 1:
		textb = str(b)
		duration = 3.0
	else:
		textb = '??'
	if framen > 2:
		textn = str(n)
		duration = 4.0
	else:
		textn = '??'
	if framen > 3:
		duration = 4.0
		textw = str(cleandecimal((float(b)-float(a))/float(n),4))
	else:
		textw = '??'
	textstr = r'''\begin{minipage}{.475\linewidth}
	\huge
	\vspace{5pt}
	\noindent
	Approximate the definite integral of the function $f(x)='''+sympy.latex(fn)+r'''$ on the interval $['''+alatex+r''','''+blatex+r''']$ with $'''+str(n)+r'''$ rectangles of equal width using the '''+str(rtype)+r''' method.
	\begin{center}
	\begin{tabular}{ |c|c|c|c| } 
		\hline
		$a='''+texta+r'''$ & $b='''+textb+r'''$ & $n='''+textn+r'''$ & $w=\frac{b-a}{n}='''+textw+r'''$\\ 
		\hline
		\end{tabular}
	\end{center}
	\end{minipage}\hfill'''
	return textstr, duration, audioStr

def maketable(a,b,n,fn,framen,rtype,alatex,blatex):

	
	
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
	

def run_it(my_function,hashprefix,a,b,n,rtype,alatex,blatex):
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows}


	\begin{document}
	\LARGE'''

	fn = sympy.sympify(cleanpar(my_function,'x'))

	if n == 2:
		tframes = 2
	elif n == 3:
		tframes = 3
	elif n == 4:
		tframes = 4
	elif n > 4:
		tframes = 4
	maxframes = 5+n+1+3*tframes+10
	if n > 4:
		maxframes -= 1
	ff = open('images/new/'+hashprefix+'inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')
	ffs = open('images/new/'+hashprefix+'subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')

	ffa = open('landing/static/audio/'+hashprefix+'inputsAudio.ffconcat','w')
	ffa.write('ffconcat version 1.0\n\n')
	
	colors = []
	tduration = 0
	for framen in range(0,maxframes):
		thestr = startstr
		color = 'black'
		text = ''
		duration = .5
		if framen < 5:
			rettex = makegraph(a,b,n,fn,0,rtype,alatex,blatex)
			thestr += '\n'+ rettex[0]
		elif framen == 5+n:
			rettex = makegraph(a,b,n,fn,framen-4,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			color = 'green'
			text = 'Visualize the rectangles'
			colors.append([tduration,color,text])
			tduration = 0
		elif framen == 5+n+1:
			rettex = makegraph(a,b,n,fn,framen-4,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
		elif framen < 5+n+2:
			rettex = makegraph(a,b,n,fn,framen-4,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			if framen == 5:
				ffs.write(str(framen+1)+'a\n')
				ffs.write('00:00:19.000 --> 00:00:23.000\n')
				ffs.write("We know the width of each rectangle and need to compute the height.\n\n")
				ffa.write("file 'riemann/part2/a.mp3'\noutpoint 00:00:04.000\n\n")
				ffs.write(str(framen+1)+'b\n')
				ffs.write('00:00:23.000 --> 00:00:29.000\n')
				if rtype=='MRAM':
					ffs.write("We are using midpoints so the height will be the value of f(x) in the middle.\n\n")
					ffa.write("file 'riemann/part2/bm.mp3'\noutpoint 00:00:06.000\n\n")
				elif rtype=='LRAM':
					ffs.write("We are using left endpoints so the height will be the value of f(x) on the left.\n\n")
					ffa.write("file 'riemann/part2/bl.mp3'\noutpoint 00:00:06.000\n\n")
				elif rtype=='RRAM':
					ffs.write("We are using right endpoints so the height will be the value of f(x) on the right.\n\n")
					ffa.write("file 'riemann/part2/br.mp3'\noutpoint 00:00:06.000\n\n")
			elif framen == 6:
				ffs.write(str(framen+1)+'a\n')
				ffs.write('00:00:29.000 --> 00:00:30.500\n')
				ffs.write("For the first rectangle,\n\n")
				ffa.write("file 'riemann/part2/c.mp3'\noutpoint 00:00:01.500\n\n")
				ffs.write(str(framen+1)+'b\n')
				ffs.write('00:00:30.500 --> 00:00:34.500\n')
				if rtype=='MRAM':
					ffs.write("we match the height of the rectangle to the height of the function in the center.\n\n")
					ffa.write("file 'riemann/part2/dm.mp3'\noutpoint 00:00:04.000\n\n")
				elif rtype=='LRAM':
					ffs.write("we match the height of the rectangle to the height of the function on the left.\n\n")
					ffa.write("file 'riemann/part2/dl.mp3'\noutpoint 00:00:04.000\n\n")
				elif rtype=='RRAM':
					ffs.write("we match the height of the rectangle to the height of the function on the right.\n\n")
					ffa.write("file 'riemann/part2/dr.mp3'\noutpoint 00:00:04.000\n\n")
			elif framen == 7:
				ffs.write(str(framen+1)+'a\n')
				endtime = 37.0+.5*(n-1)
				ffs.write('00:00:34.500 --> 00:00:'+str(endtime)+'00\n')
				ffs.write("And then repeat for each rectangle.\n\n")
				ffa.write("file 'riemann/part2/e.mp3'\noutpoint 00:"+tstamp(endtime-34.5)+"00\n\n")

				ffs.write(str(framen+1)+'b\n')
				endtime = 37.0+.5*(n-1)
				ffs.write('00:00:'+str(endtime)+'00 --> 00:00:'+str(endtime+4.0)+'00\n')
				ffs.write("We see the areas we want to compute so what's left is computing the heights.\n\n")
				ffa.write("file 'riemann/part2/f.mp3'\noutpoint 00:00:04.000\n\n")
		else:
			rettex = makegraph(a,b,n,fn,5+n+1-4,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
		

		if framen < 5+n+2+2*tframes:
			rettex = makeequation(a,b,n,fn,0,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
		elif framen == maxframes -1:
			rettex = makeequation(a,b,n,fn,framen-(5+n+1+2*tframes),rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			color = 'yellow'
			text = 'Compute the sum of the areas to approximate the integral'
			colors.append([tduration,color,text])
		else:
			rettex = makeequation(a,b,n,fn,framen-(5+n+1+2*tframes),rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			if framen == 5+n+2+2*tframes:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+40.0
				endtime = 37.0+.5*(n-1)+44.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Now we have everything we need to approximate the definite integral.\n\n")
				ffa.write("file 'riemann/part4/a.mp3'\noutpoint 00:00:04.000\n\n")
			elif framen == 5+n+2+2*tframes+2:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+44.0
				endtime = 37.0+.5*(n-1)+49.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("The integral is approximately the sum of the areas.\n\n")
				ffa.write("file 'riemann/part4/b.mp3'\noutpoint 00:00:05.000\n\n")
			elif framen == 5+n+2+2*tframes+3:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+49.0
				endtime = 37.0+.5*(n-1)+53.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Each area is the product of the width times the height.\n\n")
				ffa.write("file 'riemann/part4/c.mp3'\noutpoint 00:00:04.000\n\n")
			elif framen == 5+n+2+2*tframes+4:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+53.0
				endtime = 37.0+.5*(n-1)+58.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("The widths are equal so factor out the width and multiply by the sum of the heights.\n\n")
				ffa.write("file 'riemann/part4/d.mp3'\noutpoint 00:00:05.000\n\n")
			elif framen == 5+n+2+2*tframes+5:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+58.0
				endtime = 37.0+.5*(n-1)+62.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Each height is one of the values of f(x) from our table.\n\n")
				ffa.write("file 'riemann/part4/e.mp3'\noutpoint 00:00:04.000\n\n")
			elif framen == 5+n+2+2*tframes+6:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+62.0
				endtime = 37.0+.5*(n-1)+70.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Plug in the values from the table.\n\n")
				ffa.write("file 'riemann/part4/f.mp3'\noutpoint 00:00:08.000\n\n")
			elif framen == 5+n+2+2*tframes+7:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+70.0
				endtime = 37.0+.5*(n-1)+74.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Add them up and multiply by the width to get the Riemann approximation.\n\n")
				ffa.write("file 'riemann/part4/g.mp3'\noutpoint 00:00:04.000\n\n")
			
		if framen > 4:
			rettex = maketext(a,b,n,fn,4,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
		elif framen == 4:
			rettex = maketext(a,b,n,fn,framen,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			color = 'red'
			text = 'Compute the width of each rectangle'
			colors.append([tduration,color,text])
			tduration = 0
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:15.000 --> 00:00:19.000\n')
			ffs.write('The width of each rectangle must be 1.\n\n')
			ffa.write("file 'riemann/part1/e1.mp3'\noutpoint 00:00:04.000\n\n")
		else:
			rettex = maketext(a,b,n,fn,framen,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			if framen == 0:
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:00:00.000 --> 00:00:05.000\n')
				ffs.write("We're going to approximate the area under the curve using a sum of rectangles.\n\n")
				ffa.write("file 'riemann/part1/a.mp3'\noutpoint 00:00:05.000\n\n")
			elif framen == 1:
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:00:05.000 --> 00:00:08.000\n')
				ffs.write('The region starts at 0.\n\n')
				ffa.write("file 'riemann/part1/b0.mp3'\noutpoint 00:00:03.000\n\n")
			elif framen == 2:
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:00:08.000 --> 00:00:11.000\n')
				ffs.write('The right edge of the region is 5.\n\n')
				ffa.write("file 'riemann/part1/c5.mp3'\noutpoint 00:00:03.000\n\n")
			elif framen == 3:
				ffs.write(str(framen+1)+'\n')
				ffs.write('00:00:11.000 --> 00:00:15.000\n')
				ffs.write("We're going to use 5 rectangles of equal width.\n\n")
				ffa.write("file 'riemann/part1/d5.mp3'\noutpoint 00:00:04.000\n\n")
			

		if framen < 5+n+2:
			rettex = maketable(a,b,n,fn,0,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
		elif framen == 5+n+2+1*tframes-1:
			rettex = maketable(a,b,n,fn,framen-5-n-1,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			color = 'blue'
			text = 'Find the x-value for each rectangle'
			colors.append([tduration,color,text])
			tduration = 0

			ffs.write(str(framen+1)+'\n')
			starttime = 37.0+.5*(n-1)+20.0
			endtime = 37.0+.5*(n-1)+24.0
			ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
			if rtype=='MRAM':
				ffs.write("The final x-value is half the width from the right edge.\n\n")
				ffa.write("file 'riemann/part3/gm.mp3'\noutpoint 00:00:04.000\n\n")
			elif rtype=='LRAM':
				ffs.write("The final x-value is the width of one rectangle from the right edge.\n\n")
				ffa.write("file 'riemann/part3/gl.mp3'\noutpoint 00:00:04.000\n\n")
			elif rtype=='RRAM':
				ffs.write("The final x-value is at the right edge.\n\n")
				ffa.write("file 'riemann/part3/gr.mp3'\noutpoint 00:00:04.000\n\n")
		elif framen == 5+n+2+2*tframes-1:
			rettex = maketable(a,b,n,fn,framen-5-n-1,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			color = 'aqua'
			text = 'Find the height of each rectangle'
			colors.append([tduration,color,text])
			tduration = 0
		elif framen < 5+n+2+2*tframes:
			rettex = maketable(a,b,n,fn,framen-5-n-1,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]
			duration = rettex[1]
			tduration += duration
			if framen == 5+n+2:
				ffs.write(str(framen+1)+'a\n')
				starttime = 37.0+.5*(n-1)+4.0
				endtime = 37.0+.5*(n-1)+7.0
				ffs.write('00:00:'+str(starttime)+'00 --> 00:00:'+str(endtime)+'00\n')
				if rtype=='MRAM':
					ffs.write("The x-values are the midpoints of each rectangle.\n\n")
					ffa.write("file 'riemann/part3/am.mp3'\noutpoint 00:00:03.000\n\n")
				elif rtype=='LRAM':
					ffs.write("The x-values are the left endpoints of each rectangle.\n\n")
					ffa.write("file 'riemann/part3/al.mp3'\noutpoint 00:00:03.000\n\n")
				elif rtype=='RRAM':
					ffs.write("The x-values are the right endpoints of each rectangle.\n\n")
					ffa.write("file 'riemann/part3/ar.mp3'\noutpoint 00:00:03.000\n\n")

				ffs.write(str(framen+1)+'b\n')
				starttime = 37.0+.5*(n-1)+7.0
				endtime = 37.0+.5*(n-1)+12.0
				ffs.write('00:00:'+str(starttime)+'00 --> 00:00:'+str(endtime)+'00\n')
				if rtype=='MRAM':
					ffs.write("The first x is half the width from the left edge.\n\n")
					ffa.write("file 'riemann/part3/bm.mp3'\noutpoint 00:00:05.000\n\n")
				elif rtype=='LRAM':
					ffs.write("The first x is at the left edge.\n\n")
					ffa.write("file 'riemann/part3/bl.mp3'\noutpoint 00:00:05.000\n\n")
				elif rtype=='RRAM':
					ffs.write("The first x is the width of one rectangle to the right of the left edge.\n\n")
					ffa.write("file 'riemann/part3/br.mp3'\noutpoint 00:00:05.000\n\n")
				
			if framen == 5+n+3:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+12.0
				endtime = 37.0+.5*(n-1)+16.0
				ffs.write('00:00:'+str(starttime)+'00 --> 00:00:'+str(endtime)+'00\n')
				ffs.write("Add x1 plus the width to get x2.\n\n")
				ffa.write("file 'riemann/part3/c.mp3'\noutpoint 00:00:04.000\n\n")
			if framen == 5+n+4:
				ffs.write(str(framen+1)+'\n')
				starttime = 37.0+.5*(n-1)+16.0
				endtime = 37.0+.5*(n-1)+20.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("To get the next x's add the width to the previous x.\n\n")
				ffa.write("file 'riemann/part3/d.mp3'\noutpoint 00:00:04.000\n\n")
			if framen == 5+n+2+1*tframes:
				ffs.write(str(framen+1)+'a\n')
				starttime = 37.0+.5*(n-1)+24.0
				endtime = 37.0+.5*(n-1)+26.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("Once we know where to compute each height,\n\n")
				ffa.write("file 'riemann/part3/e.mp3'\noutpoint 00:00:02.000\n\n")

				ffs.write(str(framen+1)+'b\n')
				starttime = 37.0+.5*(n-1)+26.0
				endtime = 37.0+.5*(n-1)+40.0
				ffs.write('00:'+tstamp(starttime)+'00 --> 00:'+tstamp(endtime)+'00\n')
				ffs.write("we simply plug the values of x into f(x) to compute the heights.\n\n")
				ffa.write("file 'riemann/part3/f.mp3'\noutpoint 00:00:14.000\n\n")
		else:
			rettex = maketable(a,b,n,fn,5+n+1+2*tframes,rtype,alatex,blatex)
			thestr += '\n'+rettex[0]


		
		f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'rie'+str(framen)+'.tex','w')
		f.write(thestr)
		f.close()
		if framen > 0:
			ff.write("file '"+hashprefix+'rie'+str(framen)+".png'\nduration "+str(duration+.001)+"\n")
		else:
			ff.write("file '"+hashprefix+'rie'+str(framen)+".png'\nduration "+str(duration+.1)+"\n")
		#worker(hashprefix,framen)
		os.system('./outputLatex.sh -c "'+hashprefix+'rie'+str(framen)+'"')


		
	ff.close()
	ffs.close()
	ffa.close()
	#os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.txt -framerate 2 -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -f concat -i landing/static/audio/'+hashprefix+'inputsAudio.ffconcat -acodec copy -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'riemann.mp4 -y')
	os.system('rm landing/static/audio/'+hashprefix+'inputsAudio.ffconcat')
	
	jsoncolors = []

	for i in colors:
		jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	return 'new/'+hashprefix+'riemann.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
		

