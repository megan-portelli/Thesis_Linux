#include <stdio.h>
#include "url_parser.h"

int main(int argc, char **argv)
{
	URL_COMPONENTS *c;

	if(argc == 0){
		fprintf(stderr, "No URL passed.\n");
		return 1;
	}

	c = parse_url(argv[1]);
	if (!c) {
		fprintf(stderr, "Invalid URL");
		return -1;
	}

	// printf("Scheme: %s\n", c->scheme ? c->scheme : "");
	// printf("Host:   %s\n", c->host ? c->host : "");
	// if (c->port != -1) {
	// 	printf("Port:   %d\n", c->port);
	// }
	// printf("Path:   %s\n", c->path ? c->path : "");
	// printf("Query:  %s\n", c->query ? c->query : "");

	free_url_components(c);

	return 0;
}