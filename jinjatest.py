from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('image.html')

imageurl = ['http://test1.com', 'http://test2.com']

output = template.render(url = 'http://imgur.com', title = 'this is a test title', 
                        imageurl = imageurl, caption = caption, video = video,
                        video_still = video_still)
print(output)