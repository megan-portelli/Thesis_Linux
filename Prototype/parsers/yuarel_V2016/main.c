#include <stdlib.h>
#include <stdio.h>
#include "yuarel.h"

int main(int argc, char **argv)
{
	int p;
	struct yuarel url;
	char *parts[3];
	struct yuarel_param params[3];

	int error;

	if(argc == 0){
		fprintf(stderr, "No URL passed.\n");
		return 1;
	}

	error = yuarel_parse(&url, argv[1]);

	if (error !=0) {
		fprintf(stderr, "Invalid URL\n");
		return 2;
	}

	// printf("Struct values:\n");
	// printf("\tscheme:\t\t%s\n", url.scheme);
	// printf("\thost:\t\t%s\n", url.host);
	// printf("\tport:\t\t%d\n", url.port);
	// printf("\tpath:\t\t%s\n", url.path);
	// printf("\tquery:\t\t%s\n", url.query);
	// printf("\tfragment:\t%s\n", url.fragment);

	if (3 != yuarel_split_path(url.path, parts, 3)) {
		fprintf(stderr, "Could not split path!\n");
		return 3;
	}

	// printf("\nPath parts: '%s', '%s', '%s'\n\n", parts[0], parts[1], parts[2]);

	// printf("Query string parameters:\n");

	// p = yuarel_parse_query(url.query, '&', params, 3);
	// while (p-- > 0) {
	// 	printf("\t%s: %s\n", params[p].key, params[p].val);
	// }

	return 0;
}