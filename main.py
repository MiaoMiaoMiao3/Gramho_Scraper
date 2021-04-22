from bs4 import BeautifulSoup
import requests
from os import environ

def main():
    retrieved = retrieve_posts()
    print('Subdomains retrieved. Extracting post meta....')
    extract_post_meta(retrieved)
    print('Extraction....COMPLETE')

def retrieve_posts():
    # retrieve all subdomain links from instagram account 
    # using instagram analytics viewer Gramho
    html = requests.get(environ.get('client_insta')).content #LOAD PROFILE URL HERE
    soup = BeautifulSoup(html, 'lxml')
    subdomains = soup.find_all('div',class_='photo')
    retrieved = []
    for subdomain in subdomains:
        retrieved.append(subdomain.find('a')['href'])
    return retrieved

def extract_post_meta(retrieved):
    # define a class object to hold various attributes for a post
    class Entry:
        def __init__(self, img_src, post_date, post_descrip, comments):
            self.img_src        = img_src
            self.post_date      = post_date
            self.post_descrip   = post_descrip
            self.comments       = comments

    # loop through each post and extract information
    for subdomain in retrieved:
        html =requests.get(subdomain).content
        soup = BeautifulSoup(html, 'lxml')
        print('SUBDOMAIN: ', subdomain)
        
        # extract post image
        try:
            post_image = soup.find('div', class_='item').find('img')['src']

        # exception handling for alternate html structure
        except:
            
            try:
                post_image = soup.find('div', class_='single-photo').find('img')['src']
            
            # exception handling when a video is posted instead of an image
            except:
                try:
                    post_image = soup.find('video')['poster']
                except:
                    print('ERROR - UNABLE TO SAVE IMAGE')
                    print('SAVING IMAGE AS NONE DATATYPE')
                    post_image = None
        
        post_date = soup.find("div", class_="single-photo-time").get_text()
        print(post_date)


def export_post_meta():
    print('exporting post META...')


if __name__ == "__main__":
    main()