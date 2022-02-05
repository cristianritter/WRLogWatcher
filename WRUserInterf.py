"""Biblioteca de criacao da interface do usuario"""
import wx.adv
import wx
import os
import locale
from WRFileParser import WRFileParse

def InitLocale(self):
    """
    Substituição do método padrão devido a problemas relacionados a detecção de locale no Windows 7.
    Não foi testado no windows 10.
    """
    self.ResetLocale()
    try:
        lang, _ = locale.getdefaultlocale()
        self._initial_locale = wx.Locale(lang, lang[:2], lang)
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')  #pulo do gato
    except (ValueError, locale.Error) as ex:
        target = wx.LogStderr()
        orig = wx.Log.SetActiveTarget(target)
        wx.LogError("Unable to set default locale: '{}'".format(ex))
        wx.Log.SetActiveTarget(orig)
wx.App.InitLocale = InitLocale   #substituindo metodo que estava gerando erro por um metodo vazio

def adiciona_informacoes(self, conteudo, flag, selecao='master', errors_list=['Error', 'filtrado', 'Set']):
    """Funcao que acrescenta dados aos paineis de informacoes da tab,
    retorna uma flag que indica se existem erros nos dados adicionados"""
    found_errors_flag = False
    if selecao == 'master':
        painel = self.logpanel_master    
    
    elif selecao == 'slave':
        painel = self.logpanel_slave

    else:
        raise(NameError, 'parametro incorreto em adiciona informacoes')

    for _, linha in enumerate(conteudo):  
        error_flag = False
        for erro in errors_list:
            if (erro.lower() in linha.lower()):
                error_flag = True
        if (flag in linha):
            painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.WHITE))
        elif (error_flag):
            painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.RED))
            found_errors_flag = True
        else:
            painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
        if (linha not in painel.GetValue()):
            painel.AppendText(f'{linha}')
    return found_errors_flag   

