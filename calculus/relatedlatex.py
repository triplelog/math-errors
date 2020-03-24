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
					


def makegraph():
	
	graphstr = r'''\begin{center}
		\begin{tikzpicture}[xscale=1,yscale=2.08668478324271]
		  \draw[->] (-0.5,0) -- (4.5,0) node[right] {$x$};
		  \draw[->] (0,-1.19897156653332) -- (0,1.19717376416200) node[above] {$y$};
		  
		  \draw[domain=-0.5:4.5,smooth,variable=\x,blue] plot ({\x},{sin((\x) r)});
		  \draw[fill,red] (2,0.909297426825682) circle (.05);
		\end{tikzpicture}
		\end{center}
		
			\end{minipage}\hfill'''
	return graphstr

def maketext():
	
	
	textstr = r'''\begin{minipage}{.475\linewidth}
		\begin{center}
			A 15 foot ladder is resting against the wall. The bottom is initially 10 feet away from the wall and is being pushed towards the wall at a rate of .25 ft/sec. How fast is the top of the ladder moving up the wall 12 seconds after we start pushing?
		\end{center}'''
	return textstr

def makelist(framen,a,b,c,da,db,dc,asolved,bsolved,csolved,dasolved,dbsolved,dcsolved,asolving,bsolving,csolving,dasolving,dbsolving,dcsolving):

	eqstr = r''
	if framen > 0:
		eqstr = r'''a^2+b^2& = c^2\\'''
	deqstr = r''
	if framen > 1:
		deqstr = r'''2a\frac{da}{dt}+2b\frac{db}{dt} & = 2c\frac{dc}{dt}\\'''

	astr = r''
	if framen == asolving+1:
		astr = r'''a & = \sqrt{c^2-b^2}\\'''
	elif framen > asolved:
		astr = r'''a & = '''+cleandecimal(a,5)+r'''\\'''
	elif framen > 2:
		astr = r'''a & = \\'''
	bstr = r''
	if framen == bsolving+1:
		bstr = r'''b & = \sqrt{c^2-a^2}\\'''
	elif framen > bsolved:
		bstr = r'''b & = '''+cleandecimal(b,5)+r'''\\'''
	elif framen > 2:
		bstr = r'''b & = \\'''
	cstr = r''
	if framen == csolving+1:
		cstr = r'''c & = \sqrt{a^2+b^2}\\'''
	elif framen > csolved:
		cstr = r'''c & = '''+cleandecimal(c,5)+r'''\\'''
	elif framen > 2:
		cstr = r'''c & = \\'''

	dastr = r''
	if framen == dasolving + 1:
		dastr = r'''\frac{da}{dt} & = \frac{2c\frac{dc}{dt}-2b\frac{db}{dt}}{2a}\\'''
	elif framen > dasolved:
		dastr = r'''\frac{da}{dt} & = '''+cleandecimal(da,5)+r'''\\'''
	elif framen > 3:
		dastr = r'''\frac{da}{dt} & = \\'''
	dbstr = r''
	if framen == dbsolving + 1:
		dbstr = r'''\frac{db}{dt} & = \frac{2c\frac{dc}{dt}-2a\frac{da}{dt}}{2b}\\'''
	elif framen > dbsolved:
		dbstr = r'''\frac{db}{dt} & = '''+cleandecimal(db,5)+r'''\\'''
	elif framen > 3:
		dbstr = r'''\frac{db}{dt} & = \\'''
	dcstr = r''
	if framen == dcsolving + 1:
		dcstr = r'''\frac{dc}{dt} & = \frac{2a\frac{da}{dt}+2b\frac{db}{dt}}{2c}\\'''
	elif framen > dcsolved:
		dcstr = r'''\frac{dc}{dt} & = '''+cleandecimal(dc,5)+r'''\\'''
	elif framen > 3:
		dcstr = r'''\frac{dc}{dt} & = \\'''



	liststr = r'''\begin{minipage}{.5\linewidth}
			\scalebox{1.9}{\parbox{.4\linewidth}{%
			\large
			\begin{align*}'''+eqstr+deqstr+astr+bstr+cstr+dastr+dbstr+dcstr+r'''
			\end{align*}
			}}

	\end{minipage}\end{document}'''
	return liststr


