import os
from datetime import datetime, time
from file_read_backwards import FileReadBackwards
import time

LOG_PATH = '//10.70.40.34\STEP Software\WinRadioMax\Logs'

def get_log_filename():
    """retorna o caminho completo para acesso ao arquivo de log"""
    log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
    log_fullfilepath = os.path.join(LOG_PATH, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
    return log_fullfilepath

def keep_opened():
        """MANTEM O ARQUIVO DE LOG CARREGADO NA MEMORIA ENQUANTO O WINRADIO EXECUTA GRAVACOES DE NOVAS LINHAS PARA TESTAR O COMPORTAMENTO DO SISTEMA
        EXCECOES GERADAS E MAIS..."""
        try:
            arquivo_de_log = get_log_filename()
            conteudo = []
            with FileReadBackwards(arquivo_de_log, encoding='utf-8') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for linha in frb:
                    print(linha)
                while True:
                    time.sleep(1)
                    pass
            return conteudo
        except Exception as Err:
            print(Err)

keep_opened()