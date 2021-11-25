from pyzabbix import ZabbixMetric, ZabbixSender
import time
import parse_config
from threading import Thread

def send_status_metric(value):
    '''Envia metricas para zabbix:    
           
    Sugestão de uso:
        Em caso de problemas -> envia mensagem contendo informações do erro [strlen > 1]
            Em caso de sucesso nas rotinas -> envia flag str com '0' [strlen == 1]'''
    try:
        configuration = parse_config.ConfPacket()
        configs = configuration.load_config(
        'zabbix'  #carrega configuracoes do arquivo config.ini
        )
        while 1:
            #print("passou")
            time.sleep(int(configs['zabbix']['send_metrics_interval']))
    
            try:
                packet = [
                    ZabbixMetric(configs['zabbix']['hostname'], configs['zabbix']['key'], value[0])
                ]
                ZabbixSender(zabbix_server=configs['zabbix']['zabbix_server'], zabbix_port=int(configs['zabbix']['port'])).send(packet)
            except Exception as Err:
                print(f"Falha de conexão com o Zabbix - {Err}")
    except Exception as Err:
        print(f"Erro: {Err}")

def start_zabbix_thread(v_data):
    """v_data é o valor da metrica que precisa ser passado como lista e pode ser alterada no contexto do programa"""
    try:
        u = Thread(target=send_status_metric, args=[v_data], daemon=True)
        u.start()
    except Exception as Err:
        print(f'Erro: {Err}')

if __name__ == '__main__':
    data = [1]
    start_zabbix_thread(data)
    while(True):
        time.sleep(1)
        pass