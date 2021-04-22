from bs4 import BeautifulSoup
import requests


def retrieve_posts(client_gramho_url):
    # retrieve all subdomain links from instagram account 
    # using instagram analytics viewer Gramho
    
    html = requests.get(client_gramho_url).content #LOAD PROFILE URL HERE
    soup = BeautifulSoup(html, 'lxml')
    subdomains = soup.find_all('div',class_='photo')
    retrieved = []
    for subdomain in subdomains:
        retrieved.append(subdomain.find('a')['href'])
    return retrieved


def extract_post_meta(posts):
    # define a class object to hold various attributes for a post
    class Entry:
        def __init__(self, img_src, total_comments, total_likes, post_date, post_descrip, comments):
            self.img_src        = img_src
            self.total_comments = total_comments
            self.total_likes    = total_likes
            self.post_date      = post_date
            self.post_descrip   = post_descrip
            self.comments       = comments

    posts_meta = []

    # loop through each post and extract information
    for post in posts:
        html =requests.get(post).content
        soup = BeautifulSoup(html, 'lxml')
        print('EXTRACTING URL: ', post)
        
        # EXTRACT post image
        try:
            post_img = soup.find('div', class_='item').find('img')['src']

        # exception handling for alternate html structure
        except:
            
            try:
                post_img = soup.find('div', class_='single-photo').find('img')['src']
            
            # exception handling when a video is posted instead of an image
            except:
                try:
                    post_img = soup.find('video')['poster']
                except:
                    print('ERROR - UNABLE TO SAVE IMAGE')
                    print('SAVING IMAGE AS NONE DATATYPE')
                    post_img = None
        
        # EXTRACT total number of comments and likes
        temp_str = []
        temp_str.append(soup.find("span", class_="icon-chat").get_text())
        temp_str.append(soup.find("span", class_="icon-thumbs-up-alt").get_text())
        total_comments = temp_str[0][0:temp_str[0].find(" ")]
        total_likes = temp_str[1][0:temp_str[1].find(" ")]

        # EXTRACT the relative date for instagram post --> Use for SQL primary key? (does not cater for duplicate posts on the same day) Maybe date + time
        post_date = soup.find("div", class_="single-photo-time").get_text()
        
        # EXTRACT post descrip
        post_descrip = soup.find("div", class_="single-photo-description").get_text().strip()

        # EXTRACT comments, loop through each comment, store author and comment as array [[user1, comment1], [user2, comment2], ...]
        comments=soup.find_all('div', class_="comment")
        comment_meta = []

        for comment in comments:
            meta_user = comment.find('div', class_="comment-user").get_text().strip()
            meta_comment = comment.find('div', class_="comment-text").get_text().strip()
        
            meta_temp = [meta_user, meta_comment]
            comment_meta.append(meta_temp)

        posts_meta.append(Entry(post_img, total_comments, total_likes, post_date, post_descrip, comment_meta))
    return posts_meta

def export_post_meta(posts_meta):
    print('exporting post META...')