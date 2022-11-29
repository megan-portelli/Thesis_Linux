#include <stdio.h>
#include <stdlib.h>
#include "url.h"

int main (int argc, char **argv) {
    url_data_t * parsed_url ;

    if(argc == 0){
        fprintf(stderr, "No URL passed.\n");
        return 1;
    }

    parsed_url = (url_data_t *)malloc(sizeof(url_data_t));
    parsed_url = url_parse(argv[1]);

    if(!parsed_url){
        fprintf(stderr, "Invalid URL");
        return -1;
    }

    //url_data_inspect(parsed_url);
    
    url_free(parsed_url);

    return 0;
}