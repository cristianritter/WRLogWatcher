import wx
import time
import parse_config
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
from WRZabbixSender import WRZabbixSender
from WRFileLogger import WRLogger
from threading import Thread
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF

Logger = WRLogger()

try:
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    #carrega configuracoes do arquivo config.ini
    'default, nomes, default_modes, offsets_ms, diretorios, zabbix_keys, zabbix'  )
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
        'port' :configs['zabbix']['port']}
    FILEPARSER = {}
    ANALYZER = {}
    ZABBIXSENDER = {}
    TABS = {}
    THREAD_STATUS = []

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
    FRAME = MF("WR LogWatcher", TABS, NOMES, DIRETORIOS, FLAG)  #arquivo tabs é criado aqui dentro por ponteiro
    TBI(f"WR LogWatcher", FRAME, TABS, NOMES) 
except Exception as Err:
    print("Inicializacao das classes. Erro: ", Err)
    Logger.adiciona_linha_log('Inicialização das classes', Err)


def loop_execucao(idx, name, tab, parser, analyzer):
    time.sleep((idx+1)/3) #cria um tempo minimo entre as leituras do arquivo master para evitar conflitos de leitura
    tab.clear_content()
    tab.set_interface_paths(DIRETORIOS[nome].split(', '))      
    last_day = time.strftime('%d')
    while True:
        try:
            if last_day != time.strftime('%d'):  #limpa o painel de informações na virada do dia
                tab.clear_content()
                last_day = time.strftime('%d')
                time.sleep(20)

            mastercontent = parser.get_conteudo_log('master')
            slavecontent = parser.get_conteudo_log('slave')
            if len(mastercontent) != len(slavecontent):
                tab.set_error_led('led2')
            else:
                tab.clear_error_led('led2')                       
            for linha in mastercontent:
                tab.adiciona_informacoes(linha[0], linha[1], selecao='master')
            for linha in slavecontent:
                tab.adiciona_informacoes(linha[0], linha[1], selecao='slave')
            dados_do_log_master = parser.get_last_flag_line('master')
            dados_do_log_slave = parser.get_last_flag_line('slave')
            current_offset = analyzer.get_time_offset(dados_do_log_master, dados_do_log_slave)
            if current_offset[1] == -1:  # exibe aviso se erro de sinc de horario nos pcs monitorados
                tab.texto02a.Show()
            else:
                tab.texto02a.Hide()
            operacao_detectada = analyzer.mode_detect(OFFSETS_MS[name], current_offset[0])
            tab.set_listbox_selected(operacao_detectada)           
            if (not operacao_detectada in DEFAULT_MODES[name]):
                tab.set_error_led('led1')
                THREAD_STATUS[idx] = 1   #envia metrica para zabbix -> 1 se houver erro, 0 se tudo estiver bem
            else:
                tab.clear_error_led('led1')
                THREAD_STATUS[idx] = 0
            tab.Refresh()    
            time.sleep(5)
            
        except Exception as Err:
            print(f"{NOMES[nome]} - Erro execucao loops: {Err}")
            Logger.adiciona_linha_log(f'Execução dos loops: {name}', Err)
            time.sleep(30)


if (__name__ == '__main__'):
    try:
        t = []
        for idx, nome in enumerate(NOMES):
            t.append( Thread(target=loop_execucao, args=[idx, nome, TABS[nome], FILEPARSER[nome], ANALYZER[nome]], daemon=True)) # True executa o thread somente enquanto o programa estiver aberto
            t[idx].start()
            ZABBIXSENDER[nome].start_zabbix_thread()   #inicia thread de envio das metricas pro zabbix
        app.MainLoop()
        
    except Exception as Err:
        print("Erro1", Err)
        Logger.adiciona_linha_log('Main:', Err)