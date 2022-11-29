#include <stdio.h>
#include <stdlib.h>
#include "url.h"

int main(int argc, char **argv) {

  url_t *parsed_url ;

  if(argc == 0){
    fprintf(stderr, "No URL passed.\n");
    return 1;
  }

    parsed_url = (url_t *)malloc(sizeof(url_t));
    parsed_url = url_parse(argv[1]);

    if(!parsed_url){
      fprintf(stderr, "Invalid URL");
      return -1;
    }

  // printf("PROTOCOL: %s\n", parsed_url->protocol);
  // printf("HOST: %s\n", parsed_url->host);
  // printf("PORT: %s\n", parsed_url->port);
  // printf("PATH: %s\n", parsed_url->path);
  url_free(parsed_url);
  return 0;
}