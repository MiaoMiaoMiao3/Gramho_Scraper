from os import environ

import scraping_functions as functions

def main():

    retrieved = functions.retrieve_posts(environ.get('client_insta'))
    print('Subdomains retrieved. Extracting post meta....\n')
    
    post_meta = functions.extract_post_meta(retrieved)
    print('Extraction....COMPLETE\n')

    functions.export_post_meta(post_meta)

    print('EXPORT COMPLETE! See EXPORT.CSV for')

if __name__ == "__main__":
    main()
	