import numpy as np

import cg_python.comum
from cg_python.comum import putpixel

def circunferencia_analitico(tela, xc, yc, r):
  circunferencia = int(2 * np.pi * r)
  for angulo in np.linspace(0, 2*np.pi, circunferencia):
    x = int(xc + r * np.cos(angulo))
    y = int(yc + r * np.sin(angulo))
    tela.putpixel((x,y), (50,50,50,255))
    
def espelhar_pixel_circulo(tela, x, y):
  putpixel(tela, x,y)
  putpixel(tela, x,-y)
  putpixel(tela, -x,y)
  putpixel(tela, -x,-y)
  putpixel(tela, y,x)
  putpixel(tela, -y,x)
  putpixel(tela, y,-x)
  putpixel(tela, -y,-x)

def circunferencia_espelhado(tela, xc, yc, r):
  arco = np.pi/4
  circunferencia = int((np.pi * r)/4)
  for angulo in np.linspace(0, arco, circunferencia):
    px = int(xc + r * np.cos(angulo))
    py = int(yc + r * np.sin(angulo))
    espelhar_pixel_circulo(tela, px, py)
    
def circunferencia_bresenham(tela, xc, yc, r):
  x = 0
  y = r
  d = 3 - 2 * r
  px = xc + x
  py = yc + y
  espelhar_pixel_circulo(tela, px, py)
  while y >= x:
    x += 1
    if d > 0:
      y -= 1
      d = d + 4 * (x - y) + 10
    else:
      d = d + 4 * x + 6;
    px = xc + x
    py = yc + y
    espelhar_pixel_circulo(tela, px, py)
