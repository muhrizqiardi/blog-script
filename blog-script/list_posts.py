from os import listdir
from tabulate import tabulate
import frontmatter

def list_posts(posts_path):
  posts = []
  md_list = listdir(posts_path)
  for md_file in md_list:
    with open(f"{posts_path}\{md_file}") as f:
      post = frontmatter.load(f)
      posts.append([md_file[0:-3], post["title"], post["date"]])
  print()
  print(tabulate(posts, tablefmt='plain', headers=['Slug', 'Title', 'Date']))