def run_it(hashprefix):
	startstr = r'''\documentclass{article}
	\usepackage[utf8]{inputenc}
	\usepackage{tikz}
	\usepackage{amsmath}
	\usepackage{graphicx}
	\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

	\usetikzlibrary{shapes.geometric, arrows}


	\begin{document}
	\huge'''

	ff = open('images/new/'+hashprefix+'inputs.ffconcat','w')
	ff.write('ffconcat version 1.0\n\n')
	ffs = open('images/new/'+hashprefix+'subtitles.vtt','w')
	ffs.write('WEBVTT\n\n')
	colors = []
	tduration = 0
	durations = [3.0,3.0,3.0,3.0,4.0,2.0,2.0,2.0,2.0,2.5,2.5,1.0,2.0,2.0,2.0,2.0]
	initialvals = {'b':12}
	constantvals = {'c':15}
	knownrates = {'dc':0,'db':-.25}
	solvedvals = constantvals
	solvedrates = knownrates
	tval = 12
	cframe = 4
	asolving = -2
	bsolving = -2
	csolving = -2
	dasolving = -2
	dbsolving = -2
	dcsolving = -2
	if 'a' in constantvals:
		asolved = cframe
		cframe += 1
	if 'b' in constantvals:
		bsolved = cframe
		cframe += 1
	if 'c' in constantvals:
		csolved = cframe
		cframe += 1
	if 'da' in knownrates:
		dasolved = cframe
		cframe += 1
	if 'db' in knownrates:
		dbsolved = cframe
		cframe += 1
	if 'dc' in knownrates:
		dcsolved = cframe
		cframe += 1

	if 'a' not in constantvals and 'da' in knownrates:
		if 'a' in initialvals:
			solvedvals['a'] = tval*knownrates['da']+initialvals['a']
		else:
			solvedvals['a'] = tval*knownrates['da']
		asolved = cframe
		cframe += 1
	if 'b' not in constantvals and 'db' in knownrates:
		if 'b' in initialvals:
			solvedvals['b'] = tval*knownrates['db']+initialvals['b']
		else:
			solvedvals['b'] = tval*knownrates['db']
		bsolved = cframe
		cframe += 1
	if 'c' not in constantvals and 'dc' in knownrates:
		if 'c' in initialvals:
			solvedvals['c'] = tval*knownrates['dc']+initialvals['c']
		else:
			solvedvals['c'] = tval*knownrates['dc']
		csolved = cframe
		cframe += 1

	if 'a' not in solvedvals and 'b' in solvedvals and 'c' in solvedvals:
		solvedvals['a'] = (solvedvals['c']**2-solvedvals['b']**2)**.5
		asolving = cframe
		cframe += 1
		asolved = cframe
		cframe += 1
	if 'b' not in solvedvals and 'a' in solvedvals and 'c' in solvedvals:
		solvedvals['b'] = (solvedvals['c']**2-solvedvals['a']**2)**.5
		bsolving = cframe
		cframe += 1
		bsolved = cframe
		cframe += 1
	if 'c' not in solvedvals and 'b' in solvedvals and 'a' in solvedvals:
		solvedvals['c'] = (solvedvals['a']**2-solvedvals['b']**2)**.5
		csolving = cframe
		cframe += 1
		csolved = cframe
		cframe += 1

	if 'da' not in solvedrates and 'a' in solvedvals and 'b' in solvedvals and 'c' in solvedvals and 'db' in solvedrates and 'dc' in solvedrates:
		solvedrates['da'] = (solvedvals['c']*2*solvedrates['dc']-solvedvals['b']*2*solvedrates['db'])/(2*solvedvals['a'])
		dasolving = cframe
		cframe += 1
		dasolved = cframe
		cframe += 1
	if 'db' not in solvedrates and 'a' in solvedvals and 'b' in solvedvals and 'c' in solvedvals and 'da' in solvedrates and 'dc' in solvedrates:
		solvedrates['db'] = (solvedvals['c']*2*solvedrates['dc']-solvedvals['a']*2*solvedrates['da'])/(2*solvedvals['b'])
		dbsolving = cframe
		cframe += 1
		dbsolved = cframe
		cframe += 1
	if 'dc' not in solvedrates and 'a' in solvedvals and 'b' in solvedvals and 'c' in solvedvals and 'db' in solvedrates and 'da' in solvedrates:
		solvedrates['dc'] = (solvedvals['a']*2*solvedrates['da']+solvedvals['b']*2*solvedrates['db'])/(2*solvedvals['c'])
		dcsolving = cframe
		cframe += 1
		dcsolved = cframe
		cframe += 1

	for framen in range(0,15):
		duration = durations[framen]
		tduration += duration
		thestr = startstr

		thestr += '\n'+maketext()

		thestr += '\n'+makegraph()

		thestr += '\n'+makelist(framen,solvedvals['a'],solvedvals['b'],solvedvals['c'],solvedrates['da'],solvedrates['db'],solvedrates['dc'],asolved,bsolved,csolved,dasolved,dbsolved,dcsolved,asolving,bsolving,csolving,dasolving,dbsolving,dcsolving)

		
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
		f = open('/tmp/me/mneri/pnglatex/'+hashprefix+'rel'+str(framen)+'.tex','w')
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
			ff.write("file '"+hashprefix+'rel'+str(framen)+".png'\nduration "+str(duration+.1)+"\n\n")
		else:
			ff.write("file '"+hashprefix+'rel'+str(framen)+".png'\nduration "+str(duration+.005)+"\n\n")
		#worker(hashprefix,framen)
		os.system('./outputLatex.sh -c "'+hashprefix+'rel'+str(framen)+'"')
	ff.write("file '"+hashprefix+'rel'+str(15)+".png'\nduration "+str(2.005)+"\n\n")
	ff.close()
	ffs.close()
	os.system('ffmpeg -f concat -i images/new/'+hashprefix+'inputs.ffconcat -pix_fmt yuv420p -preset ultrafast -r 2 images/new/'+hashprefix+'related.mp4 -y')
	jsoncolors = []

	for i in colors:
		jsoncolors.append({'time':i[0],'type':i[1],'text':toJavascript(i[2])})
	return 'new/'+hashprefix+'related.mp4', jsoncolors, 'new/'+hashprefix+'subtitles.vtt'
#run_it('x^3',3,'zza')