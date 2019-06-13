# instatonote

Downloads your instagram saved posts and format them as such to be imported into Evernote. This uses the "import folders" function in Evernote and thus only works for Windows as of now. Mac version of Evernote does not have "import functions."

# instasave

Saves Instagram posts based on given url

## Requirements

Install required modules via `pip install -r requirements.txt`

## Usage

### Instanote

Run instatonote.py, enter your username and password. The script will save the posts under "posts" folder. Each instagram saved posts will be saved as its short url code html file with its corresponding image/video folder. Once that's finished. Point "import folders" in evernote to the "posts" folder, and you should get this for each post:

![](sample.png)

Caveat: Evernote does not seem to import videos when I tried this. Right now I can only add the video files manually by dragging and dropping into each evernote note.

### Instasave

Replace shortcode with shortcode of the URL. Then run the script