'''Main do projeto'''

import sys
import cv2 as cv
from modules import find_obj
from modules import camera
from modules import motores
from modules import dijsktra


def main():
    ''' Execucao principal de todo o projeto'''
    find = find_obj
    cam = camera

    base_a = './imagens/baseA.jpg'
    base_b = './imagens/baseB.jpg'
    base_c = './imagens/baseC.jpg'
    base_d = './imagens/baseD.jpg'
    esquerda = './imagens/esquerda.jpg'
    direita = './imagens/direita.jpg'
    chegou = './imagens/chegou.jpg'
    frente = './imagens/frente.jpg'

    graph = dijsktra.Graph([])
    graph.add_edge("a", "c", 1)
    graph.add_edge("a", "d", 4)
    graph.add_edge("b", "c", 1)
    graph.add_edge("b", "d", 1)
    # graph.add_edge("c", "d", 1)

    base_a = cv.imread(base_a, 0)
    base_b = cv.imread(base_b, 0)
    base_c = cv.imread(base_c, 0)
    base_d = cv.imread(base_d, 0)
    esquerda = cv.imread(esquerda, 0)
    direita = cv.imread(direita, 0)
    chegou = cv.imread(chegou, 0)
    frente = cv.imread(frente, 0)

    def converte(path):
        ''' Converte os nomes de cada node para a imagem lida
        pelo opencv.

        Input = {
            "a", "b", "c" ...
        }
        Type = str

        Output = {
            base_a, base_b, base_c ...
        }
        Type = numpy.ndarray
        '''
        path_refinado = []
        for item in path:
            if item == "a":
                path_refinado.append(base_a)
            elif item == "b":
                path_refinado.append(base_b)
            elif item == "c":
                path_refinado.append(base_c)
            elif item == "d":
                path_refinado.append(base_d)

        return path_refinado


    path = (graph.dijkstra("a", "d"))
    print('Indo de %s para %s' % (path[0], path[(len(path)-1)]))
    print('Por {0}'.format(path))
    path_limpo = converte(path)
    y = 0
    falha = 0

    while True:
        print('Lendo linhas')
        motores.lerlinhas()
        print('Tirando foto')
        pic_ext = cam.tira_foto()
        img2 = cv.cvtColor(pic_ext, cv.COLOR_BGR2GRAY)
        print('Buscando por: {0}'.format(path[y]))
        busca = find.main('sift', path_limpo[y], img2)
        if busca[0][0] == -999:
            print("Nada encontrado")
            falha = falha + 1
        else:
            print("Padrao encontrado")
            print(busca)
            crop_img = img2[busca[0][1]:busca[2][1], busca[0][0]:busca[2][0]]
            falha = 0
        busca[0][0] = -999
        direcao = ''
        x = 0
        print('Buscando direcao')
        while(busca[0][0] == -999 and falha == 0):

            if x == 0:
                busca = find.main('sift', chegou, crop_img)
                x = 1
                direcao = 'chegou'
                falha = 0
            elif x == 1:
                busca = find.main('sift', direita, crop_img)
                x = 2
                direcao = 'direita'
                falha = 0
            elif x == 2:
                busca = find.main('sift', esquerda, crop_img)
                x = 3
                direcao = 'esquerda'
                falha = 0
            elif x == 3:
                busca = find.main('sift', frente, crop_img)
                x = 4
                direcao = 'frente'
                falha = 0
            elif x == 4:
                print('Direcao nao encontrada')
                direcao = 'nada'
                falha = falha + 1

        if falha == 0:
            motores.virar(direcao)
            print('Direcao encontrada: {0}'.format(direcao))
            print(path_limpo[y])
            if direcao == 'chegou':
                print("Estacao %s alcancada" % (path[y]))
                y = y + 1
                try:
                    ponto_atual = path[y]
                except:
                    print("Destino encontrado")
                    sys.exit(1)
        elif falha == 1:
            motores.virar('nada')
        elif falha == 2:
            motores.virar('esquerda fino')
        elif falha == 3:
            motores.virar('direita fino')
        elif falha == 4:
            print("Falha de leitura - PARANDO")
            sys.exit(1)


if __name__ == '__main__':
    main()
