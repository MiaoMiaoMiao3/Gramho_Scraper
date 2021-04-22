from bs4 import BeautifulSoup
import requests
# TODO: move retrieve posts and export posts to separate files
# TODO: Create a more customizeable way for the user to specifiy what data to export and
# if and how data should be cleansed.

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
        def __init__(self, post_date, img_src, total_likes, total_comments, hashes_cnt, comments, post_descrip):
            self.post_date      = post_date
            self.img_src        = img_src
            self.total_likes    = total_likes
            self.total_comments = total_comments
            self.hashes_cnt     = hashes_cnt
            self.post_descrip   = post_descrip
            self.comments       = comments

    posts_meta = []
    hash_count = {}

    # loop through each post and extract information
    for post in posts:
        html =requests.get(post).content
        soup = BeautifulSoup(html, 'lxml')
        # print('EXTRACTING URL: ', post)
        
        # EXTRACT the relative date for instagram post --> Use for SQL primary key? (does not cater for duplicate posts on the same day) Maybe date + time
        post_date = soup.find("div", class_="single-photo-time").get_text()

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
        total_likes = temp_str[1][0:temp_str[1].find(" ")]
        total_comments = temp_str[0][0:temp_str[0].find(" ")]
        
        # EXTRACT post descrip -- from this we determined the hash count
        post_descrip = soup.find("div", class_="single-photo-description")
        descrip_hash = cleanse_text_only(post_descrip.find_all('a'))
        dictionary_count(hash_count, descrip_hash)

        # EXTRACT comments, loop through each comment, store author and comment as array [[user1, comment1], [user2, comment2], ...]
        comments=soup.find_all('div', class_="comment")
        comment_meta = []

        for comment in comments:
            meta_user = comment.find('div', class_="comment-user").get_text().strip()
            meta_comment = comment.find('div', class_="comment-text").get_text().strip()
        
            comment_meta.append(meta_comment)

        posts_meta.append(Entry(post_date, post_img, total_likes, total_comments, hash_count, comment_meta, post_descrip.get_text().strip()))
    return posts_meta


def cleanse_text_only(dirty_array):
    cleaned_array = dirty_array
    for i in range(0,len(cleaned_array)):
        cleaned_array[i] = cleaned_array[i].get_text()
        
    return (cleaned_array)

def dictionary_count(k, v):
    for value in v:
        try:
            k[value]+=1
        except:
            k[value] = 1

def export_post_meta(posts_meta):
    print('Exporting post META...')
    
    export_CSV = open('EXPORT.CSV', 'w+', encoding="utf8", newline='')
    
    print('writing to CSV.....')
    export_CSV.write('DATE| IMG_SRC| LIKES| COMMENTS_CNT| COMMENTS| DESCRIP_LF |\n')
    for post in posts_meta:
        
        export_CSV.write(post.post_date)
        export_CSV.write('|')
        export_CSV.write(post.img_src)
        export_CSV.write('|')
        export_CSV.write(post.total_likes)
        export_CSV.write('|')
        export_CSV.write(post.total_comments)
        export_CSV.write('|')
        export_CSV.write(str(post.comments))
        export_CSV.write('\n')
        export_CSV.write(str(post.post_descrip))
        export_CSV.write('\n\n')
    
    export_CSV.write('HASH COUNT')
    export_CSV.write(str(post.hashes_cnt))
    export_CSV.write('\n')
    export_CSV.close()