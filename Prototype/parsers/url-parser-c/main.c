#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "url_parser.h"

int main(int argc, char **argv) {
	int error;
	url_parser_url_t *parsed_url;

	if (argc == 0) {
		fprintf(stderr, "No URL passed.\n");
		return 1;
	}

		parsed_url = (url_parser_url_t *) malloc(sizeof(url_parser_url_t));
		error = parse_url(argv[1], true	, parsed_url);
		if (error != 0) {
			fprintf(stderr, "Invalid URL \"%s\".\n", argv[1]);
			return -1;
		}

		// printf("Protocol: '%s' - Host: '%s' - Port: '%d' - Path: '%s' - Query String: '%s' Valid Host: %d - IP: '%s'\n",
		// 	parsed_url->protocol, parsed_url->host, parsed_url->port, parsed_url->path,
		// 	parsed_url->query_string, parsed_url->host_exists, parsed_url->host_ip);
		free_parsed_url(parsed_url);

	return 0;

}