import os
import instaloader

"""Saves Instagram post based on given url"""

L = instaloader.Instaloader(dirname_pattern='posts', save_metadata=False, 
                            compress_json=False, download_comments=False, 
                            post_metadata_txt_pattern='', filename_pattern='{shortcode}/{shortcode}',
                            download_geotags=False)

USER = input("\nEnter Instagram username: ")
L.interactive_login(USER) 

shortcode = 'BvZ20xLBcj2p9VtiGkr8d4gOSNjV48737E4vGU0'

def save_post():

    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=None)

def make_dirs():

    '''makes html directory'''

    if not os.path.exists("posts"):
        os.makedirs("posts")

def main():
    save_post()
    # move_videos()

if __name__ == "__main__":
    main()