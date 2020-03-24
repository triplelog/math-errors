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

def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval

def trigradian(rawfn):
	rawfn = rawfn.replace('**','^')
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
					


def makegraph(fn,x0,framen,dfnx0,y0):
	xrange = 5.0
	tangentfn = str(dfnx0)+"*(x-"+str(x0)+")+"+str(y0)
	tangentfn = tangentfn.replace('+-','-')
	y0 = fn.evalf(subs={x: x0})
	ymin = fn.evalf(subs={x: x0-xrange})
	ymax = ymin
	for i in range(0,21):
		fntemp = fn.evalf(subs={x: x0-1+i*xrange*2.0/20})
		if fntemp < ymin:
			ymin = fntemp
		elif fntemp > ymax:
			ymax = fntemp
	if ymax >400:
		ymax = 400
	if ymin < -400:
		ymin = -400
	
	xaxisstr = r'''\draw[->] ('''+str(x0-xrange)+r''',0) -- ('''+str(x0+xrange)+r''',0) node[right] {$x$};'''
	yaxisstr = r'''\draw[->] (0,'''+str(ymin-(ymax-ymin)*.1)+r''') -- (0,'''+str(ymax+(ymax-ymin)*.1)+r''') node[above] {$y$};'''
	if x0 < -1*xrange or x0 > xrange:
		yaxisstr = ''
	if ymin-(ymax-ymin)*.1 >0 or ymax+(ymax-ymin)*.1 < 0:
		xaxisstr = ''
	graphstr = r'''\begin{center}
		\begin{tikzpicture}[xscale=1,yscale='''+str(5.0/(1.2*ymax-1.2*ymin))+r''']
		  '''+xaxisstr+r'''
		  '''+yaxisstr+r'''
		  \clip ('''+str(x0-xrange)+r''','''+str(ymin-(ymax-ymin)*.1)+r''') rectangle ('''+str(x0+xrange)+r''','''+str(ymax+(ymax-ymin)*.1)+r''');
		  \draw[domain='''+str(x0-xrange)+r''':'''+str(x0+xrange)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn).replace('x','(\\x)'))+r'''});
		  \draw[domain='''+str(x0-xrange)+r''':'''+str(x0+xrange)+r''',smooth,variable=\x,red] plot ({\x},{'''+trigradian(str(tangentfn).replace('x','(\\x)'))+r'''});
		  \draw[fill,black] ('''+str(x0)+r''','''+str(y0)+r''') circle (.075 and '''+str((ymax-ymin)*.018)+r''');
		\end{tikzpicture}
		\end{center}
	\end{minipage}

	\end{document}'''
	return graphstr

def maketext(fn,x0,framen,dfn,dfnx0,y0):
	
	derivativestr = r''
	if framen == 9:
		derivativestr = r'''\\\\f'(x) & = \\'''
	elif framen > 9:
		derivativestr = r'''\\\\f'(x) & = '''+sympy.latex(dfn)+r'''\\'''
		
	plugstr = r''
	if framen == 11:
		plugstr = r'''f'(x_0) & ='''+r'''\\'''
	elif framen > 11:
		plugstr = r'''f'(x_0) & ='''+sympy.latex(dfn).replace('x','('+str(x0)+')')+r'''\\'''
		
	evalstr = r''
	if framen > 12:
		evalstr = r'''f'(x_0) & =\color{red}'''+cleandecimal(dfnx0,5)+r'''\\'''
		
	yplugstr = r''
	if framen == 5:
		yplugstr = r'''f(x_0) & ='''+r'''\\'''
	elif framen > 5:
		yplugstr = r'''f(x_0) & ='''+sympy.latex(fn).replace('x','('+str(x0)+')')+r'''\\'''
		
	yevalstr = r''
	if framen > 6:
		yevalstr = r'''f(x_0) & =\color{blue}'''+cleandecimal(y0,5)+r'''\\'''

	
	textstr = r'''\begin{minipage}{.575\linewidth}
		\begin{center}
			Find the equation of the tangent line to the curve $f(x)='''+sympy.latex(fn)+r'''$ at $x_0='''+str(x0)+r'''$.
		\end{center}
		\scalebox{1.95}{\parbox{.575\linewidth}{%
			\large
			\begin{align*}'''+yplugstr+yevalstr+derivativestr+plugstr+evalstr+r'''
			\end{align*}
			}}
			\end{minipage}\hfill'''
	return textstr

def makelist(fn,x0,framen,dfn,dfnx0,y0):
	y0str = r''
	if framen > 7:
		y0str = r'''y_0 & = \color{blue}'''+cleandecimal(y0,5)+r'''\\'''
	elif framen > 2:
		y0str = r'''y_0 & = f(x_0)\\'''
	elif framen > 0:
		y0str = r'''y_0 & =\\'''		

	x0str = r''
	if framen > 1:
		x0str = r'''x_0 & = '''+str(x0)+r'''\\'''
	elif framen > 0:
		x0str = r'''x_0 & = \\'''
	
	mstr = r''
	if framen > 13:
		mstr = r'''m & = \color{red}'''+cleandecimal(dfnx0,5)+r'''\\'''
	elif framen > 3:
		mstr = r'''m & = f'(x_0)\\'''
	elif framen > 0:
		mstr = r'''m & = \\'''

	tangentstr = r''
	if framen > 14:
		tangentfn = r'\color{red} '+cleandecimal(dfnx0,5)+r'\color{black} '+"(x-"+cleandecimal(x0,5)+")+"+r'\color{blue} '+cleandecimal(y0,5)
		tangentfn = tangentfn.replace('+-','-').replace('--','+')
		tangentstr = r'''\Aboxed{y & ='''+tangentfn+r'''}\\'''

	liststr = r'''\begin{minipage}{.4\linewidth}
			\scalebox{1.9}{\parbox{.4\linewidth}{%
			\large
			\begin{align*}
		y & = m(x-x_0)+y_0\\'''+x0str+y0str+mstr+tangentstr+r'''
			\end{align*}
			}}\vspace{-2em}'''
	return liststr


