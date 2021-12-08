import wx
import time

from wx.core import Frame
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
from WRZabbixSender import WRZabbixSender
import parse_config
from threading import Thread
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF


try:
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'default, nomes, default_modes, offsets_ms, diretorios, zabbix_keys, zabbix'  #carrega configuracoes do arquivo config.ini
    )

   
    FLAG = configs['default']['flag_string']
    FLAG_MAX_TIME = int(configs['default']['flag_max_time_seconds'])
 
    NOMES = configs['nomes']
    DEFAULT_MODES = configs['default_modes']
    OFFSETS_MS = configs['offsets_ms']
    DIRETORIOS = configs['diretorios']  #carrega o diretorio dos logs 
    ZABBIX_KEYS = configs['zabbix_keys']
 
    ZABBIX_CONFIG = {
        'metric_interval' :configs['zabbix']['send_metrics_interval'],
        'hostname' :configs['zabbix']['hostname'],
        'server' :configs['zabbix']['zabbix_server'],
        'port' :configs['zabbix']['port']
    }
    
    FILEPARSER = {}
    ANALYZER = {}
    ZABBIXSENDER = {}
    THREAD_STATUS = []

    FRAMES = {}

    app = wx.App()
    
    for idx_, nome in enumerate(NOMES):    # loop que inicia todas as instancias de config encontradas
 
        LOG_PATHS=DIRETORIOS[nome].split(', ')
        ZABBIX_KEY=ZABBIX_KEYS[nome]
        FILEPARSER[nome] = WRFileParse(FLAG, LOG_PATHS)
        ANALYZER[nome] =WRAnalizer(FLAG_MAX_TIME)
        THREAD_STATUS.append(1)  #enviar erro como estado inicial
        ZABBIXSENDER[nome] = WRZabbixSender(
            metric_interval= ZABBIX_CONFIG['metric_interval'],
            hostname= ZABBIX_CONFIG['hostname'],
            key=ZABBIX_KEY,
            server= ZABBIX_CONFIG['server'],
            port= ZABBIX_CONFIG['port'],
            idx= idx_,
            status= THREAD_STATUS
        )

        FRAMES[nome] = MF(f"WR LogWatcher - {NOMES[nome]}")  #criacao do frame recebe o nome da janela
    TBI(f"WR LogWatcher", NOMES, FRAMES)
   
except Exception as Err:
    print("Erro: ", Err)

def loop_execucao(idx, name, frame, parser, analyzer):
    while True:
        time.sleep(5)
        try:
            frame.carrega_informacoes(' \n'.join(parser.get_conteudo_log('master')), selecao='master')
            frame.carrega_informacoes(' \n'.join(parser.get_conteudo_log('slave')), selecao='slave')
            
            dados_do_log_master = parser.get_last_flag_line('master')
            dados_do_log_slave = parser.get_last_flag_line('slave')
            current_offset = analyzer.get_time_offset(dados_do_log_master, dados_do_log_slave)
         
            if current_offset[1] == -1:  # exibe aviso se erro de sinc de horario nos pcs monitorados
                frame.texto02a.Show()
            else:
                frame.texto02a.Hide()

            operacao_detectada = analyzer.mode_detect(OFFSETS_MS[name], current_offset[0])
            frame.set_listbox_selected(operacao_detectada)
            
            if (not operacao_detectada in DEFAULT_MODES[name]):
                frame.set_error_led()
                THREAD_STATUS[idx] = 1   #envia metrica para zabbix -> 1 se houver erro, 0 se tudo estiver bem
            else:
                frame.clear_error_led()
                THREAD_STATUS[idx] = 0
            
        except Exception as Err:
            print("Erro: ", Err)

if (__name__ == '__main__'):
    try:
        t = []
        for idx, nome in enumerate(NOMES):
            pass
            t.append( Thread(target=loop_execucao, args=[idx, nome, FRAMES[nome], FILEPARSER[nome], ANALYZER[nome]], daemon=True)) # True executa o thread somente enquanto o programa estiver aberto
            t[idx].start()
            ZABBIXSENDER[nome].start_zabbix_thread()   #inicia thread de envio das metricas pro zabbix
        
        app.MainLoop()
        
    except Exception as Err:
        print("Erro1", Err)