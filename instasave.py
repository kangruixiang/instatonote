import os
import instaloader

"""Saves Instagram post based on given url"""

L = instaloader.Instaloader(dirname_pattern='posts', save_metadata=False, 
                            compress_json=False, download_comments=False, 
                            post_metadata_txt_pattern='', filename_pattern='{shortcode}/{shortcode}',
                            download_geotags=False)

shortcode = 'BLmz17fAJam'

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