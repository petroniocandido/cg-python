import cg_python
from cg_python.comum import putpixel

class Spline(object):

  def __init__(self, pontos):
    self.pontos = pontos
    
  def add(self, x, y):
    self.pontos.append((x,y))

  def linear(self, num_iter):
    spline = []
    n = len(self.pontos)
    for i in range(1,n):
    
      x1, y1 = self.pontos[i-1]
      x2, y2 = self.pontos[i]

      for t in np.linspace(0, 1, num_iter):
        
        x = (1-t)*x1 + t*x2
        y = (1-t)*y1 + t*y2

        spline.append((x,y))
    return spline

  def quadratico(self, num_iter):
    n = len(self.pontos)
    spline = []
    for i in range(2,n):
      x1, y1 = self.pontos[i-2]
      x2, y2 = self.pontos[i-1]
      x3, y3 = self.pontos[i]
      
      for t in np.linspace(0,1, num_iter):
        x = ((1-t)**2)*x1 + 2*(1-t)*t*x2 + (t**2)*x3
        y = ((1-t)**2)*y1 + 2*(1-t)*t*y2 + (t**2)*y3
        spline.append((x,y))
    return spline
    
  def cubico(self, num_iter):
    n = len(self.pontos)
    spline = self.cubico_recursivo(self.pontos, n, num_iter)[0]
    return spline

  def cubico_recursivo(self, pontos, grau, num_inter):
    splines = []
    n = len(pontos)
    if grau == 1:
      for i in range(1, n):
        spline = []
        x1, y1 = pontos[i-1]
        x2, y2 = pontos[i]
        for t in np.linspace(0,1,num_inter):
          x = (1-t)*x1 + t*x2
          y = (1-t)*y1 + t*y2
          spline.append((x,y))
        splines.append(spline)
    else:
      splines_n = self.cubico_recursivo(pontos, grau-1, num_inter)
      n = len(splines_n)
      if n == 1:
        return splines_n
      for i in range(1, n):
        spline = []
        spl1 = splines_n[i-1]
        spl2 = splines_n[i]
        for ct, t in enumerate(np.linspace(0,1,num_inter)):
          x1,y1 = spl1[ct]
          x2,y2 = spl2[ct]
          x = (1-t)*x1 + t*x2
          y = (1-t)*y1 + t*y2
          spline.append((x,y))
        splines.append(spline)
    return splines

