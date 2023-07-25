import sys
sys.path.append("airflow_pipeline")

import time
import datetime
import shutil
import os
import glob
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Caminho absoluto para o diretório onde 'meu_script.py' está localizado
caminho_absoluto = "/home/eugenio/Documentos/Gatilhos_Python/scr/script/"

# Adiciona o caminho absoluto à variável de ambiente 'PYTHONPATH'
os.environ["PYTHONPATH"] = os.pathsep.join([os.environ.get("PYTHONPATH", ""), caminho_absoluto])

dt_pasta = days_ago(0)

with DAG(
        "Teste_gatilho",
        start_date = datetime.datetime(2023, 7, 7, 17, 0, 0),
        schedule_interval='0 17-20 * * 1-5', 
    ) as dag:

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


    movimento_pasta = PythonOperator(task_id="movimento_pasta",
                                    python_callable=main,  # Função do script que será executada
                                    dag=dag)
    
    movimento_pasta