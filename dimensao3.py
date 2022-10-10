
import numpy as np


class Ponto3D(object):
  def __init__(self, x, y, z):

    # Coordenados do ponto no espaço tridimensional
    self.x = x
    self.y = y
    self.z = z
    self._norma = None
    
  def transformar(self, matriz):
    self = matriz.aplicar(self)
    
  def produto_escalar(self, ponto):
    return self.x * ponto.x + self.y * ponto.y + self.z * ponto.z
  
  def norma(self):
    if self._norma is None:
      self._norma = np.sqrt(self.x**2 + self.y**2 + self.z**2)
    return self._norma

  def distancia(self, ponto):
    return np.sqrt((self.x - ponto.x)**2 + (self.y - ponto.y)**2 + (self.z - ponto.z)**2)
  
  def produto_vetorial(self, ponto):
    return Ponto3D(self.y * ponto.z - self.z * ponto.y, self.z * ponto.x - self.x * ponto.z, self.x * ponto.y - self.y * ponto.x)
  
  def angulo(self, ponto):
    n1 = self.norma() if self.norma() > 0 else 1
    n2 = ponto.norma() if ponto.norma() > 0 else 1
    return np.arccos(self.produto_escalar(ponto) / (n1 * n2))

  def __str__(self):
    return "({},{},{})".format(self.x, self.y,self.z)


# Coordenadas 3D mais as projeções 2D das coordenadas 3D
class Ponto5D(Ponto3D):
  def __init__(self, x, y, z):
    super(Ponto5D, self).__init__(x,y,z)

    # Projeção do espaço tridimensional no espaço bidimensional
    self.px = 0
    self.py = 0
    
  def converter(ponto : Ponto3D): 
    return Ponto5D(ponto.x, ponto.y, ponto.z)
    
  def projetar(self, matriz):
    self = matriz.aplicar(self)

  def __str__(self):
    return "({},{},{})->({},{})".format(self.x, self.y,self.z,self.px,self.py)
  
  
class MatrizProjecao3D(object):

  # Construtor
  def __init__(self):
    self.matriz = np.eye(4,4)
    self.projecao = 'perspectiva'
    self.parametros = []

  def limpar(self):
    self.matriz = np.eye(4,4)

  def paralela_xy(self):
    self.projecao = 'paralela'
    self.matriz[2,2] = 0
    return self

  def paralela_xz(self):
    self.projecao = 'paralela'
    self.matriz[2,2] = 0
    self.matriz[1,1] = 0
    self.matriz[2,1] = 1
    return self

  def paralela_yz(self):
    self.projecao = 'paralela'
    self.matriz[2,2] = 0
    self.matriz[0,0] = 0
    self.matriz[2,0] = 1
    return self

  def isometrica(self):
    self.projecao = 'isometrica'
    self.matriz[2,2] = 0
    self.matriz[2,0] = -1
    self.matriz[2,1] = -1
    return self

  def cavalier(self):
    self.projecao = 'cavalier'
    self.matriz[2,2] = 0
    self.matriz[2,0] = np.sqrt(2)/2
    self.matriz[2,1] = np.sqrt(2)/2
    return self

  def cabinet(self):
    self.projecao = 'cabinet'
    self.matriz[2,2] = 0
    self.matriz[2,0] = np.sqrt(2)/4
    self.matriz[2,1] = np.sqrt(2)/4
    return self

  def obliqua(self, alfa, beta):
    self.projecao = 'obliqua'
    self.parametros = [alfa, beta]

  def _obliqua_matriz(self, z, alfa, beta):
    matriz = np.eye(4,4)
    L = z / np.tan(beta)
    matriz[0,3] = L * np.cos(alfa)
    matriz[1,3] = L * np.sin(alfa)
    return matriz

  def perspectiva(self, camera):
    self.projecao = 'perspectiva'
    self.parametros = [camera]

  def _perspectiva_matriz(self, z, distancia):
    matriz = np.eye(4,4)
    matriz[0,0] = z/distancia
    matriz[1,1] = z/distancia
    return matriz

  def aplicar(self, ponto):
    z = ponto.z if ponto.z > 0 else 1
    if self.projecao == 'perspectiva':
      camera = self.parametros[0]
      d = camera.distancia(ponto)
      matriz = self._perspectiva_matriz(z, d)
    elif self.projecao == 'obliqua':
      a,b = self.parametros
      matriz = self._obliqua_matriz(z, a, b)
    else:
      matriz = self.matriz
    p = np.array([ponto.x, ponto.y, ponto.z, 1])
    pt = p.dot(matriz)
    ponto.px = pt[0]
    ponto.py = pt[1]
    return ponto

  def str(self):
    return str(self.matriz)

  
class PontoEsferico(object):
  def __init__(self, raio, alfa, beta):
    self.raio = raio #[0,inf]
    self.alfa = alfa #[0, 2pi]
    self.beta = beta #[0, pi]

  def de3D(self, ponto : Ponto3D):
    self.raio = ponto.norma()
    self.alfa = np.arctan(ponto.y / ponto.x)
    self.beta = np.arccos( ponto.z / ponto.norma() )
  
  def para3D(self):
    return Ponto3D(
        self.raio * np.cos(self.alfa) * np.sin(self.beta),
        self.raio * np.sin(self.alfa) * np.sin(self.beta),
        self.raio * np.cos(self.beta),
    )

  def para5D(self):
    return Ponto5D.converter(self.para3D())

  def mover(self, alfa, beta):
    return PontoEsferico(self.raio, self.alfa + alfa, self.beta + beta)  
