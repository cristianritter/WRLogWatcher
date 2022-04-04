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
from datetime import timedelta
import sys
from threading import Thread
import parse_config
from WRFileParser import WRFileParse
from WRDataAnalyser import WRAnalizer
from WRZabbixSender import WRZabbixSender
from WRFileLogger import WRLogger
from WRUserInterf import TabDisparoPraca, TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF

Logger = WRLogger()

try:
    '''Carregamento das informações do arquivo config.ini'''
    configuration = parse_config.ConfPacket() 
    configs = configuration.load_config(
    'default, nomes, default_modes, offsets_ms, diretorios, zabbix_keys, zabbix'  )
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
    
    '''Criação das listas e sets que armazenam os registros de instancias abertas'''
    FILEPARSER = {}
    ANALYZER = {}
    ZABBIXSENDER = {}
    TABS = {}
    THREAD_STATUS = []
    FLAG = 'Serial'
  
    app = wx.App()   #criação da interface gráfica

    '''Criando as instancias de serviços que rodam paralelamente'''
    for idx_, nome in enumerate(NOMES):      
        ZABBIX_KEY=ZABBIX_KEYS[nome]
        FILEPARSER[nome] = WRFileParse()
        ANALYZER[nome] =WRAnalizer(Logger)
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
    FRAME = MF("WR LogWatcher", TABS, NOMES, DIRETORIOS, FLAG, Logger)  #arquivo tabs é um set vazio, vai ser preenchido pela classe MF
    
    '''Criação do TaskBar'''
    TBI(f"WR LogWatcher", FRAME, TABS, NOMES) 

except Exception as Err:
    print("Inicializacao das classes. Erro: ", Err)
    Logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}')


'''Definição de rotinas de serviços que são executados em loop por threads'''

