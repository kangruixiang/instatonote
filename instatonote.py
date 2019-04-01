import instaloader
import os
import glob
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('template.html')

L = instaloader.Instaloader(dirname_pattern='posts', save_metadata=False, 
                            compress_json=False, download_comments=False, 
                            post_metadata_txt_pattern='', filename_pattern='{shortcode}/{shortcode}')
L.load_session_from_file("kangruixiang")
profile = instaloader.Profile.from_username(L.context, "kangruixiang")

class Instasaved:

    def __init__(self, caption, shortcode):
        try:
            self.title = caption[:50]
            self.caption = caption
        except:
            self.title = shortcode
            self.caption = ''
        self.shortcode = shortcode
        self.url = f'https://instagram.com/p/{shortcode}'
        self.url_text = self.url.split("/")[2]
        self.image_url = f'{shortcode}.jpg'

def make_dirs():

    '''makes html directory'''

    if not os.path.exists("posts"):
        os.makedirs("posts")

def find_images(shortcode):
    
    '''finds images files in directory'''

    path = os.path.join('**', shortcode, '*.jpg')
    image_list = glob.glob(path)
    jpg_images = []
    for img in image_list:
        imgurl = img.split('\\')[1:]
        imgurl = '/'.join(imgurl)
        jpg_images.append(imgurl)
    return jpg_images

def find_videos(shortcode):

    path = os.path.join('**', shortcode, '*.mp4')
    vid_list = glob.glob(path)
    mp4_videos = []
    for vid in vid_list:
        vidurl = vid.split('\\')[1:]
        vidurl = '/'.join(vidurl)
        mp4_videos.append(vidurl)
    return mp4_videos

def jinja_output(title, url, url_text, jpg_images, mp4_videos, caption):
    render = template.render(title = title, url = url, url_text = url_text, images = jpg_images, videos = mp4_videos, caption = caption)
    return render 

def html_file(render, shortcode):
    with open(f'posts/{shortcode}.html', 'w', encoding='utf-8') as f:
        f.write(render)
    print(f'saving {shortcode}.html')

def download_saved():
    for post in profile.get_saved_posts():
        L.download_post(post, target=None)

def move_videos():
    PATH = os.path.join('posts', '**', '*.mp4')
    print(PATH)
    videos = glob.glob(PATH)
    print(videos)
    for vid in videos:
        dest = os.path.join('posts', vid.split('\\')[-1])
        os.rename(vid, dest)
        print(f'moving {vid}')

def main():
    make_dirs()
    download_saved()
    for post in profile.get_saved_posts():
        I = Instasaved(post.caption, post.shortcode)
        title, caption, shortcode, url, url_text, image_url = I.title, I.caption, I.shortcode, I.url, I.url_text, I.image_url
        jpg_images = find_images(shortcode)
        mp4_videos = find_videos(shortcode)
        render = jinja_output(title, url, url_text, jpg_images, mp4_videos, caption)
        html_file(render, shortcode)
    move_videos()

if __name__ == "__main__":
    main()