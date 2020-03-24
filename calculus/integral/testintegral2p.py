#!/bin/bash

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

BACKGROUND=White
FNAME=`date +%s%N`.png
DISPLAY=
PACKAGES=
SIZE=13

while getopts b:d:f:o:t:c:a:p:s: ARG; do
    case $ARG in
	b)
	    BACKGROUND=$OPTARG
	    ;;
	d)
	    DISPLAY=\$\$
	    ;;
	f)
	    FORMULA=$OPTARG
	    ;;
	o)
	    FNAMEOLD=$OPTARG
	    ;;
	t)
	    FNAMET=$OPTARG
	    ;;
	c)
	    FNAME=$OPTARG
	    ;;
	a)
	    FNAME2=$OPTARG
	    ;;
	p)
	    IFS=":"
	    PLIST=($OPTARG)
	    
	    for P in $PLIST; do
		PACKAGES=$PACKAGES\\usepackage{$P}
	    done
	    ;;
	s)
	    SIZE=$OPTARG
	    ;;
    esac
done

if [ ! "$FORMULA" ]; then
    echo "No input formula."
    exit 0
fi

BNAME=${FNAME##*/}
TMPDIR=/tmp/me/mneri/pnglatex

if [ ! -d $TMPDIR ]; then
    mkdir -p $TMPDIR
fi

PREFIX1="\documentclass{article}\usepackage[utf8]{inputenc}\usepackage{tikz}\usepackage{calc}\usepackage[margin=0.1in,paperwidth=12in,paperheight=14.25in]{geometry}\usepackage{ifthen}\usepackage{hyperref}\usetikzlibrary{shapes.geometric, arrows}\tikzstyle{startstop} = [rectangle, minimum width=6cm, minimum height=1cm,text centered, draw=black, fill=red!30]\tikzstyle{process} = [rectangle, rounded corners, minimum width=6.05cm, minimum height=1cm, text centered, text width=6.05cm, draw=black, fill=orange!30]\tikzstyle{processlong} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=green!30]\tikzstyle{processop} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=orange!30]\tikzstyle{processfn} = [rectangle, rounded corners, minimum height=1cm, text centered, draw=black, fill=red!30]\tikzstyle{processbegin} = [rectangle, minimum width=6cm, minimum height=1cm, text centered, text width=6cm, draw=black, fill=green!30]\tikzstyle{processred} = [rectangle, minimum width=6cm, minimum height=1cm, text centered, text width=6cm, draw=black, fill=red!30]\tikzstyle{decision} = [diamond, minimum width=6cm, minimum height=1cm, text centered, draw=black, fill=green!30]\tikzstyle{arrow} = [thick,->,>=stealth]"
PREFIX2="\begin{document}\large$DISPLAY"
SUFFIX="$DISPLAY\end{tikzpicture}\end{document}"
FORMULA="\newlength{\myla}\settowidth{\myla}{$\displaystyle\int x^{3}dx$}\newlength{\mylb}\settowidth{\mylb}{$+$}\newlength{\mylc}\settowidth{\mylc}{$\displaystyle\int 3dx$}\newlength{\mylaa}\settowidth{\mylaa}{$\frac{x^{2}}{2}$}\newlength{\mylca}\settowidth{\mylca}{\$3 x$}\newlength{\mylaaa}\settowidth{\mylaaa}{$\frac{x^{2}}{2} + 3 x$}\newlength{\tempc}\setlength{\tempc}{-20pt+20pt+\mylaaa}\ifthenelse{\mylaa<\tempc}{\def\mylaa{\tempc}}{}\newlength{\tempaa}\setlength{\tempaa}{-20pt+20pt+\mylca}\ifthenelse{\mylc<\tempaa}{\def\mylc{\tempaa}}{}\newlength{\tempaaa}\setlength{\tempaaa}{-20pt+20pt+\mylaa}\ifthenelse{\myla<\tempaaa}{\def\myla{\tempaaa}}{}\begin{tikzpicture}[node distance=100pt]\node (dec0) [processlong] {$\displaystyle\int x^{3} + 3dx$};\node (deca) [processlong, below of=dec0, xshift=-(-20pt+20pt+\myla+20pt+\mylb+20pt+\mylc)/2+\myla/2, yshift=-0pt ] {$\displaystyle\int x^{3}dx$};\node (decb) [processlong, right of=deca, xshift=-80pt+(\myla+\mylb)/2] {$+$};\node (decc) [processlong, right of=decb, xshift=-80pt+(\mylb+\mylc)/2] {$\displaystyle\int 3dx$};\node (decaa) [processlong, below of=deca, xshift=-(-20pt+20pt+\mylaa)/2+\mylaa/2, yshift=-0pt ] {$\frac{x^{2}}{2}$};\node (decca) [processlong, below of=decc, xshift=-(-20pt+20pt+\mylca)/2+\mylca/2, yshift=-0pt ] {\$3 x$};\node (decaaa) [processlong, below of=dec0, xshift=-(-20pt+20pt+\mylaaa)/2+\mylaaa/2, yshift=-200pt ] {$\frac{x^{2}}{2} + 3 x$};\draw [arrow] (dec0.south) -- node[anchor=north] {} (deca.north);\draw [arrow] (dec0.south) -- node[anchor=north] {} (decb.north);\draw [arrow] (dec0.south) -- node[anchor=north] {} (decc.north);\draw [arrow] (deca.south) -- node[anchor=north] {} (decaa.north);\draw [arrow] (decc.south) -- node[anchor=north] {} (decca.north);\draw [arrow] (decaa.south) -- node[anchor=north] {} (decaaa.north);\draw [arrow] (decb.south) -- node[anchor=north] {} (decaaa.north);\draw [arrow] (decca.south) -- node[anchor=north] {} (decaaa.north);"


echo $PREFIX1 > $TMPDIR/$BNAME.tex
echo $PREFIX2$FORMULA$SUFFIX >> $TMPDIR/$BNAME.tex

#latex -halt-on-error -output-directory=$TMPDIR $TMPDIR/$BNAME.tex | sed -n '/^!/,/^ /p'

#if [ ${PIPESTATUS[0]} -ne 0 ]; then
#    rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.dvi $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
#    exit 1
#fi

#dvipng -bg $BACKGROUND -o 'img.png' -q -T 7in,9in -D 120 -z 3 $TMPDIR/$BNAME.dvi > /dev/null
#rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.dvi $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
#montage $FNAMEOLD images/blank.png -geometry 600x771+1+1 $FNAME
#montage $FNAMEOLD $FNAMET -geometry 600x771+1+1 $FNAME2