"""Aplicativo de monitoração do sistema de disparos do WinRadio das rádios do grupo NSC de Santa Catarina"""

__author__ = "Cristian Ritter"
__copyright__ = "Copyright 2021, WRLogWatcher"
__credits__ = ["empty"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Cristian Ritter"
__email__ = "cristianritter@gmail.com"
__status__ = "Production"

'''Importando classes utilizadas'''
import wx
import time
from threading import Thread
import parse_config
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
from WRZabbixSender import WRZabbixSender
from WRFileLogger import WRLogger
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF

Logger = WRLogger()

try:
    '''Carregamento das informações do arquivo config.ini'''
    configuration = parse_config.ConfPacket() 
    configs = configuration.load_config(
    'default, nomes, default_modes, offsets_ms, diretorios_disparos, zabbix_keys, zabbix'  )
    FLAG = configs['default']['flag_string']
    NOMES = configs['nomes']
    DEFAULT_MODES = configs['default_modes']
    OFFSETS_MS = configs['offsets_ms']
    DIRETORIOS_DISPARO = configs['diretorios_disparos']  #carrega o diretorio dos logs 
    ZABBIX_KEYS = configs['zabbix_keys']
    ZABBIX_CONFIG = {
        'metric_interval' :configs['zabbix']['send_metrics_interval'],
        'hostname' :configs['zabbix']['hostname'],
        'server' :configs['zabbix']['zabbix_server'],
        'port' :configs['zabbix']['port']}
    
    '''Criação das listas e sets que armazenam os registros de instancias abertas'''
    FILEPARSER = {}
    ANALYZER = {}
    ZABBIXSENDER = {}
    TABS = {}
    THREAD_STATUS = []
  
    app = wx.App()   #criação da interface gráfica

    '''Criando as instancias de serviços que rodam paralelamente'''
    for idx_, nome in enumerate(NOMES):      
    #    LOG_PATHS=DIRETORIOS_DISPARO[nome].split(', ')
        ZABBIX_KEY=ZABBIX_KEYS[nome]
        FILEPARSER[nome] = WRFileParse()
        ANALYZER[nome] =WRAnalizer()
        THREAD_STATUS.append(0)  #enviar OK como estado inicial
        ZABBIXSENDER[nome] = WRZabbixSender(
            metric_interval= ZABBIX_CONFIG['metric_interval'],
            hostname= ZABBIX_CONFIG['hostname'],
            key=ZABBIX_KEY,
            server= ZABBIX_CONFIG['server'],
            port= ZABBIX_CONFIG['port'],
            idx= idx_,
            status= THREAD_STATUS
        )
    
    '''Criação do frame principal da interface gráfica'''
    FRAME = MF("WR LogWatcher", TABS, NOMES, DIRETORIOS_DISPARO, FLAG)  #arquivo tabs é um set vazio, vai ser preenchido pela classe MF
    
    '''Criação do TaskBar'''
    TBI(f"WR LogWatcher", FRAME, TABS, NOMES) 

except Exception as Err:
    print("Inicializacao das classes. Erro: ", Err)
    Logger.adiciona_linha_log('Inicialização das classes', Err)


'''Definição de rotinas de serviços que são executados em loop por threads'''
def instancia_de_treading(idx, name, tab, parser, analyzer):
    time.sleep((idx+1)/3)   #cria um tempo minimo entre as leituras do arquivo master para evitar conflitos de leitura
    diretorios_list = DIRETORIOS_DISPARO[name].split(', ')       
    tab.set_interface_paths(diretorios_list)    #seta label da tab da interface grafica com os diretórios
    last_day = time.strftime('%d')     #armazena o dia atual para limpeza de paineis na virada de data
    
    while True:
        try:
            '''limpeza dos paineis de informações na virada do dia'''
            if last_day != time.strftime('%d'):  
                tab.clear_content()
                last_day = time.strftime('%d')
                time.sleep(10)
            
            '''leitura do conteudo dos logs'''
            mastercontent = parser.get_conteudo_log(diretorios_list[0])
            slavecontent = parser.get_conteudo_log(diretorios_list[1])
            
            '''adicao das informacoes nos paineis'''
            errors_founded_master = tab.adiciona_informacoes(conteudo=mastercontent, flag=FLAG, selecao='master')
            errors_founded_slave = tab.adiciona_informacoes(conteudo=slavecontent, flag=FLAG, selecao='slave')
            
            '''Processa os dados e verifica o offset de tempo entre os disparos recebidos'''
            dados_do_log_master = tab.get_last_flag_line(flag=FLAG, seletor='master')
            dados_do_log_slave = tab.get_last_flag_line(flag=FLAG, seletor='slave')
            current_offset = analyzer.get_time_offset(dados_do_log_master, dados_do_log_slave)    

            '''Detecta o modo de operação do sistema e atualiza o painel com essa informação'''
            operacao_detectada = analyzer.mode_detect(OFFSETS_MS[name], current_offset[0])
            tab.set_listbox_selected(operacao_detectada)           
            
            '''Seta led de erro em caso de problemas de interpretação dos comandos seriais'''
            if (errors_founded_master or errors_founded_slave):           
                tab.set_error_led('ledErroInterpretaSerial')
            else:
                tab.clear_error_led('ledErroInterpretaSerial')
            
            '''Seta led de erro caso o modo de operação atual não seja o modo padrão programado
            Atualiza também essa informação na variável de métrica do zabbix
            '''
            if (not operacao_detectada in DEFAULT_MODES[name]):
                tab.set_error_led('ledErroModoOperacao')
                THREAD_STATUS[idx] = 1   #metrica para zabbix -> 1 se houver erro, 0 se tudo ok
            else:
                tab.clear_error_led('ledErroModoOperacao')
                THREAD_STATUS[idx] = 0

            '''Apresenta informação em texto caso hajam problemas de sincronismo de horário nos computadores dos WINRADIOS
            timestamp do slave menor do que do master [viagem no tempo]
            '''
            if current_offset[1] == -1:  
                tab.textoErroTimeSync.Show()
            else:
                tab.textoErroTimeSync.Hide()
 
            '''Atualiza o painel e finaliza aguardando pelo próximo ciclo'''
            tab.Refresh()    
            time.sleep(5)
            
        except Exception as Err:
            print(f"{NOMES[nome]} - Erro execucao loops: {Err}")
            Logger.adiciona_linha_log(f'Execução dos loops: {name}', Err)
            time.sleep(30)


if (__name__ == '__main__'):
    try:
        '''Criacao e start dos threads'''
        t = []
        for idx, nome in enumerate(NOMES):
            t.append( Thread(target=instancia_de_treading, args=[idx, nome, TABS[nome], FILEPARSER[nome], ANALYZER[nome]], daemon=True)) # True executa o thread somente enquanto o programa estiver aberto
            t[idx].start()
            ZABBIXSENDER[nome].start_zabbix_thread()   #inicia thread de envio das metricas pro zabbix
        
        '''Loop de execução da interface gráfica'''
        app.MainLoop()
        
    except Exception as Err:
        print("Erro do loop principal", Err)
        Logger.adiciona_linha_log('Main:', Err)