def instancia_de_treading(idx: int, name: str, tab: TabDisparoPraca, parser: WRFileParse, analyzer: WRAnalizer):
    time.sleep((idx+1)/3)   #cria um tempo minimo entre as leituras do arquivo master para evitar conflitos de leitura
    diretorios_list = DIRETORIOS[name].split(', ')       
    
    tab.set_interface_paths(diretorios_list)    #seta label da tab da interface grafica com os diretórios
    last_day = time.strftime('%d')     #armazena o dia atual para limpeza de paineis na virada de data
    recorrente = False
    while True:
        try:
            '''leitura do conteudo dos logs'''
            debug = 1
            mastercontent = parser.get_conteudo_log(DIRETORIOS[ list(NOMES.keys())[0] ].split(', ')[0])
            slavecontent = parser.get_conteudo_log(diretorios_list[0])

            '''limpeza dos paineis de informações na virada do dia'''
            debug = 2
            if (last_day != time.strftime('%d')):  
                tab.clear_content()
                last_day = time.strftime('%d')
                time.sleep(10)            
            
            if (mastercontent == 0):
                continue
            
            '''adicao das informacoes nos paineis'''
            debug = 3
            errors_founded_master = tab.adiciona_informacoes(conteudo=mastercontent, flag=FLAG, selecao='master')
            errors_founded_slave = tab.adiciona_informacoes(conteudo=slavecontent, flag=FLAG, selecao='slave')

            '''Processa os dados e verifica o offset de tempo entre os disparos recebidos'''
            debug = 4
            
            dados_do_log_master = tab.get_4last_flag_lines(flag=FLAG, seletor='master')
            dados_do_log_slave = tab.get_4last_flag_lines(flag=FLAG, seletor='slave')

            if (dados_do_log_master == 0):
                continue
            
            last_line_slave = analyzer.get_similar_line(dados_do_log_master[0], dados_do_log_slave)
            last_but_one_line_slave = analyzer.get_similar_line(dados_do_log_master[1], dados_do_log_slave)
                  
            last_line_offset = analyzer.get_time_offset(dados_do_log_master[0], last_line_slave)  
            last_but_one_line_offset =  analyzer.get_time_offset(dados_do_log_master[1], last_but_one_line_slave)

            '''Detecta o modo de operação do sistema e atualiza o painel com essa informação'''
            debug = 5
            operacao_last_line = analyzer.mode_detect(OFFSETS_MS[name], last_line_offset)
            operacao_last_but_one_line = analyzer.mode_detect(OFFSETS_MS[name], last_but_one_line_offset)
            tab.set_listbox_selected(operacao_last_line)           
            
            '''Seta led de erro em caso de problemas de interpretação dos comandos seriais'''
            debug = 6
            if (errors_founded_master or errors_founded_slave):           
                tab.set_error_led('ledErroInterpretaSerial')
            else:
                tab.clear_error_led('ledErroInterpretaSerial')
            
            '''Seta led de erro caso o modo de operação atual não seja o modo padrão programado
            Atualiza também essa informação na variável de métrica do zabbix
            '''
            debug = 7
            if (not operacao_last_line in DEFAULT_MODES[name] and not operacao_last_but_one_line in DEFAULT_MODES[name]):
                if recorrente == True:                
             
                    tab.set_error_led('ledErroModoOperacao')
                    THREAD_STATUS[idx] |= (1<<0)   #metrica para zabbix -> adiciona 1 se houver erro de posicao da botoneira
                    log = f"Modo de operação anormal detectado em {NOMES[name]}, Dados master: {dados_do_log_master}, Dados slave: {dados_do_log_slave} Operações: {operacao_last_line}, {operacao_last_but_one_line}"
                    
                    adicionar = True
                    for linha in Logger.get_last10_lines():
                        if (log in linha):
                            adicionar = False
                    if adicionar == True:
                        Logger.adiciona_linha_log(log)
                else:
                    recorrente = True
            else:
                recorrente = False
                tab.clear_error_led('ledErroModoOperacao')
                THREAD_STATUS[idx] &= ~(1<<0)

            debug = 8
            '''Informa se o winradio master está com o botoneira na posição de geração'''
            #print('Serial' in dados_do_log_master[0][3])
            if ('Serial' in dados_do_log_master[0][3] and not 'Received' in dados_do_log_master[0][3]):
                THREAD_STATUS[idx] |= (1<<1)   #metrica para zabbix -> adiciona 1 se houver erro de posicao da botoneira
            else:
                THREAD_STATUS[idx] &= ~(1<<1)           

            '''Apresenta informação em texto caso hajam problemas de sincronismo de horário nos computadores dos WINRADIOS
            timestamp do slave menor do que do master [viagem no tempo]
            '''
            debug = 9
            if last_line_offset < timedelta(microseconds = 0) and last_but_one_line_offset < timedelta(microseconds = 0):  
                tab.textoErroTimeSync.Show()
            else:
                tab.textoErroTimeSync.Hide()
 
            '''Atualiza o painel e finaliza aguardando pelo próximo ciclo'''
            debug = 10
            tab.Refresh()  
            time.sleep(60)
            
        except Exception as Err:
            print(f"{NOMES[nome]} - Execucao dos Loops: {Err}")
            Logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}', debug)
            time.sleep(30)


if (__name__ == '__main__'):
    try:
        '''Criacao e start dos threads'''
        t = []
        for idx, nome in enumerate(NOMES):
            if idx == 0:
                continue
            t.append( Thread(target=instancia_de_treading, args=[idx, nome, TABS[nome], FILEPARSER[nome], ANALYZER[nome]], daemon=True)) # True executa o thread somente enquanto o programa estiver aberto
            t[idx-1].start()
            ZABBIXSENDER[nome].start_zabbix_thread()   #inicia thread de envio das metricas pro zabbix
        
        '''Loop de execução da interface gráfica'''
        app.MainLoop()
        
    except Exception as Err:
        print("Erro do loop principal", Err)
        Logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}')