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

PREFIX1="\documentclass[12pt]{article}$PACKAGES\pagestyle{empty}\renewcommand{\baselinestretch}{1.5}\usepackage{graphicx}\newcommand*{\Scale}[2][4]{\scalebox{#1}{\ensuremath{#2}}}\setlength{\parindent}{0pt}\usepackage[paperheight=9in,paperwidth=7.6in, margin=1in]{geometry}"
PREFIX2="\begin{document}\large$DISPLAY"
SUFFIX="$DISPLAY\end{document}"
echo $PREFIX1 > $TMPDIR/$BNAME.tex
echo "\usepackage{color}\newcommand*{\mathcolor}{}" >> $TMPDIR/$BNAME.tex
echo "\def\mathcolor#1#{\mathcoloraux{#1}}" >> $TMPDIR/$BNAME.tex
echo "\newcommand*{\mathcoloraux}[3]{%" >> $TMPDIR/$BNAME.tex
echo "  \protect\leavevmode" >> $TMPDIR/$BNAME.tex
echo "  \begingroup" >> $TMPDIR/$BNAME.tex
echo "    \color#1{#2}#3%" >> $TMPDIR/$BNAME.tex
echo "  \endgroup" >> $TMPDIR/$BNAME.tex
echo "}" >> $TMPDIR/$BNAME.tex
echo $PREFIX2$FORMULA$SUFFIX >> $TMPDIR/$BNAME.tex

latex -halt-on-error -output-directory=$TMPDIR $TMPDIR/$BNAME.tex | sed -n '/^!/,/^ /p'

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.dvi $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
    exit 1
fi

dvipng -bg $BACKGROUND -o $FNAMET -q -T 7in,9in -D 120 -z 3 $TMPDIR/$BNAME.dvi > /dev/null
rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.dvi $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
montage $FNAMEOLD images/blank.png -geometry 600x771+1+1 $FNAME
montage $FNAMEOLD $FNAMET -geometry 600x771+1+1 $FNAME2