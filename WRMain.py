import wx
import time
from threading import Thread
from WRDataAnalyser import verifica_erros
from WRFileParser import parse_file, le_arquivo
from WRUserInterf import TaskBarIcon as TBI
from WRUserInterf import MyFrame as MF

dados_do_log = parse_file()
estado_de_falha = True

def loop_execucao(estado):
    while True:
        estado = (verifica_erros(dados_do_log))       
        time.sleep(1)
    pass

if (__name__ == '__main__'):
    try:
        t = Thread(target=loop_execucao, args=(estado_de_falha, ), daemon=True)  # True executa o thread somente enquanto o programa estiver aberto
        t.start()

        app = wx.App()
        frame = MF("WR LogWatcher")  #criacao do frame recebe o nome da janela
        TBI(frame)
        #frame.carrega_informacoes(' '.join(parse_file()) )
        frame.informa_erro(estado_de_falha)
        app.MainLoop()
   
    except Exception as Err:
        print(Err)