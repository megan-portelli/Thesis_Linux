ALL = unittest
CC = gcc
CFLAGS = -Wall -O2 -MMD
LDFLAGS =
SOURCES = $(wildcard ./*.c)
DEPENDS = $(SOURCES:.c=.d)

all: $(ALL)

main: main.c url_parser.c
	sudo gcc -Wall main.c url_parser.c -o main -lm

unittest: unittest.o url_parser.o
	$(CC) -o $@ $^ $(LDFLAGS)

clean:
	-rm -f *.o
	-rm -f *.d
	-rm -f $(ALL)

-include $(DEPENDS)
