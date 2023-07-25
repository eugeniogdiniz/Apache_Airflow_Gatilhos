import shutil
import os
import glob

def extrair_texto_arquivo(texto, delimitador):
    partes = texto.rsplit(delimitador, 1)  # Dividir a string usando o delimitador como referência, apenas uma vez (a partir da direita)
    if len(partes) > 1:
        return partes[1]
    else:
        return texto  # Caso o delimitador não seja encontrado, retorna a string original

def tratamento_de_dados(arquivo):
    arquivo = extrair_texto_arquivo(arquivo, '/')
    caminho_origem = f'/home/eugenio/Documentos/Gatilhos_Python/pasta_origem/{arquivo}'
    caminho_destino = f'/home/eugenio/Documentos/Gatilhos_Python/pasta_destino/{arquivo}'
    shutil.move(caminho_origem, caminho_destino)

def main():
    pasta = '/home/eugenio/Documentos/Gatilhos_Python/pasta_origem' 
    extensao_arquivo = "*.csv"

    caminho_arquivos = os.path.join(pasta, extensao_arquivo)

    arquivos_encontrados = glob.glob(caminho_arquivos)

    if not arquivos_encontrados:
        print("Nenhum arquivo Excel encontrado na pasta. Nenhum tratamento de dados será executado.")
    else:
        print(f"Encontrados {len(arquivos_encontrados)} arquivos Excel. Executando tratamento de dados para cada um...")
        for arquivo in arquivos_encontrados:
            print(f"Arquivo: {arquivo}")
            tratamento_de_dados(arquivo)

if __name__ == "__main__":
    main()