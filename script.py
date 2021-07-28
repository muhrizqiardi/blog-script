from json.decoder import JSONDecodeError
import sys
import argparse
import json

# Command Line Arguments
new_post_parser = argparse.ArgumentParser(description="➕ Create a new post directly")
new_post_parser.add_argument(
  'post_title',
  metavar="post_title",
  type=str,
  help="Title of the new post"
)
args = new_post_parser.parse_args()
print(args.post_title)

# Functions
def input_with_default(default_string, arg = ""):
  user_input = input()
  return user_input if len(user_input) > 0 else default_string

def config_writer():
  config = {}

  print("Where is your main blog folder located? (absolute path):")
  config["parent-path"] = input()

  print("Where is the posts located, relative to main blog folder? (/_posts):")
  config["posts-path"] = input_with_default("/_posts")

  print("Where is the assets folder (for images and such) located, relative to main blog folder? (/public/assets/blog):")
  config["assets-path"] = input_with_default("/public/assets/blog")

  return config

print("👋 Welcome to blog-script. Create a blog easily with git and markdown.\nMade by Muhammad Rizqi Ardiansyah")
config = {}

# Loads Config JSON, if doesn't exist create a new one
with open('config.json', 'w+') as file:

  # Try reading config.json
  try: 
    config = json.load(file)

  # If error, copy the current config.json's content to the config.json.old
  except JSONDecodeError:
    print("Error reading config file. Creating a new one.")

    with open('config.json.old', 'w+') as old_file:
      file.write(old_file.read())
    
    config = config_writer()
    json.dump(config, file)

print("Parent directory: " + config["parent-path"])
print("Posts directory: " + config["posts-path"])
print("Assets directory: " + config["assets-path"])

