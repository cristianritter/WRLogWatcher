import wx
import time
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
import parse_config
from threading import Thread
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF
#import locale

#locale.setlocale(locale.LC_ALL, 'pt-BR.UTF-8')

configuration = parse_config.ConfPacket()
configs = configuration.load_config(
'diretorios, default'  #carrega configuracoes do arquivo config.ini
)

FLAG = configs['default']['flag_string']
FLAG_MAX_TIME = int(configs['default']['flag_max_time_seconds'])
LOG_PATH = (configs['diretorios']['pasta_raiz_dos_logs'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini

parser = WRFileParse(FLAG, LOG_PATH)
analizer = WRAnalizer(FLAG_MAX_TIME)

app = wx.App()
frame = MF("WR LogWatcher")  #criacao do frame recebe o nome da janela
TBI(frame)


def loop_execucao(fileparser):
    while True:
        dados_do_log = fileparser.get_last_flag_line()
        frame.carrega_informacoes(' \n'.join(fileparser.get_conteudo_log()))

        #fail_status = (analizer.verifica_erros(dados_do_log))   
        #print(fail_status)    
        #frame.informa_erro(fail_status)

        time.sleep(1)
    pass

if (__name__ == '__main__'):
    try:
        t = Thread(target=loop_execucao, args=[parser], daemon=True)  # True executa o thread somente enquanto o programa estiver aberto
        t.start()
        app.MainLoop()
   
    except Exception as Err:
        print(Err)