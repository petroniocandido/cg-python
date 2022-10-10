from cg_python.dimensao3 import Ponto3D


class FonteLuz(object):
  def __init__(self, ponto : Ponto3D, intensidade):
    self.posicao = ponto
    self.intensidade = intensidade
