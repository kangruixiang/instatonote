import glob
import os
from jinja2 import Environment, FileSystemLoader



path = os.path.join('**', 'Bf1fLx-gCRE', '*.jpg')
image_list = glob.glob(path)
jpg_images = []
for img in image_list:
    imgurl = img.split('\\')[1:]
    imgurl = '/'.join(imgurl)
    jpg_images.append(imgurl)

path = os.path.join('**', 'Bf1fLx-gCRE', '*.mp4')
vid_list = glob.glob(path)
mp4_videos = []
for vid in vid_list:
    vidurl = vid.split('\\')[1:]
    vidurl = '/'.join(vidurl)
    mp4_videos.append(vidurl)


PATH = "./html" # path for html files
IPATH = "./posts/**/*" # path for media files
MEDIAPATH = "/Users/Kang/Library/Application Support/Anki2/User 1/collection.media/" # path for anki media folder


videos = glob.glob(f"{IPATH}.mp4")
for vid in videos:
    dest = MEDIAPATH + image.split('/')[-1]
    os.rename(image, dest)