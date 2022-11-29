main: main.c
	sudo gcc -Wall main.c -o main -lm

test: url_parser
	./main https://google.com/

clean:
	-rm main