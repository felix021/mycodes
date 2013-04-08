##  Percy++
##  Copyright 2007 Ian Goldberg <iang@cs.uwaterloo.ca>
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of version 2 of the GNU General Public License as
##  published by the Free Software Foundation.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  There is a copy of the GNU General Public License in the COPYING file
##  packaged with this plugin; if you cannot find it, write to the Free
##  Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
##  02111-1307  USA

#-DTEST_RR is for Roth-Ruckenstein algorithm
#CXXFLAGS=-Wall -g -O2 -DTEST_RR
CXXFLAGS=-Wall -g -O2
LDLIBS=-lntl -lgmp

OBJS=recover.o rr_roots.o ZZ_pXY.o

main: $(OBJS)
	g++ -o $@ $^ $(LDLIBS)
	echo "done"

clean:
	-rm -f *.o

veryclean: clean
	-rm -f $(TARGETS)
