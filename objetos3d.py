import numpy as np
from cg_python.dimensao3 import Ponto3D, Ponto5D, PontoEsferico
from cg_python.faces import Face
from cg_python.luz import FonteLuz

# Uma Malha (Mesh) é um conjunto de faces conectadas
class Mesh(object):
  def __init__(self, faces, cor):
    self.faces = faces
    self.cor = cor

    self.xmax = np.max([f.xmax for f in self.faces])
    self.ymax = np.max([f.ymax for f in self.faces])
    self.zmax = np.max([f.zmax for f in self.faces])
    self.xmin = np.min([f.xmin for f in self.faces])
    self.ymin = np.min([f.ymin for f in self.faces])
    self.zmin = np.min([f.zmin for f in self.faces])

  def add(self, face):
    self.faces.append(face)
    self.xmax = np.max([self.xmax, face.xmax])
    self.ymax = np.max([self.xmax, face.xmax])
    self.zmax = np.max([self.xmax, face.xmax])
    self.xmin = np.min([self.xmin, face.xmin])
    self.ymin = np.min([self.xmin, face.xmin])
    self.zmin = np.min([self.xmin, face.xmin])

  def centro(self):
    return Ponto5D(self.xmin + (self.xmax - self.xmin)/2, 
                   self.ymin + (self.ymax - self.ymin)/2, 
                   self.zmin + (self.zmax - self.zmin)/2, 
                   )

  def transformar(self, matriz):
    novas = []
    for face in self.faces:
      novas.append(face.transformar(matriz))
    return Mesh(novas, self.cor)

  def wireframe(self, tela, matriz_projecao):
    for face in self.faces:
      face.projetar(matriz_projecao)
      face.boundary(tela)

  def backface_culling(self, camera):
    for face in self.faces:
      ang_camera = face.vetor_normal_unitario().angulo(camera)
      face.visivel = ang_camera >= 0   

  def sombrear_global(self, tela, camera, matriz_projecao, luz):
    draw = ImageDraw.Draw(tela)  
    
    iluminacao_global = (int(self.cor[0] * luz.intensidade), 
                         int(self.cor[1] * luz.intensidade),
                         int(self.cor[2] * luz.intensidade),
                         255)
    
    self.backface_culling(camera)
    
    for face in sorted(self.faces, key=lambda f: (f.zmax, f.zmin), reverse=True):

      if face.visivel:

        face.projetar(matriz_projecao)

        draw.polygon(face.pontos, fill = iluminacao_global, outline = iluminacao_global) 


  def sombrear_flat(self, tela, camera, matriz_projecao, luz):
    draw = ImageDraw.Draw(tela)  
    
    self.backface_culling(camera)
    
    for face in sorted(self.faces, key=lambda f: (f.zmax, f.zmin), reverse=True):

      if face.visivel:

        face.projetar(matriz_projecao)

        ang_luz = face.vetor_normal_unitario().angulo(luz.posicao)

        if not np.isnan(ang_luz):

          iluminacao_flat = (int(self.cor[0] * np.abs(np.cos(ang_luz) * luz.intensidade)), 
                          int(self.cor[1] * np.abs(np.cos(ang_luz) * luz.intensidade)),
                          int(self.cor[2] * np.abs(np.cos(ang_luz) * luz.intensidade)),
                          255)

          draw.polygon(face.pontos, fill = iluminacao_flat, outline = iluminacao_flat) 

  def sombrear_phong(self, tela, camera, matriz_projecao, luz):
    draw = ImageDraw.Draw(tela)  
    
    self.backface_culling(camera)
    
    for face in sorted(self.faces, key=lambda f: (f.zmax, f.zmin), reverse=True):

      if face.visivel:

        face.projetar(matriz_projecao)

        ang_luzA = face.pontos3d[0].angulo(luz.posicao)
        ang_luzA = ang_luzA if not np.isnan(ang_luzA) else 0
        
        iluminacao_pontoA = (self.cor[0] * np.abs(np.cos(ang_luzA) * luz.intensidade), 
                          self.cor[1] * np.abs(np.cos(ang_luzA) * luz.intensidade),
                          self.cor[2] * np.abs(np.cos(ang_luzA) * luz.intensidade),
                          255)
        #print(iluminacao_pontoA)
        
        ang_luzB = face.pontos3d[1].angulo(luz.posicao)
        ang_luzB = ang_luzB if not np.isnan(ang_luzB) else 0
        iluminacao_pontoB = (self.cor[0] * np.abs(np.cos(ang_luzB) * luz.intensidade), 
                          self.cor[1] * np.abs(np.cos(ang_luzB) * luz.intensidade),
                          self.cor[2] * np.abs(np.cos(ang_luzB) * luz.intensidade),
                          255)
        #print(iluminacao_pontoB)

        ang_luzC = face.pontos3d[2].angulo(luz.posicao)
        ang_luzC = ang_luzC if not np.isnan(ang_luzC) else 0
        iluminacao_pontoC = (self.cor[0] * np.abs(np.cos(ang_luzC) * luz.intensidade), 
                          self.cor[1] * np.abs(np.cos(ang_luzC) * luz.intensidade),
                          self.cor[2] * np.abs(np.cos(ang_luzC) * luz.intensidade),
                          255)
        #print(iluminacao_pontoC)
        
        rx = int(face.xmax - face.xmin)
        ry = int(face.ymax - face.ymin)
        #nxy = max(rx,ry)
        #print(nxy)
        degrade = np.zeros((rx, ry, 4))
        for x in range(rx):
          for y in range(ry):
            dA = np.sqrt((face.pontos3d[0].px - rx - x)**2 + (face.pontos3d[0].py - ry - y)**2) #/ nxy
            dB = np.sqrt((face.pontos3d[1].px - rx - x)**2 + (face.pontos3d[1].py - ry - y)**2) #/ nxy
            dC = np.sqrt((face.pontos3d[2].px - rx - x)**2 + (face.pontos3d[2].py - ry - y)**2) #/ nxy

            norma = dA + dB + dC

            degrade[x,y,0] = int((iluminacao_pontoA[0] * dA +iluminacao_pontoB[0] * dB +iluminacao_pontoC[0] * dC))/norma
            degrade[x,y,1] = int((iluminacao_pontoA[1] * dA +iluminacao_pontoB[1] * dB +iluminacao_pontoC[1] * dC))/norma
            degrade[x,y,2] = int((iluminacao_pontoA[2] * dA +iluminacao_pontoB[2] * dB +iluminacao_pontoC[2] * dC))/norma
            degrade[x,y,3] = 255


        draw.polygon(face.pontos, fill = (255, 255, 255, 255), outline = (255, 255, 255, 255))

        for x in range(int(face.xmin), int(face.xmax)):
          for y in range(int(face.ymin), int(face.ymax)):
            if x >= 0 and x < tela.width and y >= 0 and y < tela.height:
              if tela.getpixel((x,y)) == (255, 255, 255, 255) :
                cor = tuple([int(degrade[x-rx, y-ry, i]) for i in range(4)])
                tela.putpixel((x, y), cor)
      
      
