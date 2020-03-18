import instaloader
import os
import glob
from jinja2 import Environment, FileSystemLoader

"""Saves instagram saved posts"""


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


def downloadSettings(username):
    setting = instaloader.Instaloader(dirname_pattern='posts', save_metadata=False,
                                      compress_json=False, download_comments=False,
                                      post_metadata_txt_pattern='', filename_pattern='{shortcode}/{shortcode}',
                                      download_geotags=False)
    setting.interactive_login(username)
    return setting


def getProfile(username, setting):
    profile = instaloader.Profile.from_username(setting.context, username)
    return profile


def download_saved(profile, setting):
    for post in profile.get_saved_posts():
        setting.download_post(post, target=None)


def make_dirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def returnTemplate(template):
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


def move_videos():
    PATH = os.path.join('posts', '**', '*.mp4')
    videos = glob.glob(PATH)
    for vid in videos:
        dest = os.path.join('posts', vid.split('\\')[-1])
        os.rename(vid, dest)
        print(f'moving {vid}')


def main():
    make_dirs('posts')
    username = input("\nEnter Instagram username: ")
    setting = downloadSettings(username)
    profile = getProfile(username, setting)
    download_saved(profile, setting)
    for post in profile.get_saved_posts():
        I = Instasaved(post.caption, post.shortcode)
        title, caption, shortcode, url, url_text, image_url = I.title, I.caption, I.shortcode, I.url, I.url_text, I.image_url
        jpg_images = find_images(shortcode)
        mp4_videos = find_videos(shortcode)
        template = returnTemplate('template.html')
        render = jinja_output(title, url, url_text,
                              jpg_images, mp4_videos, caption, template)
        html_file(render, shortcode)
    move_videos()


if __name__ == "__main__":
    main()
