import parse_config
import os
from datetime import datetime, timedelta

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
configuration = parse_config.ConfPacket()
configs = configuration.load_config(
'diretorios'
)

filename = f'Comm_{datetime.now().year}_{datetime.now().month}_{datetime.now().day}.txt'  # define o nome do arquivo de log atual baseado na data de hoje
log_path = (configs['diretorios']['pasta_raiz_dos_logs'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini

arquivo_de_log = os.path.join(log_path, filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo

try:
    with open(arquivo_de_log, 'r', encoding='utf-8') as file:
        print(file.read())
except Exception as Err:
    print("Erro ao abrir o arquivo. Verifique o caminho no arquivo 'config.ini'")
    print(Err)
