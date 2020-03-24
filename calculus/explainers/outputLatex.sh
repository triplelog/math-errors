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
	f)
	    FORMULA=$OPTARG
	    ;;
	c)
	    FNAME=$OPTARG
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


BNAME=${FNAME##*/}
TMPDIR=/tmp/me/mneri/pnglatex

if [ ! -d $TMPDIR ]; then
    mkdir -p $TMPDIR
fi


pdflatex -halt-on-error -output-directory=$TMPDIR $TMPDIR/$BNAME.tex | sed -n '/^!/,/^ /p'
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.dvi $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
    exit 1
fi
mudraw -w 1200 -h 600 -r 100 -c rgb -o $FNAME.png $TMPDIR/$BNAME.pdf
#convert ../images/new/$FNAME.png ../images/new/$FNAME.bmp > /dev/null
rm $TMPDIR/$BNAME.aux $TMPDIR/$BNAME.pdf $TMPDIR/$BNAME.log $TMPDIR/$BNAME.tex > /dev/null
