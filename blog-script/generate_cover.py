from PIL import Image
from svglib.svglib import svg2rlg
from geopatterns import GeoPattern
from reportlab.graphics import renderPM
import io
import os
import math
import base64
import random
  

def generate_cover(text, path, filename):
  pattern = GeoPattern(text, random.choices(['hexagons', 'overlapping_circles', 'overlapping_rings',
                                             'plaid', 'plus_signs', 'rings', 'sinewaves', 'squares', 'triangles', 'xes'])[0])
  renderPM.drawToFile(svg2rlg(io.StringIO(base64.decodebytes(
      pattern.base64_string).decode('utf-8'))), '.pattern_temp.png', fmt='PNG')

  pattern = Image.open(".pattern_temp.png").convert("RGBA")
  bg = Image.new(mode="RGB", size=(1200, 628), color=(math.ceil(random.random(
  )*255), math.ceil(random.random()*255), math.ceil(random.random()*255)))

  for x in range(math.ceil(bg.size[0]/pattern.size[0])):
    for y in range(math.ceil(bg.size[1]/pattern.size[1])):
      bg.paste(pattern, (pattern.size[0]*x, pattern.size[1]*y))
  os.remove("./.pattern_temp.png")
  bg.save(f'{os.path.normpath(os.path.join(path, filename))}.png')
