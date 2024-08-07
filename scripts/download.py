import instaloader
import os
from PIL import Image

images = []
posts_file_path = 'posts'

def download_all(folder_path):
    # Initialize instaloader
    loader = instaloader.Instaloader()

    # Login (optional)
    # loader.interactive_login("your_username")

    # Replace 'account_name' with the Instagram account you want to scrape
    profile = instaloader.Profile.from_username(loader.context, 'nails.by_dunja')

    # Create a directory to store downloaded content
    os.makedirs(folder_path, exist_ok=True)

    # Iterate over the posts
    for post in profile.get_posts():
        loader.download_post(post, target=folder_path)


def clean_and_rename(folder_path):
    # Change directory to the specified folder path
    os.chdir(folder_path)

    # Get a list of all files in the folder
    files = os.listdir()
    print(files)
    # Initialize a counter for renaming jpg files
    jpg_count = 0
    
    files = sorted(files, reverse=True)
    for file in files:
        if file.endswith('.jpg'):
            jpg_count += 1
            new_name = f'nails_by_dunja_post_{jpg_count}.webp'
            
            os.rename(file, new_name)
       
            img =  Image.open(new_name)
            width, height = img.size
            new_width = 400
            new_height = int(height * new_width / width)
            img_resized = img.resize((new_width, new_height), Image.ADAPTIVE)
            img_resized.save(new_name, "webp")

        
            img = f'<img src="./posts/{new_name}" />'
            images.append(img)
            print(f'Renamed {file} to {new_name}')
        # elif file.endswith('.mp4'):
        #     clip = VideoFileClip(file)

        #     # Calculate new dimensions while maintaining aspect ratio
        #     new_height = 800
        #     ratio = new_height / clip.size[1]
        #     new_width = int(clip.size[0] * ratio)

        #     # Resize video
        #     resized_clip = clip.resize(height=new_height, width=new_width)
            
        #     # Remove audio
        #     final_clip = resized_clip.without_audio()

        #     # Export the final clip as MP4 (or any other desired format)
        #     jpg_count += 1
        #     output_path_mp4 = f'nails_by_dunja_post_{jpg_count}.mp4'
        #     output_path_ogg = f'nails_by_dunja_post_{jpg_count}.ogg'
        #     output_path_webm = f'nails_by_dunja_post_{jpg_count}.webm'
            
        #     video = f''' <video autoplay muted loop playsinline>
        #         <source src="./posts/{output_path_webm}" type="video/webm">
        #         <source src="./posts/{output_path_ogg}" type="video/ogg">
        #         <source src="./posts/{output_path_mp4}" type="video/mp4">
        #         Your browser does not support HTML5 video.
        #         </video>'''
        #     images.append(video)
        #     final_clip.write_videofile(output_path_mp4, codec='libx264', audio_codec='aac')
        #     final_clip.write_videofile(output_path_ogg, codec='libtheora', audio_codec='libvorbis')
        #     final_clip.write_videofile(output_path_webm, codec='libvpx', audio_codec='libvorbis')
        #     os.remove(file)
        else :
            os.remove(file)
            print(f'Removed {file}')

    print(f'Process completed. Renamed {jpg_count} .jpg files.')

checked = []
def load_all_files(folder_path):
    os.chdir(folder_path)

    files = os.listdir()
    files = sorted(files)
    for file in files:
        if file.endswith('.webp'):
            img = f'<img src="./posts/{file}" />'
            images.append(img)
        elif file.endswith('.mp4'):
            check = os.path.splitext(file)[0]
            if check in checked:
                continue

            checked.append(check)
            x = file.replace(".mp4", ".webm")
            y = file.replace(".mp4", ".ogg")
            video = f''' <video autoplay muted loop playsinline>
            <source src="./posts/{x}" type="video/webm">
            <source src="./posts/{y}" type="video/ogg">
            <source src="./posts/{file}" type="video/mp4">
            Your browser does not support HTML5 video.
            </video>'''
            images.append(video)
        elif file.endswith('.ogg'):
            check = os.path.splitext(file)[0]
            if check in checked:
                continue

            checked.append(check)
            x = file.replace(".ogg", ".webm")
            y = file.replace(".ogg", ".mp4")
            video = f''' <video autoplay muted loop playsinline>
            <source src="./posts/{x}" type="video/webm">
            <source src="./posts/{file}" type="video/ogg">
            <source src="./posts/{y}" type="video/mp4">
            Your browser does not support HTML5 video.
            </video>'''
            images.append(video)
        elif file.endswith('.webm'):
            check = os.path.splitext(file)[0]
            if check in checked:
                continue

            checked.append(check)
            x = file.replace(".webm", ".ogg")
            y = file.replace(".webm", ".mp4")
            video = f''' <video autoplay muted loop playsinline>
            <source src="./posts/{file}" type="video/webm">
            <source src="./posts/{x}" type="video/ogg">
            <source src="./posts/{y}" type="video/mp4">
            Your browser does not support HTML5 video.
            </video>'''
            images.append(video)
        
    os.chdir('..')

def replace_and_write(input_file, output_file, text):
    if len(images) == 0:
        load_all_files("posts")
        text = "".join(images)


    print(os.getcwd())
    # Read the entire content of the input file into a string
    with open(input_file, 'r') as f:
        file_content = f.read()

    # Replace '#IMAGES' with 'Some other text'
    modified_content = file_content.replace('#IMAGES', text)

    # Write the modified content to the output file
    with open(output_file, 'w') as f:
        f.write(modified_content)

    print(f"Created {output_file}")

download_all(posts_file_path)
clean_and_rename(posts_file_path)
os.chdir("..") 
replace_and_write("galerija_template.html", "galerija.html", "".join(images))