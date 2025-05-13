import os
import base64
import mimetypes
import instaloader
import glob
import shutil
from jinja2 import Environment, FileSystemLoader

"""Saves Instagram post based on given url"""

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

L = instaloader.Instaloader(dirname_pattern='posts', save_metadata=False, 
                            compress_json=False, download_comments=False, 
                            post_metadata_txt_pattern='', filename_pattern='{shortcode}/{shortcode}',
                            download_geotags=False)

# USER = input("\nEnter Instagram username: ")
# L.interactive_login(USER) 

postURL = input('\nEnter Post URL: ')

shortcode = 'placeholder'

def make_dirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def find_images(shortcode):
    '''finds images files in directory and return string of base64 data'''
    path = os.path.join('**', shortcode, '*.jpg')
    image_list = glob.glob(path)
    jpg_images = []
    for img_path in image_list:
        # imgurl = img.split('\\')[1:]
        # imgurl = '/'.join(imgurl)
        # jpg_images.append(imgurl)
        img_in_64 = convert_to_base64(img_path)
        jpg_images.append(img_in_64)
    
    return jpg_images


def find_videos(shortcode):
    path = os.path.join('**', shortcode, '*.mp4')
    vid_list = glob.glob(path)
    mp4_videos = []
    for vid_path in vid_list:
        # vidurl = vid.split('\\')[1:]
        # vidurl = '/'.join(vidurl)
        vid_in_64 = convert_to_base64(vid_path)
        mp4_videos.append(vid_in_64)

    return mp4_videos

def return_template(template):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('template.html')
    return template

def jinja_output(title, url, url_text, jpg_images, mp4_videos, caption, template):
    render = template.render(title=title, url=url, url_text=url_text,
                             images=jpg_images, videos=mp4_videos, caption=caption)
    return render

def html_file(render, shortcode):
    saved_html = os.path.join('posts', f'{shortcode}.html')
    with open(saved_html, 'w', encoding='utf-8') as f:
        f.write(render)
    print(f'Saving {shortcode}')

def save_post(shortcode):
    '''downloads the post images and videos'''
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=None)
    return post

def convert_to_base64(file_path):
    file_type, _ = mimetypes.guess_type(file_path)

    if file_type is None:
        raise ValueError("Could not determine MIME type")
    
    with open(file_path, "rb") as media_file:
        data = base64.b64encode(media_file.read()).decode('utf-8')

    return f"data:{file_type};base64,{data}"
    
def cleanup(shortcode):
    media_path = os.path.join('posts', shortcode)
    print(media_path)
    shutil.rmtree(media_path)


def main():
    make_dirs('posts')
    post = save_post(postURL)
    I = Instasaved(post.caption, post.shortcode)
    title, caption, shortcode, url, url_text = I.title, I.caption, I.shortcode, I.url, I.url_text
    jpg_images = find_images(shortcode)
    mp4_videos = find_videos(shortcode)
    template = return_template('template.html')
    render = jinja_output(title, url, url_text, jpg_images, mp4_videos, caption, template)
    html_file(render, shortcode)
    cleanup(shortcode)

if __name__ == "__main__":
    main()