class Cubo(Mesh):
  def __init__(self, x, y, z, altura, largura, profundidade, cor):
    
    p1 = Ponto5D(x, y, z)
    p2 = Ponto5D(x+largura, y, z)
    p3 = Ponto5D(x+largura, y+altura, z)
    p4 = Ponto5D(x, y+altura, z)
    p5 = Ponto5D(x, y, z+profundidade)
    p6 = Ponto5D(x+largura, y, z+profundidade)
    p7 = Ponto5D(x+largura, y+altura, z+profundidade)
    p8 = Ponto5D(x, y+altura, z+profundidade)

    face1 = Face([p1, p4, p3, p2]) # Frente
    face2 = Face([p1, p5, p6, p2]) # Topo
    face3 = Face([p1, p5, p8, p4]) # Lado Direito 
    face4 = Face([p2, p6, p7, p3]) # Lado Esquerdo
    face5 = Face([p3, p7, p8, p4]) # Fundo
    face6 = Face([p5, p6, p7, p8]) # Atras

    super(Cubo, self).__init__([face1, face2, face3, face4, face5, face6], cor)


class Piramide(Mesh):
  def __init__(self, x, y, z, altura, largura, profundidade):
    p1 = Ponto5D(x, y, z)
    p2 = Ponto5D(x-largura/2, y-altura/2, z+profundidade)
    p3 = Ponto5D(x+largura/2, y-altura/2, z+profundidade)
    p4 = Ponto5D(x+largura/2, y+altura/2, z+profundidade)
    p5 = Ponto5D(x-largura/2, y+altura/2, z+profundidade)

    face1 = Face([p1, p2, p3]) 
    face2 = Face([p1, p3, p4]) 
    face3 = Face([p1, p4, p5])
    face4 = Face([p1, p5, p2])
    face5 = Face([p2, p3, p4, p5])

    super(Piramide, self).__init__([face1, face2, face3, face4, face5])

    

class Esfera(Mesh):
  def __init__(self, x, y, z, raio, cor, detalhe=12):
    self.centro = Ponto5D(x, y, z)
    self.raio = raio
    pontos = []

    trans = MatrizTransformacao3D()
    trans.translacao(x, y, z)

    for alfa in np.linspace(0, 2*np.pi, detalhe):
      linha = []
      for beta in np.linspace(0, np.pi, detalhe):
        ponto = PontoEsferico(raio, alfa, beta)
        linha.append(ponto)
      pontos.append(linha)

    faces = []

    for ix in range(len(pontos)-1):
      for iy in range(len(pontos[ix])-1):

        a1 = pontos[ix][iy]
        a2 = pontos[ix+1][iy]
        a3 = pontos[ix+1][iy+1]

        f1 = Face([a1.para5D(),a2.para5D(),a3.para5D()])

        f1 = f1.transformar(trans)

        #print(f1)

        faces.append(f1)

        b1 = pontos[ix][iy]
        b2 = pontos[ix][iy+1]
        b3 = pontos[ix+1][iy+1]

        f2 = Face([b1.para5D(),b2.para5D(),b3.para5D()])

        f2 = f2.transformar(trans)

        #print(f2)

        faces.append(f2)

    super(Esfera, self).__init__(faces, cor)

    
 
