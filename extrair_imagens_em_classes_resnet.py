import os
import shutil

dicionario_camadas_classes = {
    "0": "parallel",
    "1": "divergent",
    "2": "divergent",
    "3": "sigmoid",
    "4": "parallel",
    "5": "chaotic",
    "6": "parallel",
    "7": "parallel",
    "8": "divergent",
    "9": "chaotic"
}


def criar_pasta_resnet(pasta_imagens_por_camada, pasta_imagens_por_face):
    camadas_validas = list(range(10))
    camadas_validas.remove(4)
    camadas_validas.remove(8)

    for c in camadas_validas:

        face_camada = dicionario_camadas_classes[str(c)]

        pasta_origem = os.path.join(pasta_imagens_por_camada, str(c))
        pasta_destino = os.path.join(pasta_imagens_por_face, face_camada)
        os.makedirs(pasta_destino, exist_ok=True)

        lista_imagens = sorted(os.listdir(pasta_origem))
        caminho_origem_imagens = [os.path.join(pasta_origem, img)
                                  for img in lista_imagens]
        caminho_destino_imagens = [os.path.join(pasta_destino, img)
                                   for img in lista_imagens]
        
        for src, dst in zip(caminho_origem_imagens, caminho_destino_imagens):
            shutil.copy(src, dst)
            print(dst, "salvo.")


def main():

    pasta_imagens_por_camada = './imagens_janelas_25000_amostras/training'
    pasta_imagens_por_face = './imagens_janelas_por_classe/training'
    criar_pasta_resnet(pasta_imagens_por_camada, pasta_imagens_por_face)

    pasta_imagens_por_camada = './imagens_janelas_25000_amostras/validation'
    pasta_imagens_por_face = './imagens_janelas_por_classe/validation'
    criar_pasta_resnet(pasta_imagens_por_camada, pasta_imagens_por_face)

if __name__ == "__main__":
    main()
