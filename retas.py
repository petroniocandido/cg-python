from cg_python.comum import putpixel

def reta_analitico(imagem, x1, y1, x2, y2, cor=(50,50,50,255)):
  m = (y1 - y2)/(x1-x2)
  b = y1 - m * x1
  for x in range(x1, x2):
    y = int(m * x + b)
    putpixel(imagem, x,y, cor=cor)
    
def reta_dda(imagem, x1, y1, x2, y2, cor=(50,50,50,255)):
  dx = x2 - x1
  dy = y2 - y1
  maior_eixo = max([abs(dx), abs(dy)])
  incx = dx / maior_eixo
  incy = dy / maior_eixo
  x = x1
  y = y1
  for i in range(maior_eixo):
    putpixel(imagem, int(x), int(y), cor=cor)
    x += incx
    y += incy
    
def reta_bresenham(imagem, x1, y1, x2, y2, cor=(50,50,50,255)):
  dx = abs(x2 - x1)
  dy = abs(y2 - y1)
  dy2 = 2 * dy
  di = dy2 - dx
  dydx2 = 2 * (dy - dx)

  if x1 > x2:
    x = x2
    y = y2
    xfim = x1
  else:
    x = x1
    y = y1
    xfim = x2
  
  putpixel(imagem, x, y, cor=cor)

  while x < xfim:
    x += 1

    if di < 0:
      di += dy2
    else:
      y += 1
      di += dydx2
    
    putpixel(imagem, x, y, cor=cor)
    

def reta(tela, x1, y1, x2, y2, cor=(50,50,50,255), metodo = 'dda'):
  if metodo == 'analitico':
    reta_analitico(tela, x1, y1, x2, y2, cor=cor)
  elif metodo == 'dda':
    reta_dda(tela, x1, y1, x2, y2, cor=cor)
  elif metodo == 'bresenham':
    reta_bresenham(tela, x1, y1, x2, y2, cor=cor)
