import numpy as np

import cg_python.comum
import cg_python.dimensao3 import Ponto3D, Ponto5D
from cg_python.poligonos import Poligono

# Uma face é um conjunto de pontos 3D (no mínimo 3) conectados entre si
# A face é basicamente um polígono 2D, formado por pontos 3D projetados

class Face(Poligono):

  def __init__(self, pontos):
    super(Face, self).__init__()
    
    self.visivel = True

    self.normal = None
    
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
      novos.append(Ponto5D.converter(matriz.aplicar(ponto)))
    return Face(novos)

  def vetor_normal(self):
    if self.normal is None:
      p1 = self.pontos3d[0]
      p2 = self.pontos3d[1]
      p3 = self.pontos3d[2]

      a = Ponto3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
      b = Ponto3D(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)

      self.normal = a.produto_vetorial(b)

    return self.normal


  def vetor_normal_unitario(self):
    norma = self.vetor_normal().norma()
    self.normal = Ponto3D(self.normal.x/norma, self.normal.y/norma, self.normal.z/norma)

    return self.normal

  def __str__(self):
    tmp = "Face ["
    for ponto in self.pontos3d:
      tmp += str(ponto) + " "
    tmp += "]"
    return tmp

  
  
  
