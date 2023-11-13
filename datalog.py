import datetime
import os
from ftplib import FTP
import schedule
import time
import random
#pip install schedule
def criar_mensagem():
    # Obtém a data e hora atual
    agora = datetime.datetime.now()
    data_hora = agora.strftime("%Y-%m-%d %H:%M:%S")

    # Gera um número aleatório de 1 a 50
    numero = str(random.randint(1, 50))

    # Formata a mensagem
    mensagem = f"{data_hora},{numero}"

    return mensagem

def escrever_log_local(mensagem):
    with open("data.tmp", "a") as arquivo:
        arquivo.write(mensagem + "\n")

def enviar_para_telemovel(mensagem):
    # Configurações FTP
    endereco_ftp = "192.168.1.4"
    porta_ftp = 2121

    # Conecta ao servidor FTP
    with FTP() as ftp:
        ftp.connect(endereco_ftp, porta_ftp)
        ftp.login()

        # Nome do arquivo no telemóvel (data e hora sem espaços)
        nome_arquivo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.txt")

        # Escreve o arquivo temporário no telemóvel
        with open("data.tmp", "rb") as arquivo:
            ftp.storbinary(f"STOR {nome_arquivo}", arquivo)

def tarefa_agendada():
    mensagem = criar_mensagem()
    escrever_log_local(mensagem)
    enviar_para_telemovel(mensagem)

# Agendamento da tarefa a cada 15 segundos
schedule.every(15).seconds.do(tarefa_agendada)
print("\x1bc\x1b[43;30m")

while True:
    schedule.run_pending()
    time.sleep(1)