class TabDisparoPraca(wx.Panel):
    """Classe de criação de uma tab de instancia de WINRADIO monitorado"""
    def __init__(self, parent, names, paths):
        warning_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        super().__init__(parent=parent) 
        self.names = names
        self.paths = paths
        coluna_geral = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        self.listboxmode = ''
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        texto01b1 = wx.StaticText(self, label='Log de eventos do sistema de referência', style=wx.ALIGN_CENTER, size=(600,15))
        self.textoMasterPath = wx.StaticText(self, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(600,15))
        self.logpanel_master = wx.TextCtrl(self, value='', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(600,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        texto01b2 = wx.StaticText(self, label='Log de eventos do sistema monitorado', style=wx.ALIGN_CENTER, size=(600,15))
        self.texto01b2b = wx.StaticText(self, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(600,15))
        self.logpanel_slave = wx.TextCtrl(self, value='', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(600,400))  #cria um edit
        self.logpanel_slave.SetBackgroundColour(wx.Colour(190,190,170))
        coluna_ref_panel = wx.BoxSizer(wx.VERTICAL)
        coluna_sec_panel = wx.BoxSizer(wx.VERTICAL)   
        coluna_ref_panel.Add(self.logpanel_master, proportion=0, flag=wx.ALL, border=5)
        coluna_ref_panel.Add(texto01b1, proportion=0, flag=wx.ALL, border=5)        
        coluna_ref_panel.Add(self.textoMasterPath, proportion=0, flag=wx.ALL, border=5)        
        coluna_sec_panel.Add(self.logpanel_slave, proportion=0, flag=wx.ALL, border=5)
        coluna_sec_panel.Add(texto01b2, proportion=0, flag=wx.ALL, border=5)        
        coluna_sec_panel.Add(self.texto01b2b, proportion=0, flag=wx.ALL, border=5)        
        box_linha01b.Add(coluna_ref_panel, proportion=0, flag=wx.ALL, border=5)
        box_linha01b.Add(coluna_sec_panel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=5)

        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox1 = wx.ListBox(self, choices=["SAT POA", "SAT REG", "BARIX", "LINK DOWN"])
        box_linha02.Add(wx.StaticText(self, label='Modo de operação detectado:'), proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        box_linha02.Add(self.listbox1, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        
        self.ledErroModoOperacao =  wx.StaticText(self, wx.ID_ANY, label='', size=(20,10))
        self.ledErroModoOperacao.SetBackgroundColour('gray')
        box_linha02a = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02a.Add(self.ledErroModoOperacao, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02a.Add(wx.StaticText(self, label='Posição da botoneira'), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       
        self.ledErroInterpretaSerial =  wx.StaticText(self, wx.ID_ANY, label='', size=(20,10))
        self.ledErroInterpretaSerial.SetBackgroundColour('gray')
        box_linha02b = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02b.Add(self.ledErroInterpretaSerial, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02b.Add(wx.StaticText(self, label='Historico de interpretação dos comandos'), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       

        box_coluna02a = wx.BoxSizer(wx.VERTICAL)
        box_coluna02a.Add(box_linha02a, proportion=0, flag=wx.ALL, border=0)
        box_coluna02a.Add(box_linha02b, proportion=0, flag=wx.ALL, border=0)
        
        box_linha02.AddSpacer(50)
        box_linha02.Add(box_coluna02a, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        
        self.textoErroTimeSync = wx.StaticText(self, label='Verifique a sincronização de horário dos sistemas de referência e/ou monitorados.')
        self.textoErroTimeSync.Font = warning_font
        self.textoErroTimeSync.BackgroundColour = 'red'
        self.textoErroTimeSync.Hide()
                   
        coluna_geral.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna_geral.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna_geral.Add(box_linha02, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        coluna_geral.Add(self.textoErroTimeSync, proportion=0, flag=wx.CENTER |wx.CENTER, border=0) 
        
        self.listbox1.Bind(wx.EVT_LISTBOX, self.on_select)  #associa funcao ao botao
        
        self.SetSizer(coluna_geral)
        self.Show()

    def on_select(self, event):
        self.set_listbox_selected(self.listboxmode)
        pass
    
    def set_error_led(self, selecao='ledErroModoOperacao'):
        """Funcao que pinta o led de vermelho"""
        if selecao == 'ledErroModoOperacao':
            self.ledErroModoOperacao.SetBackgroundColour('Red')
        if selecao == 'ledErroInterpretaSerial':
            self.ledErroInterpretaSerial.SetBackgroundColour('Red')    
        self.Refresh()

    def clear_error_led(self, selecao='ledErroModoOperacao'):
        """Funcao que pinta o led de verde"""
        if selecao == 'ledErroModoOperacao':
            self.ledErroModoOperacao.SetBackgroundColour('Green')
        if selecao == 'ledErroInterpretaSerial':
            self.ledErroInterpretaSerial.SetBackgroundColour('Green')
        self.Refresh()

    def set_interface_paths(self, paths):
        """
        Funcao que seta o texto da interface que indica os paths monitorados
        Recebe uma lista no estilo [path master, path slave]
        """
        self.textoMasterPath.SetLabel(self.paths[ list(self.names.keys())[0] ].split(', ')[0])
        self.texto01b2b.SetLabel(paths[1])

    def set_listbox_selected(self, mode):
        """
        Funcao que seleciona uma opcao no listbox dos modos de operacao\n
        Recebe uma string com o nome do modo de servico. Suporta as opcoes listadas no listbox\n
        SAT POA, SAT REG, BARIX, LINK DOWN
        """
        self.listboxmode = mode
        for idx, content in enumerate(self.listbox1.GetItems()):
            if mode in content:
                self.listbox1.Select(idx)

    def adiciona_informacoes(self):
        """Funcao que atualiza o painel de informacoes do log."""
        pass
    
    def clear_content(self):
            self.logpanel_master.Clear()  
            self.logpanel_slave.Clear()

    def get_last_flag_line(self, flag, seletor='master'):
        """retorna uma lista com o conteudo da ultima linha de log com a flag ou retorna 0 em caso de erro"""
        if (seletor == 'master'):
            painel = self.logpanel_master
        elif (seletor == 'slave'):
            painel = self.logpanel_slave
        
        try:
            data_list = painel.GetValue().split('\n')  #criacao de um dicionario para armazenar os dados
            for linha in reversed(data_list):  #adicionado reversed
                if (flag in linha):  #procura pela Flag 
                    return linha.replace(" - ", "-").split('-')  #caso encontre retorna as informações da linha
            return 0
        except Exception as Err:
            print(f'Erro em get_last_flag_line: {Err}')


    def get_2last_flag_lines(self, flag, seletor='master'):
        """retorna uma lista com o conteudo da ultima linha de log com a flag ou retorna 0 em caso de erro"""
        if (seletor == 'master'):
            painel = self.logpanel_master
        elif (seletor == 'slave'):
            painel = self.logpanel_slave
        
        try:
            data_list = painel.GetValue().split('\n')  #criacao de um dicionario para armazenar os dados
            tobereturned = []
            for linha in reversed(data_list):  #adicionado reversed
                if (flag in linha):  #procura pela Flag 
                    tobereturned.append(linha.replace(" - ", "-").split('-'))
                    if ( len(tobereturned) >= 2 ):
                        return tobereturned  # retorna as informações das ultimas duas linhas
            return 0
        except Exception as Err:
            print(f'Erro em get_last_flag_line: {Err}')


class TabDisparoArquivo(wx.Panel):
    """Classe de criação de uma tab de pesquisa de arquivos antigos"""
   
    def __init__(self, parent, names, lista_paths, flag):
        super().__init__(parent=parent) 
        self.FLAG = flag
        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel
        self.lista_paths = lista_paths
        self.names = names
        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        self.textoMasterPath = wx.StaticText(self, label="Selecione a praça para buscar o arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_master = wx.TextCtrl(self, value='Sem informações de disparo para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        self.texto01b2b = wx.StaticText(self, label="Selecione a praça para buscar o arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_slave = wx.TextCtrl(self, value='Sem informações de disparo para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_slave.SetBackgroundColour(wx.Colour(190,190,170))
        list_choices = list(names.values())
        self.listbox1 = wx.ListBox(self, choices=list_choices)
        self.filepick01 = wx.FilePickerCtrl(self, path="", wildcard="COMM*",
               message="Selecione o arquivo de log", size=(390,25), style=wx.FLP_USE_TEXTCTRL)
        self.listbox2 = wx.ListBox(self, choices=list_choices)
        self.filepick02 = wx.FilePickerCtrl(self, path="", wildcard="COMM*",
               message="Selecione o arquivo de log", size=(390,25), style=wx.FLP_USE_TEXTCTRL)
        
        coluna01a = wx.BoxSizer(wx.VERTICAL)
        coluna01b = wx.BoxSizer(wx.VERTICAL)   
        coluna01a.Add(self.logpanel_master, proportion=0, flag=wx.ALL, border=5)
        coluna01a.Add(self.textoMasterPath, proportion=0, flag=wx.ALL, border=5)        
        coluna01a.Add(self.listbox1, proportion=0, flag=wx.ALL | wx.CENTER, border=5)        
        coluna01a.Add(self.filepick01, proportion=0, flag=wx.ALL | wx.CENTER, border=30)

        coluna01b.Add(self.logpanel_slave, proportion=0, flag=wx.ALL, border=5)
        coluna01b.Add(self.texto01b2b, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.listbox2, proportion=0, flag=wx.ALL | wx.CENTER, border=5)        
        coluna01b.Add(self.filepick02, proportion=0, flag=wx.ALL | wx.CENTER, border=30)

        box_linha01b.Add(coluna01a, proportion=0, flag=wx.ALL, border=5)
        box_linha01b.Add(coluna01b, proportion=0, flag=wx.ALL, border=5)

        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
                   
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        
        self.listbox1.Bind(wx.EVT_LISTBOX, lambda event: self.on_select(event, 'listbox1'))  #associa funcao ao botao
        self.listbox2.Bind(wx.EVT_LISTBOX, lambda event: self.on_select(event, 'listbox2'))  #associa funcao ao botao
        self.filepick01.Bind(wx.EVT_FILEPICKER_CHANGED, lambda event: self.on_open(event, 'filepick01'))  #associa funcao ao botao
        self.filepick02.Bind(wx.EVT_FILEPICKER_CHANGED, lambda event: self.on_open(event, 'filepick02'))  #associa funcao ao botao
        self.SetSizer(coluna)
        self.Show()
    
    def on_select(self, event, selecao):
        if selecao == 'listbox1':
            listbox = self.listbox1
            filepick = self.filepick01

        elif selecao == 'listbox2':
            listbox = self.listbox2
            filepick = self.filepick02
        
        text = listbox.GetStringSelection()
        for item in self.names:
            if (self.names[item] == text):
                filepick.Path = os.path.join(self.lista_paths[item].split(', ')[0], '') 
                break
            else:
                filepick.Path = os.path.join(self.lista_paths[ list(self.lista_paths.keys())[0] ].split(', ')[0], '') #se nao for nenhuma anterior entao é cabeça de rede

    def on_open(self, event, selecao):
        parser_ = WRFileParse()
        if (selecao == 'filepick01'):    
            filepick = self.filepick01
            self.textoMasterPath.SetLabel(filepick.Path)
            self.logpanel_master.Clear()  
            seletor = 'master'
            
        elif (selecao == 'filepick02'):
            filepick = self.filepick02
            self.texto01b2b.SetLabel(filepick.Path)
            self.logpanel_slave.Clear()  
            seletor = 'slave'
        conteudo = parser_.get_conteudo_log(filepick.Path)
        self.adiciona_informacoes(conteudo, self.FLAG, seletor)
        
    def adiciona_informacoes(self, conteudo, selecao='master'):
        """Funcao que atualiza o painel de informacoes do log. \n"""
        pass

    def clear_content(self):
        self.logpanel_master.SetLabel('Sem informações de disparo para exibir')  
        self.logpanel_slave.SetLabel('Sem informações de disparo para exibir')
        self.textoMasterPath.SetLabel("Selecione a praça para buscar o arquivo")
        self.texto01b2b.SetLabel("Selecione a praça para buscar o arquivo")
        self.filepick01.SetPath("")
        self.filepick02.SetPath("")
        self.listbox1.Selection = -1
        self.listbox2.Selection = -1


class TabComercial(wx.Panel):
    """Classe de criação de uma tab de pesquisa de arquivos antigos"""
   
    def __init__(self, parent, names, lista_paths, flag):
        panel_font = wx.Font(wx.FontInfo(8))
        super().__init__(parent=parent) 
        coluna_geral = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel
        self.lista_paths = lista_paths
        self.names = names
        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        texto_playlist = wx.StaticText(self, label='Playlist', style=wx.ALIGN_CENTER, size=(-1,-1))
        texto_exibido = wx.StaticText(self, label='Comprovantes', style=wx.ALIGN_CENTER, size=(-1,-1))
        self.panel_playlist = wx.TextCtrl(self, value='Sem informações para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL, size=(370,420))  #cria um edit
        self.panel_playlist.SetBackgroundColour(wx.Colour(190,190,170))
        self.panel_exibido = wx.TextCtrl(self, value='Sem informações para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL, size=(480,420))  #cria um edit
        self.panel_exibido.SetBackgroundColour(wx.Colour(190,190,170))
        self.panel_exibido.SetFont(panel_font)
        texto_disparo = wx.StaticText(self, label='Disparos', style=wx.ALIGN_CENTER, size=(-1,-1))
        self.panel_disparo = wx.TextCtrl(self, value='Sem informações para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL, size=(370,420))  #cria um edit
        self.panel_disparo.SetBackgroundColour(wx.Colour(190,190,170))
        list_choices = list(names.values())
        self.listbox1 = wx.ListBox(self, choices=list_choices, size=(-1, -1))
        
        coluna01a = wx.BoxSizer(wx.VERTICAL)
        coluna01b = wx.BoxSizer(wx.VERTICAL)   
        coluna01c = wx.BoxSizer(wx.VERTICAL)   
        coluna01a.Add(texto_playlist, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=5)        
        coluna01a.Add(self.panel_playlist, proportion=0, flag=wx.ALL, border=0)
        
        coluna01b.Add(texto_disparo, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=5)        
        coluna01b.Add(self.panel_disparo, proportion=0, flag=wx.ALL, border=0)
        
        coluna01c.Add(texto_exibido, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=5)        
        coluna01c.Add(self.panel_exibido, proportion=0, flag=wx.ALL, border=0)
        
        box_linha01b.Add(coluna01a, proportion=0, flag=wx.TOP, border=5)
        box_linha01b.Add(coluna01b, proportion=0, flag=wx.TOP, border=5)
        box_linha01b.Add(coluna01c, proportion=0, flag=wx.TOP, border=5)

        self.timepicker1 = wx.adv.TimePickerCtrl(self)
        self.timepicker1.SetTime(0, 0, 0)
        self.timepicker2 = wx.adv.TimePickerCtrl(self)
        self.timepicker2.SetTime(23,59,00)
        self.filterbutton = wx.Button(self, label='Consultar')

        self.calendar = wx.adv.CalendarCtrl(self)

        linha_selecao_praca = wx.BoxSizer(wx.HORIZONTAL)
        linha_selecao_praca.Add(wx.StaticText(self, label="Praça: ", style=wx.ALIGN_CENTER, size=(-1,-1)), proportion=0, flag=wx.ALL, border=5)
        linha_selecao_praca.Add(self.listbox1, proportion=0, flag=wx.ALL, border=5)
        linha_selecao_praca.AddSpacer(20)
        linha_selecao_praca.Add(wx.StaticText(self, label="Data: ", style=wx.ALIGN_CENTER, size=(-1,-1)), proportion=0, flag=wx.ALL, border=5)
        linha_selecao_praca.Add(self.calendar)
        linha_selecao_praca.AddSpacer(20)
        linha_selecao_praca.Add(wx.StaticText(self, label="Horário de inicio e fim: ", style=wx.ALIGN_CENTER, size=(-1,-1)), proportion=0, flag=wx.TOP, border=15)
        linha_selecao_praca.Add(self.timepicker1, flag=wx.ALL, border=10)
        linha_selecao_praca.Add(wx.StaticText(self, label='-', style=wx.ALIGN_CENTER), flag=wx.TOP, border=15)
        linha_selecao_praca.Add(self.timepicker2, flag=wx.ALL, border=10)
        linha_selecao_praca.AddSpacer(30)
        linha_selecao_praca.Add(self.filterbutton, flag=wx.ALL, border=10)
        linha_selecao_praca.AddSpacer(10)
        

        coluna_geral.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna_geral.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna_geral.AddSpacer(10)
        coluna_geral.Add(linha_selecao_praca, flag=wx.ALIGN_CENTER, border=5)        
        
        
        self.filterbutton.Bind(wx.EVT_BUTTON, self.onFilter)

        self.panel_disparo.SetFont(panel_font)
        self.panel_exibido.SetFont(panel_font)
        self.panel_playlist.SetFont(panel_font)
        self.SetSizer(coluna_geral)        
        self.Show()

    def onFilter(self, event):
        self.on_open(None)
      
    def on_open(self, event):
        parser_ = WRFileParse()
        self.panel_playlist.Clear()  
        self.panel_disparo.Clear()  
        self.panel_exibido.Clear()  

        data = str(self.calendar.Date).split()[0].split('/')
      
        text = self.listbox1.GetStringSelection()
        if (len(text) == 0):
            wx.MessageBox("Selecione uma praça antes de tentar realizar a consulta", "Atenção!")
            return

        for item in self.names:
            if (self.names[item] == text):
                playlist_filepath = os.path.join(self.lista_paths[item].split(', ')[1], f'{data[1]}{data[0]}.pl1') 
                disparo_filepath = os.path.join(self.lista_paths[item].split(', ')[0], f'Comm_{data[2]}_{data[1]}_{data[0]}.txt') 
                exibido_filepath = os.path.join(self.lista_paths[item].split(', ')[2], f'{data[2]}{data[1]}{data[0]}WRC.LOG') 
                break
                
        conteudo_playlist = parser_.get_conteudo_log(playlist_filepath)
        conteudo_disparo = parser_.get_conteudo_log(disparo_filepath)
        conteudo_exibido = parser_.get_conteudo_log(exibido_filepath)
  
        if (conteudo_playlist != 0 and conteudo_exibido != 0 and conteudo_disparo != 0):
            self.adiciona_informacoes(conteudo_playlist, 'playlist')      
            self.adiciona_informacoes(conteudo_disparo, 'disparo')
            self.adiciona_informacoes(conteudo_exibido, 'exibido')
        else:
            wx.MessageBox(f"Um ou mais arquivos não foram encontrados, verifique a existencia ou tente novamente mais tarde.\
            \n{playlist_filepath} \n{disparo_filepath} \n{exibido_filepath}", "File not found")

        
        
    def adiciona_informacoes(self, conteudo, selecao):
        """Funcao que acrescenta dados aos paineis de informacoes da tab,
        retorna uma flag que indica se existem erros nos dados adicionados"""
        filtro_inicio = str(self.timepicker1.GetValue())[-8:-3]
        filtro_fim = str(self.timepicker2.GetValue())[-8:-3]
        

        if selecao == 'playlist':
            painel = self.panel_playlist    

        elif selecao == 'disparo':
            painel = self.panel_disparo
        
        elif selecao == 'exibido':
            painel = self.panel_exibido

        else:
            raise(NameError, 'parametro incorreto em adiciona informacoes')
        filtrar = True
        for _, linha in enumerate(conteudo):
            linha2 = linha.replace('-',' ')
            horario_bloco = linha2.split(' ')
            for item in horario_bloco:
                if ('>' in item):
                    continue
                if (':' in item[:5]):
                    timeinicio = int(filtro_inicio.replace(':', ''))
                    timefim = int(filtro_fim.replace(':', ''))
                    timelinha = int(item[:5].replace(':', ''))
                    if (timelinha >= timeinicio):
                        filtrar = False
                    if (timelinha >= timefim):
                        filtrar = True
            
            if (filtrar):
                continue

                    
            if ('.mp3' in linha or 'Serial' in linha):
                estilo = 1 #branco
            
            elif ('BREAK COMERCIAL' in linha or 'Thread' in linha or 'filtrado' in linha.lower() or 'LOAD PLAYLIST' in linha):
                estilo = 2 #vermelho

            else:
                estilo = 3 #cinza

            if (estilo == 1):    #alterar
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.WHITE))
            elif (estilo == 2):        #alterar 
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.RED))
            else:
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
            
            if (linha not in painel.GetValue()):
                painel.AppendText(f'{linha}')
        return 0   

    def clear_content(self):
        self.panel_playlist.SetLabel('Sem informações para exibir')  
        self.panel_disparo.SetLabel('Sem informações para exibir')
        self.panel_exibido.SetLabel('Sem informações para exibir')
        self.listbox1.Selection = -1
      

class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia no tray do sistema
    """
    def __init__(self, prog_name, frame, tabs_dict, names):
        """
        Funcao que inicializa o tray do sistema \n  
        """
        self.frame = frame
        self.tabs_dict = tabs_dict
        self.names = names
        super(TaskBarIcon, self).__init__()
        
        self.TRAY_TOOLTIP = prog_name
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        task_icon = os.path.join(ROOT_DIR, 'task_icon.png')          
        self.SetIcon(wx.Icon(task_icon), self.TRAY_TOOLTIP)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down) #funcao que define o metodo de clique esquerdo no trayicon

    def create_menu_item(self, menu, label, func):
            item = wx.MenuItem(menu, -1, label)
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
            menu.Append(item)
            return item

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for name in self.tabs_dict.keys():
            # definindo metodos para cada submenu criado, funcao lambda permite enviar parametros especificos para cada submenu
            if name in self.names.keys():   #verifica se essa tab é do arquivo de configuracoes ou se é uma tab fixa
              self.create_menu_item(menu, f'View {self.names[name]}', lambda evt, temp=name: self.on_right_down(evt, temp))      

        menu.AppendSeparator()
        self.create_menu_item(menu, f'Analisar Disparos', lambda evt, temp='disparos_dual_tab': self.on_right_down(evt, temp))      
        self.create_menu_item(menu, f'Analisar Comprovantes', lambda evt, temp='exibicao_tripla_tab': self.on_right_down(evt, temp))      
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Fechar a aplicação', self.on_exit) #on exit program clique
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Sobre', self.on_get_info) #apresentacao de informacoes sobre o desenvolvedor
        return menu

    def on_left_down(self, event): 
        """
        Metodo executado ao clicar com o botao esquerdo
        """
        self.frame.Show()
        self.frame.Raise()
        #self.frame.notebook.SetSelection(1)  #seleciona a tab selecionada
      
    def on_right_down(self, event, tab):
        """
        Metodo executado ao clicar com o botao direito em submenus\n
        button_label recebe a tab especifica de cada submenu 
        """
        self.frame.Show()
        for idx, tab_name in enumerate(self.tabs_dict.keys()):
            if tab_name == tab:
                self.frame.notebook.SetSelection(idx)  #seleciona a tab selecionada 
      
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def on_get_info(self, event):
        wx.MessageBox("Feito por Cristian Ritter para NSC TV", 'Sobre o aplicativo')


class MyFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
    #----------------------------------------------------------------------
    def __init__(self, prog_name, tabs, names, paths, flag):
        """Constructor"""     
        super().__init__(None, style=wx.CAPTION | wx.FRAME_TOOL_WINDOW, 
                          title=prog_name,
                          size=(1280,760)
                          ) 
           
        self.Centre()    #centraliza a janela    
        panel = wx.Panel(self)      #cria um painel
        notebook = wx.Notebook(panel)    #cria um caderno de abas
        self.tabs = tabs    #armazena as abas criadas na variavel tabs
        self.notebook = notebook
        for idx, nome in enumerate(names):
            if idx == 0:
                continue
            self.tabs[nome] = TabDisparoPraca(notebook, names, paths)
            notebook.AddPage(self.tabs[nome], names[nome])
        self.tabs['disparos_dual_tab'] = TabDisparoArquivo(notebook, names=names, lista_paths=paths, flag=flag)
        notebook.AddPage(self.tabs['disparos_dual_tab'], "Análise Histórica - Disparos")
        self.tabs['exibicao_tripla_tab'] = TabComercial(notebook, names=names, lista_paths=paths, flag=flag)
        notebook.AddPage(self.tabs['exibicao_tripla_tab'], "Análise Histórica - Comprovantes")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, proportion=0, flag=wx.ALL, border=5)
        hide_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
        sizer.Add(hide_bt, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        hide_bt.Bind(wx.EVT_BUTTON, self.on_press)  #associa funcao ao botao

        panel.SetSizer(sizer)
        self.Layout()     
        self.Show()

    def on_press(self, event):
        """Funcao executada ao pressionar o botao Esconder"""
        self.tabs['disparos_dual_tab'].clear_content()
        self.tabs['exibicao_tripla_tab'].clear_content()
        self.Hide()      

TabDisparoPraca.adiciona_informacoes = adiciona_informacoes
TabDisparoArquivo.adiciona_informacoes = adiciona_informacoes

if __name__ == '__main__':
    """
    Este trecho do código permite testar a biblioteca individualmente e fornece também exemplos de uso.
    """
    app = wx.App(useBestVisual=True)

    names = {'praca01': 'WINRADIO ATL BLU', 'praca02': 'WINRADIO ATL CHA', 'praca03': 'WINRADIO ATL CRI', 'praca04': 'WINRADIO ATL JOI', 'praca05': 'WINRADIO BKP'}
    paths = {'praca01': 'C:\\, C:\\', 'praca02': 'C:\\, C:\\', 'praca03': 'C:\\, C:\\', 'praca04': 'C:\\, C:\\', 'praca05': 'C:\\, C:\\'}
    tabs_dict = {}
    frame = MyFrame(prog_name="WR LogWatcher", tabs=tabs_dict, names=names, paths=paths, flag="Received")  #criacao do frame recebe o nome da janela
    
    frame_names = {'nome_do_perfil' : 'apelido'}
    frames_dict = {'nome_do_perfil' :frame}
    TaskBarIcon("WR LogWatcher - ATL_JOI", frame, tabs_dict, names)

    app.MainLoop()
