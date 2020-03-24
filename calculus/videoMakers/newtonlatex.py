import sympy
from sympy import *
from sympy.abc import x
import sys

    
def cleandecimal(inputval,maxd):
	rval = str(round(inputval,maxd))
	while rval.find('.') > -1 and (rval[-1] == '0' or rval[-1] == '.'):
		rval=rval[:-1]
	return rval

def getnewtonfn(fn):
	indexeq = fn.find('=')
	if indexeq == -1:
		try:
			newtonfn = sympy.sympify(fn)
		except:
			newtonfn = ''
		return False,newtonfn
	else:
		leftfn = fn[:indexeq]
		rightfn = fn[indexeq+1:]
		try:
			newtonfn = sympy.sympify(leftfn+'-('+rightfn+')')
		except:
			newtonfn = ''
		return True,newtonfn,fn
		
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
					
startstr = r'''\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[margin=0.05in,paperwidth=12in,paperheight=6in]{geometry}

\usetikzlibrary{shapes.geometric, arrows}


\begin{document}
\huge'''


def makegraph(fn,xlist,ylist,dfn,framen,ymin,ymax,xmin,xmax):
	fnstr = r'f(x)='+sympy.latex(fn[1])
	x0str = str(xlist[0])
	
	xaxisstr = r'''\draw[->] ('''+str(xmin-(xmax-xmin)*.5)+r''',0) -- ('''+str(xmax+(xmax-xmin)*.5)+r''',0) node[right] {$f(x)=0$};'''
	yaxisstr = r'''\draw[->] (0,'''+str(ymin-(ymax-ymin)*.25)+r''') -- (0,'''+str(ymax+(ymax-ymin)*.25)+r''') node[above] {$y$};'''
	if xmin-(xmax-xmin)*.5 > 0 or xmax+(xmax-xmin)*.5 < 0:
		yaxisstr = ''
	if ymin-(ymax-ymin)*.25 >0 or ymax+(ymax-ymin)*.25 < 0:
		xaxisstr = ''
	graphstr = r'''\begin{minipage}{.575\linewidth}
		\begin{center}
			Approximate a solution to the equation $'''+fnstr+r'''$ near $x='''+x0str+r'''$.
		\end{center}
		\begin{center}
		\begin{tikzpicture}[xscale='''+str(10.0/(2.0*xmax-2.0*xmin))+r''',yscale='''+str(10.0/(1.5*ymax-1.5*ymin))+r''']
		  '''+xaxisstr+r'''
		  '''+yaxisstr+r'''
		  
		  \draw[domain='''+str(xmin-(xmax-xmin)*.5)+r''':'''+str(xmax+(xmax-xmin)*.5)+r''',smooth,variable=\x,blue] plot ({\x},{'''+trigradian(str(fn[1]).replace('x','(\\x)').replace('**','^'))+r'''}) node[right] {$'''+fnstr+r'''$};

		\end{tikzpicture}
		\end{center}
			\end{minipage}\hfill'''
			
	return graphstr

def makelist(fn,xlist,ylist,dfn,framen,ymin,ymax,xmin,xmax):
		
	x0str = r''
	if framen > 2:
		x0str = str(xlist[0])
	
	dfnstr = r''
	if framen > 1:
		dfnstr = sympy.latex(dfn)
	
	fnstr = r''
	if framen > 0:
		fnstr = sympy.latex(fn[1])
	
	x1str = r''
	if framen > 4:
		x1str = str(xlist[1])
	x2str = r''
	if framen > 5:
		x2str = str(xlist[2])
	x3str = r''
	if framen > 6:
		x3str = str(xlist[3])
	x4str = r''
	if framen > 7:
		x4str = str(xlist[4])
	x5str = r''
	if framen > 8:
		x5str = str(xlist[5])
	x6str = r''
	if framen > 9:
		x6str = str(xlist[6])
	x7str = r''
	if framen > 10:
		x7str = str(xlist[7])
	liststr = r'''\begin{minipage}{.4\linewidth}
			\scalebox{1.75}{\parbox{.4\linewidth}{%
			\large
			\begin{align*}
		f(x) & = '''+fnstr+r'''\\
		f'(x) & = '''+dfnstr+r'''\\
		x_{n+1} & = x_n-\frac{f(x_n)}{f'(x_n)}\\
		x_0 & = '''+x0str+r'''\\
		x_1 & = '''+x1str+r'''\\
		x_2 & = '''+x2str+r'''\\
		x_3 & = '''+x3str+r'''\\
		x_4 & = '''+x4str+r'''\\
		x_5 & = '''+x5str+r'''\\
		x_6 & = '''+x6str+r'''\\
		x_7 & = '''+x7str+r'''\\
			\end{align*}
			}}
	\end{minipage}

	\end{document}'''
	return liststr
	
fn = getnewtonfn('x^2=55')
x0 = 7
xlist = [x0]
ylist = []
dfn = sympy.diff(fn[1])
for i in range(0,7):
	dfnx0 = dfn.evalf(subs={x:xlist[i]})
	y0 = fn[1].evalf(subs={x:xlist[i]})
	xlist.append(xlist[i]-y0/dfnx0)
	ylist.append(y0)
ylist.append(fn[1].evalf(subs={x:xlist[7]}))

xmin = xlist[0]
xmax = xmin
for i in xlist:
	if i < xmin:
		xmin = i
	elif i > xmax:
		xmax = i
		
ymin = ylist[0]
ymax = ymin
for i in ylist:
	if i < ymin:
		ymin = i
	elif i > ymax:
		ymax = i
yxmin = fn[1].evalf(subs={x:xmin-(xmax-xmin)*.5})
yxmax = fn[1].evalf(subs={x:xmax+(xmax-xmin)*.5})
if yxmin < ymin:
	ymin = yxmin
elif yxmin > ymax:
	ymax = yxmin
if yxmax < ymin:
	ymin = yxmax
elif yxmax > ymax:
	ymax = yxmax

framen = int(sys.argv[1])
thestr = startstr



#thestr += '\n'+maketext(fn,x0,framen,dfn,dfnx0,y0)
#thestr += '\n'+makelist(fn,x0,framen,dfn,dfnx0,y0)
thestr += '\n'+makegraph(fn,xlist,ylist,dfn,framen,ymin,ymax,xmin,xmax)
thestr += '\n'+makelist(fn,xlist,ylist,dfn,framen,ymin,ymax,xmin,xmax)

print(thestr)