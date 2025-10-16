
#	Hugh Fisher


## Build options

CC = gcc
CXX = g++
CFLAGS = -I. -Wall -O2 $$(pkg-config --cflags libpng)
LDFLAGS = $$(pkg-config --libs libpng)


OBJS =	\
	fail.o		\
	julia.o

LIBS = -lm -lpthread \

##	Full program

CXXFLAGS = $(CFLAGS)

julia : $(OBJS)
	/bin/rm -f julia
	$(CXX) $(CFLAGS) -o julia $(OBJS) $(LDFLAGS) $(LIBS)

clean:
	/bin/rm -f *.o core julia

depend:
	makedepend -fMakefile -w10 -Y *.c *.cpp
