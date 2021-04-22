from os import environ

import scraping_functions as functions

def main():

    retrieved = functions.retrieve_posts(environ.get('client_insta'))
    print('Subdomains retrieved. Extracting post meta....')
    
    post_meta = functions.extract_post_meta(retrieved)
    print('Extraction....COMPLETE')

    functions.export_post_meta(post_meta)

    print('EXPORT COMPLETE! SEE EXPORT.CSV FOR RESULTS')

if __name__ == "__main__":
    main()