def run_it(my_function,x0,hashprefix):
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\usepackage{mathtools}
	\usepackage{color}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows}


	\begin{document}
	\huge'''
	fn = sympy.sympify(cleanpar(my_function,'x'))
	
	dfn = sympy.diff(fn)
	dfnx0 = dfn.evalf(subs={x:x0})
	y0 = fn.evalf(subs={x:x0})
	ff = open('images/new/'+hashprefix+'inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')
	ffs = open('images/new/'+hashprefix+'subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')
	colors = []
	tduration = 0
	durations = [3.0,3.0,3.0,3.0,4.0,2.0,2.0,2.0,2.0,2.5,2.5,1.0,2.0,2.0,2.0,2.0]
	for framen in range(0,16):
		duration = durations[framen]
		tduration += duration
		thestr = startstr

		thestr += '\n'+maketext(fn,x0,framen,dfn,dfnx0,y0)

		thestr += '\n'+makelist(fn,x0,framen,dfn,dfnx0,y0)

		thestr += '\n'+makegraph(fn,x0,framen,dfnx0,y0)
		if framen == 4:
			colors.append([tduration,'black','What do you need to find?'])
			tduration = 0
		if framen == 8:
			colors.append([tduration,'red','Find the y-coordinate'])
			tduration = 0
		if framen == 14:
			colors.append([tduration,'blue','Find the slope'])
			tduration = 0
		if framen == 15:
			colors.append([tduration*2,'green','Combine to get the equation of the line'])
			tduration = 0
		f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'tan'+str(framen)+'.tex','w')
		f.write(thestr)
		f.close()

		if framen == 0:
			ffs.write(str(framen+1)+'a\n')
			ffs.write('00:00:00.000 --> 00:'+tstamp(2.0)+'00\n')
			ffs.write("To determine the equation of a line we need\n\n")

			ffs.write(str(framen+1)+'b\n')
			ffs.write('00:00:02.000 --> 00:'+tstamp(4.0)+'00\n')
			ffs.write("to know the slope and the\n\n")

			ffs.write(str(framen+1)+'c\n')
			ffs.write('00:00:04.000 --> 00:'+tstamp(6.0)+'00\n')
			ffs.write("x and y-coordinates of a point on the line.\n\n")
		if framen == 2:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:06.000 --> 00:'+tstamp(9.0)+'00\n')
			ffs.write("The x-coordinate of our point is given.\n\n")
		if framen == 3:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:09.000 --> 00:'+tstamp(12.0)+'00\n')
			ffs.write("The y-coordinate will be found by computing f(x0).\n\n")
		if framen == 4:
			ffs.write(str(framen+1)+'a\n')
			ffs.write('00:00:12.000 --> 00:'+tstamp(14.0)+'00\n')
			ffs.write("The slope of the line is found by\n\n")

			ffs.write(str(framen+1)+'b\n')
			ffs.write('00:00:14.000 --> 00:'+tstamp(16.0)+'00\n')
			ffs.write("evaluating the derivative at x0.\n\n")

		if framen == 5:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:16.000 --> 00:'+tstamp(20.0)+'00\n')
			ffs.write("Compute y0 by plugging x0 into f(x).\n\n")
		if framen == 7:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:20.000 --> 00:'+tstamp(24.0)+'00\n')
			ffs.write("Evaluate to find y0.\n\n")

		if framen == 9:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:24.000 --> 00:'+tstamp(29.0)+'00\n')
			ffs.write("To compute the slope, first differentiate f(x).\n\n")
		if framen == 11:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:29.000 --> 00:'+tstamp(36.0)+'00\n')
			ffs.write("Then plug in x0 and evaluate.\n\n")

		if framen == 15:
			ffs.write(str(framen+1)+'\n')
			ffs.write('00:00:36.000 --> 00:'+tstamp(40.0)+'00\n')
			ffs.write("Finally, plug the values into the formula for the equation of a line.\n\n")

		if framen == 0:
			ff.write("file '"+hashprefix+'tan'+str(framen)+".png'\nduration "+str(duration+.1)+"\n\n")
		else:
			ff.write("file '"+hashprefix+'tan'+str(framen)+".png'\nduration "+str(duration+.005)+"\n\n")
		#worker(hashprefix,framen)
		os.system('./outputLatex.sh -c "'+hashprefix+'tan'+str(framen)+'"')
	ff.write("file '"+hashprefix+'tan'+str(15)+".png'\nduration "+str(2.005)+"\n\n")
	ff.close()
	ffs.close()
	os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'tangent.mp4 -y')
	jsoncolors = []

	for i in colors:
		jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	return 'new/'+hashprefix+'tangent.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
#run_it('x^3',3,'zza')