from json.decoder import JSONDecodeError
from slugify import slugify
from getpass import getuser
from generate_cover import generate_cover
from config_writer import config_writer
from open_external import open_external
from list_posts import list_posts
import os
import sys
import json
import argparse
import datetime
import subprocess

config = {}

### Functions definition
# Format colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

# Initialize argparse
def init_argparse():
  parser = argparse.ArgumentParser(
      description=f"Create a blog easily with {bcolors.OKCYAN}git{bcolors.ENDC} and {bcolors.OKCYAN}markdown{bcolors.ENDC}."
  )

  parser.add_argument('--about', action="store_true", help="About the program")
  parser.add_argument('--info', action="store_true", help="Info about the blog")
  parser.add_argument('--list', action="store_true", help="List all the post")
  parser.add_argument('--publish', action="store_true", help="Commit and push posts to the directory")

  # For creating a post
  parser.add_argument('--create', action="store_true", help="Create a post")
  parser.add_argument('-t', '--title', type=str, help="Set a post's  title")
  parser.add_argument('-e', '--excerpt', type=str, help="Set a post's excerpt")
  parser.add_argument('-a', '--author', type=str, help="Set a post's author")
  parser.add_argument('-d', '--date', type=str, help="Set a post's date")
  parser.add_argument('-c', '--cover', type=str, help="Set a post's cover image")
  parser.add_argument('-gc', '--generate-cover', action="store_true", help="Generate a post's cover image")

  # For editing a post
  parser.add_argument('--edit', action="store_true", help="Edit a post based on provided slug")
  parser.add_argument('-s', '--slug', type=str, help="Slug of a post")


  args = parser.parse_args()
  return args

def create_post(parent_path, posts_path, assets_path, post_field):
  md_template = open('default.md').read()
  post_slug = slugify(post_field["title"])
  new_post_absolute_path = '{}{}/{}.md'.format(parent_path, posts_path, post_slug)
  new_assets_absolute_path = parent_path + assets_path + "/" + post_slug

  try: 
    # create new md file
    with open(new_post_absolute_path, 'w+') as new_post:
      # write the new template based of the 
      new_post.write(md_template.format(**post_field))
    
    os.mkdir(new_assets_absolute_path) # create new path on assets folder
    if args.generate_cover:
      """ 
      geopatterns by @bryanveloso
      """
      print(f"{bcolors.OKGREEN}🖼 Generating Cover Image...{bcolors.ENDC}")
      try:
        generate_cover(args.title, new_assets_absolute_path, "Cover Image")
      except Exception as e:
        print(f'{bcolors.FAIL}⚠ An error happened while generating image: {e}{bcolors.ENDC}')

    print(f"{bcolors.OKGREEN}✔ Creating post succeed{bcolors.ENDC}\n")
    print(f"📝 Location of markdown file: {bcolors.OKCYAN}\"{os.path.normpath(new_post_absolute_path)}\"{bcolors.ENDC}")
    print(f"📝 Location of assets folder: {bcolors.OKCYAN}\"{os.path.normpath(new_assets_absolute_path)}\"{bcolors.ENDC}")

    print(f"{bcolors.OKGREEN}🏃‍♀️ Opening in external editor...{bcolors.ENDC}")
    open_external(new_post_absolute_path)

  except FileExistsError: 
    print(f'{bcolors.FAIL}⚠ Post already existed{bcolors.ENDC}')
  
  except IndexError:
    print(f'{bcolors.FAIL}⚠ Markdown template isn\'t properly formatted{bcolors.ENDC}')

  except Exception as e: 
    print(f'{bcolors.FAIL}⚠ An error happened: {e}{bcolors.ENDC}')


### Main function
def main():
  if args.about:
    print(f"\n👋 Welcome to {bcolors.BOLD}blog-script{bcolors.ENDC}. Create a blog easily with {bcolors.OKCYAN}git{bcolors.ENDC} and {bcolors.OKCYAN}markdown{bcolors.ENDC}.")
    print(f"🧑 Made by {bcolors.WARNING}Muhammad Rizqi Ardiansyah{bcolors.ENDC}")
  config = {}

  # Loads Config JSON, if doesn't exist create a new one
  try:
    file = open('config.json', 'r+') 
    # Try reading config.json
    try: 
      config = json.load(file)

    # If error, copy the current config.json's content to the config.json.old
    except JSONDecodeError:
      print(f"{bcolors.FAIL}⚠ Error reading config file. Creating a new one.{bcolors.ENDC}")

      with open('config.json.old', 'w+') as old_file:
        old_file.write(file.read())
      
      config = config_writer()
      json.dump(config, file)
  except FileNotFoundError: 
    print(f"{bcolors.FAIL}⚠ Config file missing. Creating a new one.{bcolors.ENDC}")
    config = config_writer()
    json.dump(config, open('config.json', 'x'))
  except Exception as e: 
    print(f"{bcolors.FAIL}⚠ An error happened: {e}{bcolors.ENDC}")

  if args.publish: 
    print(f"{bcolors.OKGREEN}🐙 Creating a git commit...{bcolors.ENDC}")
    try:
      os.chdir(config["parent-path"])
      os.system('git checkout blog --no-guess')
      os.system('git add -A')
      os.system('git commit -m "published post(s)"')
      
      print(f"{bcolors.OKGREEN}☁ Pushing to remote...{bcolors.ENDC}")
      os.system('git push')

    except Exception as e:
      print(f"{bcolors.FAIL}⚠ An error happened while publishing: {e}{bcolors.ENDC}")


  if args.info:
    print(
    f""" 
    \t{bcolors.BOLD}Blog: {bcolors.ENDC}{config["blog-title"]}
    \t{bcolors.BOLD}By: {bcolors.ENDC}{config["blog-author"]}

    \t⚙ Config directory: \t"{os.path.realpath(open('config.json').name)}"
    \t📂 Parent directory: \t"{config["parent-path"]}"
    \t📄 Posts directory: \t"{config["parent-path"]}{config["posts-path"]}"
    \t🖼 Assets directory: \t"{config["parent-path"]}{config["assets-path"]}"
    """)

  if args.list:
    print(f"✍ Listing all posts:")
    list_posts(f"{config['parent-path']}{config['posts-path']}")

  if args.edit and args.slug:
    post_path = f"{config['parent-path']}{config['posts-path']}/{args.slug}.md"
    print(f"{bcolors.OKGREEN}🏃 Opening in {args.slug}.md external editor...{bcolors.ENDC}")

    open_external(post_path)

  if args.create and args.title: 

    print(f"✍ Creating {args.title}") 
    post_field = {
      "title": args.title,
      "slug": slugify(args.title),
      "author": args.author if args.author else config["blog-author"],
      "excerpt": args.excerpt if args.excerpt else "",
      "date": args.date if args.date else datetime.datetime.now().isoformat(),
      "cover": f"{os.path.join(config['parent-path'], config['assets-path'])}\\Cover Image.png" if args.generate_cover else "",
    }
    create_post(config["parent-path"], config["posts-path"], config["assets-path"], post_field)
  print()

args = init_argparse()

if __name__ == "__main__":
  main()
