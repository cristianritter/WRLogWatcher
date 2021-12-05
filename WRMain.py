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
    'diretorios, default, offsets, zabbix'  #carrega configuracoes do arquivo config.ini
    )

    PRACA = configs['default']['nome_praca']
    FLAG = configs['default']['flag_string']
    FLAG_MAX_TIME = int(configs['default']['flag_max_time_seconds'])
    LOG_PATH_MASTER = (configs['diretorios']['pasta_logs_master'])  #carrega o diretorio dos logs master que servem como referencia
    LOG_PATH_SLAVE = (configs['diretorios']['pasta_logs_slave'])  #carrega o diretorio dos logs slave que serao monitorados
    OPERACAO_PADRAO = configs['default']['modo_operacao_padrao']
    CONFIG_OFFSETS = {
        'sat_poa_sat_poa' :int(configs['offsets']['sat_poa_sat_poa']),
        'sat_poa_barix_ms' :int(configs['offsets']['sat_poa_barix_ms']),
        'sat_poa_sat_reg_ms' :int(configs['offsets']['sat_poa_sat_reg_ms']),
    }
    ZABBIX_CONFIG = {
        'metric_interval' :int(configs['zabbix']['send_metrics_interval']),
        'hostname' :configs['zabbix']['hostname'],
        'key' :configs['zabbix']['key'],
        'server' :configs['zabbix']['zabbix_server'],
        'port' :int(configs['zabbix']['port'])
    }
    
    
    parser = WRFileParse(FLAG, LOG_PATH_MASTER, LOG_PATH_SLAVE)
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
    frame.masterpath = LOG_PATH_MASTER
    frame.slavepath = LOG_PATH_SLAVE
    
    TBI(frame, "WR LogWatcher", PRACA)
except Exception as Err:
    print("Erro: ", Err)

def loop_execucao(parser, ZMETRICA):
    while True:
        time.sleep(1)
        try:
            pass
            frame.carrega_informacoes(' \n'.join(parser.get_conteudo_log('master')), descricao='master')
            frame.carrega_informacoes(' \n'.join(parser.get_conteudo_log('slave')), descricao='slave')
            
            dados_do_log_master = parser.get_last_flag_line('master')
            dados_do_log_slave = parser.get_last_flag_line('slave')
            current_offset = analizer.get_time_offset(dados_do_log_master, dados_do_log_slave)

            operacao_detectada = analizer.mode_detect(CONFIG_OFFSETS, current_offset)
            frame.set_listbox_selected(operacao_detectada)
            if (not operacao_detectada in OPERACAO_PADRAO):
                frame.set_error_led()
            else:
                frame.clear_error_led()
            
            #if fail_status:     #envia metrica para zabbix -> 1 se houver erro, 0 se tudo estiver bem
            #    ZMETRICA[0] = 1
            #else:
            #    ZMETRICA[0] = 0
            
        except Exception as Err:
            print("Erro: ", Err)

if (__name__ == '__main__'):
    try:
        t = Thread(target=loop_execucao, args=[parser, ZMETRICA], daemon=True)  # True executa o thread somente enquanto o programa estiver aberto
        t.start()
        zsender.start_zabbix_thread(ZMETRICA)   #inicia thread de envio das metricas pro zabbix
        app.MainLoop()
   
    except Exception as Err:
        print(Err)