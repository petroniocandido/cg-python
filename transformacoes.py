import numpy as np
import cg_python.comum
from cg_python.poligonos import Poligono
from cg_python.dimensao3 import Ponto3D

class MatrizTransformacao2D(object):

  # Construtor
  def __init__(self):
    self.matriz = np.eye(3,3)

  def limpar(self):
    self.matriz = np.eye(3,3)

  def transformar(self, tx, ty, ex, ey, r):
    self.translacao(tx, ty)
    self.escala(ex, ey)
    self.rotacao(r)
    return self

  def translacao(self, tx, ty):
    self.matriz[2,0] += tx
    self.matriz[2,1] += ty
    return self

  def escala(self, ex, ey):
    self.matriz[0,0] = ex if self.matriz[0,0] == 1 else ex + self.matriz[0,0]
    self.matriz[1,1] = ey if self.matriz[1,1] == 1 else ey + self.matriz[1,1]
    return self

  def rotacao(self, r):
    self.matriz[0,0] = np.cos(r) if self.matriz[0,0] == 1 else np.cos(r) + self.matriz[0,0]
    self.matriz[0,1] = -np.sin(r) if self.matriz[0,1] == 1 else -np.sin(r) + self.matriz[0,1]
    self.matriz[1,0] = np.sin(r) if self.matriz[1,0] == 1 else np.sin(r) + self.matriz[1,0]
    self.matriz[1,1] = np.cos(r) if self.matriz[1,1] == 1 else np.cos(r) + self.matriz[1,1]
    return self

  def aplicar_poligono(self, poligono : Poligono) -> Poligono:
    sem_tran = np.eye(3,3)
    sem_tran[0:1, 0:1] = self.matriz[0:1,0:1]
    cx1, cy1 = poligono.centro()

    p2 = poligono.transformar(sem_tran)

    cx2, cy2 = p2.centro()

    tx = cx2 - cx1
    ty = cy2 - cy1

    tran = np.eye(3,3)
    tran[2, 0:1] = self.matriz[2, 0:1]
    tran[2,0] -= tx
    tran[2,1] -= ty

    p3 = p2.transformar(tran)

    return p3

  def aplicar(self, x : float, y : float) -> tuple:
    p = np.array([x, y, 1])
    pt = p.dot(self.matriz)
    return (pt[0], pt[1])

  def str(self):
    return str(self.matriz)
  
  
class MatrizTransformacao3D(object):

  # Construtor
  def __init__(self):
    self.matriz = np.eye(4,4)

  def limpar(self):
    self.matriz = np.eye(4,4)

  def transformar(self, tx, ty, tz, ex, ey, ez, rx, ry, rz):
    self.translacao(tx, ty, tz)
    self.escala(ex, ey, ez)
    self.rotacao(rx, ry, rz)
    return self

  def translacao(self, tx, ty, tz):
    self.matriz[3,0] += tx
    self.matriz[3,1] += ty
    self.matriz[3,2] += tz
    return self

  def escala(self, ex, ey, ez):
    self.matriz[0,0] = ex if self.matriz[0,0] == 1 else ex + self.matriz[0,0]
    self.matriz[1,1] = ey if self.matriz[1,1] == 1 else ey + self.matriz[1,1]
    self.matriz[2,2] = ex if self.matriz[2,2] == 1 else ez + self.matriz[2,2]
    return self

  def rotacao(self, rx, ry, rz):
    self.matriz[1,1] = np.cos(rx) if self.matriz[1,1] == 1 else np.cos(rx) + self.matriz[1,1]
    self.matriz[1,2] -= np.sin(rx)
    self.matriz[2,1] += np.sin(rx)
    self.matriz[2,2] = np.cos(rx) if self.matriz[2,2] == 1 else np.cos(rx) + self.matriz[2,2]

    self.matriz[0,0] = np.cos(ry) if self.matriz[0,0] == 1 else np.cos(ry) + self.matriz[0,0]
    self.matriz[0,2] += np.sin(ry)
    self.matriz[2,0] -= np.sin(ry)
    self.matriz[2,2] = np.cos(ry) if self.matriz[2,2] == 1 else np.cos(ry) + self.matriz[2,2]

    self.matriz[0,0] = np.cos(rz) if self.matriz[0,0] == 1 else np.cos(rz) + self.matriz[0,0]
    self.matriz[0,1] += -np.sin(rz)
    self.matriz[1,0] += np.sin(rz)
    self.matriz[1,1] = np.cos(rz) if self.matriz[1,1] == 1 else np.cos(rz) + self.matriz[1,1]

    return self


  def aplicar(self, ponto : Ponto3D):
    p = np.array([ponto.x, ponto.y, ponto.z, 1])
    pt = p.dot(self.matriz)
    return Ponto3D(pt[0], pt[1], pt[2])

  def str(self):
    return str(self.matriz)
