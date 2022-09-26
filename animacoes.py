import numpy as np
import PIL
from PIL import Image

def animar(num_frames, duracao, funcao_animacao, largura, altura, arquivo_gif, background="white"):
  #LOOP PRINCIPAL
  
  # LISTA DOS FRAMES DA ANIMAÇÃO
  frames = []

  # REPETE DE 0 ATÉ O NÚMERO DE FRAMES
  for i in range(num_frames):

    # CRIA A NOVA IMAGEM VAZIA
    tela = Image.new(mode="RGBA", size=(altura,largura), color=background)

    # PASSA A IMAGEM EM BRANCO E O NÚMERO DO FRAME PARA A FUNÇÃO DE ANIMAÇÃO
    new_frame = funcao_animacao(tela, i) 

    # ADICIONA O NOVO FRAME GERADO À LISTA DE FRAMES
    frames.append(new_frame)

  # SALVA A ANIMAÇÃO EM UM ARQUIVO .GIF, COM 40 MILISEGUNDOS ENTRE CADA FRAME
  frames[0].save(arquivo_gif, format='GIF', append_images=frames[1:], save_all=True, duration=duracao, loop=0)
