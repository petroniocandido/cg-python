import numpy as np
import PIL
from PIL import Image

def putpixel(imagem, x, y, cor=(50,50,50,255)):
  if x >= 0 and x <= imagem.width and y >= 0 and y <= imagem.height:
    imagem.putpixel((int(x),int(y)), cor)
