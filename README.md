# Disciplina de Computação Gráfica

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

* **Professor**: Petrônio Cândido de  Lima e Silva  <span itemscope itemtype="https://schema.org/Person"><a itemprop="sameAs" content="https://orcid.org/0000-0002-1202-2552" href="https://orcid.org/0000-0002-1202-2552" target="orcid.widget" rel="noopener noreferrer" style="vertical-align:top;"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" style="width:1em;margin-right:.5em;" alt="ORCID iD icon"></a></span>
* **Bacharelado em Sistemas de Informação - IFNMG Januária**

Códigos desenvolvidos na disciplina de Computação Gráfica

Licença
=======

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This material is licensed under “Creative Commons Attribution - NonCommercial - ShareAlike” license. All external portions included in this material are cited in loco.

Esse material está licenciado com uma licença  “Creative Commons Atribuição - NãoComercial - CompartilhaIgual”. Todos os materiais externos inclusos neste material serão referenciados in loco.

Instalação
==========

```
git clone https://github.com/petroniocandido/cg_python
```

Exemplos de Uso
===============

* Polígonos 
```
git clone https://github.com/petroniocandido/cg_python
```

* Animação 3D
```
import numpy as np
import PIL
from PIL import Image, ImageDraw
import cg_python.comum
from cg_python.dimensao3 import Ponto3D, Ponto5D, MatrizProjecao3D
from cg_python.transformacoes import MatrizTransformacao3D
from cg_python.animacoes import animar

background=(0,0,0,255)
cor=(255,255,255,255)
camera = Ponto3D(10,10,10)
luz = FonteLuz( Ponto3D(1,10,1) ,1)

def funcao_animacao(tela, quadro):
  proj = MatrizProjecao3D()
  proj.cavalier()

  trans_luz = MatrizTransformacao3D()

  trans_luz.rotacao((np.pi/400)*quadro, (np.pi/600)*quadro, 0)

  luz.posicao = trans_luz.aplicar(luz.posicao)

  cubo = Cubo(150,150,150,100,100,100, cor)

  trans = MatrizTransformacao3D()

  c = cubo.centro()

  trans.translacao(-c.x, -c.y, -c.z)
  cubo = cubo.transformar(trans)
  trans.limpar()

  trans.rotacao((np.pi/200)*quadro, 0, (np.pi/200)*quadro)
  cubo = cubo.transformar(trans)
  trans.limpar()

  #trans.translacao(c.x, c.y, c.z)
  #cubo = cubo.transformar(trans)
  #trans.limpar()

  cubo.sombrear_phong(tela, camera, proj, luz)

  return tela

animar(100, 100, funcao_animacao, 500, 500, "animacao.gif", background=background)
```
