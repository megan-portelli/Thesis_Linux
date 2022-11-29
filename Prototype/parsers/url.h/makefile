main: main.c url.c
	sudo gcc -Wall main.c url.c -o main -lm

test: url_parser
	./main https://google.com

clean:
	-rm main