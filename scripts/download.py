import instaloader
import os

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

    for file in files:
        if file.endswith('.jpg'):
            jpg_count += 1
            new_name = f'nails_by_dunja_post_{jpg_count}.jpg'
            img = f'<img src="./posts/{new_name}" />'
            images.append(img)
            os.rename(file, new_name)
            print(f'Renamed {file} to {new_name}')
        else:
            os.remove(file)
            print(f'Removed {file}')

    print(f'Process completed. Renamed {jpg_count} .jpg files.')

def replace_and_write(input_file, output_file, text):
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