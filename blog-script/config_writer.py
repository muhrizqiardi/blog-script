# Create a prompt to ask a directories for config
def config_writer():
  config = {}

  print("What is your blog's name?:")
  config["blog-title"] = input()

  print(f"Who is the author? ({getuser()}): ")
  config["blog-author"] = input() or getuser()

  print("Where is your main blog folder located? (absolute path):")
  config["parent-path"] = input()

  print("Where is the posts located, relative to main blog folder? (/_posts):")
  config["posts-path"] = input() or "/_posts"

  print("Where is the assets folder (for images and such) located, relative to main blog folder? (/public/assets/blog):")
  config["assets-path"] = input() or "/public/assets/blog"

  return config
