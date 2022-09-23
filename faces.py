import numpy as np

import cg_python.comum
import cg_python.3d import Ponto5D
from cg_python.poligonos import Poligono

# Uma face é um conjunto de pontos 3D (no mínimo 3) conectados entre si
# A face é basicamente um polígono 2D, formado por pontos 3D projetados
class Face(Poligono):

  def __init__(self, pontos):
    super(Face, self).__init__()
    
    # Lista de Pontos 3D
    self.pontos3d = pontos
    
    x = [p.px for p in self.pontos3d]
    y = [p.py for p in self.pontos3d]
    z = [p.z for p in self.pontos3d]
    self.xmax = np.max(x)
    self.ymax = np.max(y)
    self.zmax = np.max(z)
    self.xmin = np.min(x)
    self.ymin = np.min(y)
    self.zmin = np.min(z)

  def projetar(self, matriz):
    self.pontos = []
    for ponto in self.pontos3d:
      ponto.projetar(matriz)
      self.add(ponto.px, ponto.py)

  def transformar(self, matriz):
    novos = []
    for ponto in self.pontos3d:
      novos.append(matriz.aplicar(ponto))
    return Face(novos)
  
