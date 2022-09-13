import numpy as np

class MatrizTransformacao2D(object):

  # Construtor
  def __init__(self):
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
    self.matriz[0,0] *= ex
    self.matriz[1,1] *= ey
    return self

  def rotacao(self, r):
    self.matriz[0,0] *= np.cos(r)
    self.matriz[0,1] *= -np.sin(r)
    self.matriz[1,0] *= np.sin(r)
    self.matriz[1,1] *= np.cos(r)
    return self

  def aplicar(self, x, y):
    p = np.array([x, y, 1])
    pt = p.dot(self.matriz)
    return (pt[0], pt[1])

  def str(self):
    return str(self.matriz)
