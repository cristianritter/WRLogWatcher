from datetime import datetime
import os

class WRLogger:
    """Registrador de logs em arquivos"""  

    def __init__(self):
        self.LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LOGS') 

    def adiciona_linha_log(self, nome, texto=''):
        dataFormatada = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        mes_ano = datetime.now().strftime('_%Y%m')
        print(f'{dataFormatada} - [{nome}] - {texto} \n')
        try:
            log_file = os.path.join(self.LOGS_DIR, f'log{mes_ano}.txt')
            f = open(log_file, "a")
            f.write(f'{dataFormatada} - [{nome}] - {texto} \n')
            f.close()
        except Exception as err:
            print(f'Erro durante registro no arquivo de log. {err}')
         
if __name__ == '__main__':
    pass
    Logger = WRLogger()
    Logger.adiciona_linha_log('nome', 'descricao do erro')