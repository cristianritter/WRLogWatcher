import wx
import time
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
from WRZabbixSender import WRZabbixSender
import parse_config
from threading import Thread
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF

ZMETRICA = [""]

try:
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'diretorios, default, zabbix'  #carrega configuracoes do arquivo config.ini
    )

    PRACA = configs['default']['nome_praca']
    FLAG = configs['default']['flag_string']
    FLAG_MAX_TIME = int(configs['default']['flag_max_time_seconds'])
    LOG_PATH = (configs['diretorios']['pasta_raiz_dos_logs'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini
    ZABBIX_CONFIG = {
        'metric_interval' :int(configs['zabbix']['send_metrics_interval']),
        'hostname' :configs['zabbix']['hostname'],
        'key' :configs['zabbix']['key'],
        'server' :configs['zabbix']['zabbix_server'],
        'port' :int(configs['zabbix']['port'])
    }
    
    parser = WRFileParse(FLAG, LOG_PATH)
    analizer = WRAnalizer(FLAG_MAX_TIME)
    zsender = WRZabbixSender(
        ZABBIX_CONFIG['metric_interval'],
        ZABBIX_CONFIG['hostname'],
        ZABBIX_CONFIG['key'],
        ZABBIX_CONFIG['server'],
        ZABBIX_CONFIG['port'],
        ZMETRICA
        )

    app = wx.App()
    frame = MF("WR LogWatcher", PRACA)  #criacao do frame recebe o nome da janela
    TBI(frame)
except Exception as Err:
    print("Erro: ", Err)

def loop_execucao(fileparser, ZMETRICA):
    while True:
        time.sleep(1)
        try:
            dados_do_log = fileparser.get_last_flag_line()
            frame.carrega_informacoes(' \n'.join(fileparser.get_conteudo_log()))
            
            fail_status = (analizer.verifica_erros(dados_do_log)) 
            frame.informa_erro(fail_status)

        except Exception as Err:
            print("Erro: ", Err)

if (__name__ == '__main__'):
    try:
        t = Thread(target=loop_execucao, args=[parser, ZMETRICA], daemon=True)  # True executa o thread somente enquanto o programa estiver aberto
        t.start()
        zsender.start_zabbix_thread(ZMETRICA)
        app.MainLoop()
   
    except Exception as Err:
        print(Err)