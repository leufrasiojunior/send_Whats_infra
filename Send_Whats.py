from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
import os, random, atexit, string, pywhatkit, shutil, customtkinter, sys, datetime
import pandas as pd
import logging


def configure_logger(file_name, level=logging.INFO):
    logging.basicConfig(level=level)
    logger = logging.getLogger(file_name)
    file_handler = logging.FileHandler("logs/" + file_name + '.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

my_logger = configure_logger('log', level=logging.INFO)
my_logger.info('Program Started!')

text_pgto = "configs/text_pgto.txt"
arq_os = "configs/text_os.txt"
arq_conf = "configs/send_whats.conf"
qtdNomes = 0

folder_path = 'configs/'
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
current_apre = datetime.datetime.now().strftime('%H')

customtkinter.set_appearance_mode("light")
app = customtkinter.CTk()
app.geometry("550x250")
app.title("Send Whats")
app.resizable(False, False)

def delete_files_on_exit(folder_path):
    file_list = os.listdir(folder_path)
    if (len(file_list) == 0):
        my_logger.info('No files do remove in upload folder.')
    else:
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                try:
                    my_logger.info(f'File {file_path} Removed')
                    os.remove(file_path)
                    my_logger.info('Program finished')
                    
                except Exception as e:
                    my_logger.info(f"Error removing {file_path} %s", str(e))
                    
folder_path = 'upload/'
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
atexit.register(delete_files_on_exit, folder_path)

def generate_bases():
    try:
        xlsx_personalizado = filedialog.asksaveasfilename(
            filetypes=[("Arquivos do Xlsx do Excel", ".xlsx")],
            defaultextension=".xlsx",
            initialfile="Base_Exemplo.xlsx",
            confirmoverwrite=False,
            title='Salvar base de Exemplo')
        if xlsx_personalizado == '':
            messagebox.showerror("Operação cancelada!", "Solicitação cancelada!")
            my_logger.info('The process to save the example file has been canceled.')
        else:
            columns=['Nome','Telefone','Proposta']
            names =  ['Nome 1','Nome 2','Nome 3','Nome 4', 'Nome 5']
            teles = ['+5511900000000','+5511900000001','+5511900000002','+5511900000003','+5511900000004']
            propostas  = [800123,800235,800,1,2]
            #
            df = pd.DataFrame(list(zip(names,teles,propostas)), columns=columns)
            df.to_excel(xlsx_personalizado, index = False)
            messagebox.showinfo("Arquivo salvo", "Arquivo salvo em " + xlsx_personalizado)
        my_logger.info('File example saved {xlsx_personalizado} ')      
    except Exception as SE:
            messagebox.showerror("Arquivo não salvo!", "Falha no processo para salvar o arquivo de exemplo em " + xlsx_personalizado)
            my_logger.warning(f'error when saving file to folder {xlsx_personalizado} %s', str(SE))
        
def generate_random_name(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def btnyes():
    messagebox.showinfo("Certo!", "Agora você pode voltar para enviar as mensagens.")
    windowPerson.destroy()
    configWindow.destroy()
    app.deiconify()


def btnno():
    messagebox.showinfo(
        "Certo!",
        "Reveja os valores do arquivo de texto. Lebre-se de trocar o nome para {nomes}.\nEste script somente envia textos com um nome.",
    )

def text_os():
    try:
        text_file = open(arq_os, "w", encoding="utf-8")
        text_file.write(osBox.get(1.0, END))
        text_file.close()

        text_file = open(text_pgto, "w", encoding="utf-8")
        text_file.write(textPgto.get(1.0, END),)
        my_logger.info('New OS or Payment messages have changed.')
        
        text_file.close()
        configWindow.destroy()
        app.deiconify()
    except Exception as TG:
        my_logger.critical(f'Error to save text files to config. %s', str(TG))
        messagebox.showerror("Erro ao salvar!", "Falha no processo para salvar a configuração!: " + str(TG))

def texto_personalizado():
    my_logger.info('Process to upload a custom message started.')
    apre = "Bom dia"
    nomes = ["Nome 1"]
    txt_personalizado = filedialog.askopenfilename(
        filetypes=[("Carregar texto personalizado", "*.txt")])
    
    if txt_personalizado:
        global new_file_path
        global folder_destiny
        folder_destiny = "upload/"
        new_file_name = generate_random_name() + '.txt'
        new_file_path = new_file_name
        folder_desti = f"{folder_destiny}/{new_file_path}"
        shutil.copy2(txt_personalizado, folder_desti)
    file_personalized = folder_desti
    
    with open(file_personalized, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    try:
        for nome in nomes:
            conteudo_interpretado = conteudo.format(apre=apre, nomes=nome)
            global windowPerson
            windowPerson = customtkinter.CTkToplevel(app)
            windowPerson.geometry("1500x250")
            windowPerson.title("Texto Personalizado. Teste de visualização")
            windowPerson.resizable(True, True)
            lblPerson = customtkinter.CTkLabel(
                windowPerson, 
                text=conteudo_interpretado, 
                font=("", 20), 
                justify="center")
            lblPerson.place(relx=0.1, rely=0.5, anchor="nw")
            lblyesno = customtkinter.CTkLabel(
                windowPerson,
                text="Está aparecendo todos os nomes normalmente?",
                font=("", 20),
                justify="center",
            )
            lblyesno.place(relx=0.1, rely=0.1, anchor="nw")
            btnYes = customtkinter.CTkButton(windowPerson, 
                                            text="Sim", 
                                            command=btnyes).place(relx=0.2, rely=0.2)

            btnNo = customtkinter.CTkButton(windowPerson, 
                                            text="Não", 
                                            command=btnno).place(relx=0.4, rely=0.2
            )
    except Exception as TP:
        my_logger.error(f'Error loading custom file. Check the variable: %s', str(TP))
        messagebox.showerror("Erro ao carregar o arquivo?!", "Falha no processo para carregar o arquivo! Verifique a variável" + str(TP))
            
def save_config():
    file_conf = open(arq_conf, "w", encoding="utf-8")
    time = close_config.get(1.0, END)
    tab = time_config.get(1.0, END)
    saveConf = {
    "time_send": tab,
    "time_close_tab": time
}
    for name, value in saveConf.items():
        file_conf.write(f"{name}={value}")
    file_conf.close()
    app.withdraw()
    save.destroy()
    app.deiconify()
def config():
    with open(arq_conf, "r", encoding="utf-8") as config:
        vars = config.read()
    linhas = vars.split("\n")
    list_vars = {}
    for linha in linhas:
        if "=" in linha:
            nome, valor = linha.split("=")
            list_vars[nome.strip()] = valor.strip()

    time_send = int(list_vars["time_send"])
    time_close_tab = int(list_vars["time_close_tab"])
    app.withdraw()
    def closeapp():
        config.destroy()
        app.deiconify()
    config = customtkinter.CTkToplevel(app)
    global save
    save = config
    config.protocol("WM_DELETE_WINDOW", closeapp)
    config.title("Configuração do Programa")
    config.geometry("700x180")
    config.resizable(False, False)

    aviso = customtkinter.CTkLabel(config, text="Configure os tempos para a aplicação funcionar antes de enviar a mensagem e a próxima mensagem.\nSempre com o tempo em segundos.", justify="center")
    
    aviso.pack()
    aviso.place(x=60, y=2)
    
    label = customtkinter.CTkLabel(config, 
                                   text="Tempo para aguardar o envio de mensagens.", 
                                   justify="center")
    
    label.pack()
    label.place(x=80, y=40)
    global time_config
    global close_config
    time_config = customtkinter.CTkTextbox(
        config,
        width=50,
        height=20,
        fg_color="#D3D3D3",
        text_color="black",
        border_spacing=5,
        border_color="black",
        border_width=3,
        corner_radius=10,
        font=("", 20)
    )

    time_config.pack()
    time_config.place(x=190, y=65)

    ###---

    lbl_close_tab = customtkinter.CTkLabel(config, text="Tempo para enviar a próxima mensagem", justify="center")
    lbl_close_tab.pack()
    lbl_close_tab.place(x=380, y=40)
    close_config = customtkinter.CTkTextbox(
        config,
        width=50,
        height=20,
        fg_color="#D3D3D3",
        text_color="black",
        border_spacing=5,
        border_color="black",
        border_width=3,
        corner_radius=10,
        font=("", 20))
    
    close_config.pack()
    close_config.place(x=480, y=65)
    save_img = customtkinter.CTkImage(Image.open("images/salvar-arquivo.png"))
    btnConfig = customtkinter.CTkButton(
        config, text="Salvar", 
        command=save_config, 
        image=save_img
    ).place(x=300, y=130)
    #Tempo  envio e mensagens
    time_config.insert("0.0", time_send)
    #tempo fechar aba e enviar prox msg
    close_config.insert("0.0", time_close_tab)

def load_base():
    load_file = customtkinter.CTkToplevel(app)
    app.withdraw()
    def closeapp():
        app.deiconify()
    load_file.protocol("WM_DELETE_WINDOW", closeapp)
    caminho_arquivo = filedialog.askopenfilename(filetypes=[('Arquivos do Excel', '*.xlsx')])
    
    if caminho_arquivo:
        pasta_destino = 'upload/'
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        nome_arquivo = caminho_arquivo.split('/')[-1]
        caminho_destino = f'{pasta_destino}/{nome_arquivo}'
        shutil.copy2(caminho_arquivo, caminho_destino)
        # print(f"Arquivo salvo em: {caminho_destino}")
    else:
        CTkMessagebox(title="Base não selecionada", 
                      message="Nenhuma base carregada.")
    
    load_file.destroy()
    app.deiconify()

    global nomes, qtdNomes, data_frame
    data_frame = pd.read_excel(f"{caminho_destino}")
    nomes = (data_frame['Nome'].tolist())
    qtdNomes = len(nomes)


    if qtdNomes > 0:
        customtkinter.CTkLabel(app, 
                                       text=f"Nomes a processar: {qtdNomes}                           ", fg_color="#DBDBDB").place(x=225, y=50)
def config_button():
    global configWindow
    app.withdraw()
    def ao_fechar_segunda_janela():
        configWindow.destroy()
        app.deiconify()
    configWindow = customtkinter.CTkToplevel(app)
    configWindow.protocol("WM_DELETE_WINDOW", ao_fechar_segunda_janela)
    configWindow.title("Configuração de Texto")
    configWindow.geometry("800x350")
    configWindow.resizable(False, False)
    # ---#
    label = customtkinter.CTkLabel(configWindow, 
                                   text="Texto de Aguardando Pagamento")
    
    label.pack()
    label.place(x=25, y=8)
    global textPgto
    textPgto = customtkinter.CTkTextbox(
        configWindow,
        width=375,
        height=255,
        fg_color="#D3D3D3",
        text_color="black",
        border_spacing=5,
        border_color="black",
        border_width=3,
        corner_radius=10,
    )
    textPgto.pack()
    textPgto.place(x=20, y=30)
    nome_arquivo = "configs/text_pgto.txt"
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    textPgto.insert("0.0", conteudo)
    global osBox
    labelOs = customtkinter.CTkLabel(configWindow, text="Texto de O.S")
    osBox = customtkinter.CTkTextbox(
        configWindow,
        width=375,
        height=255,
        fg_color="#D3D3D3",
        text_color="black",
        border_spacing=5,
        border_color="black",
        border_width=3,
        corner_radius=10,
    )
    labelOs.pack()
    osBox.pack()
    osBox.place(x=405, y=30)
    labelOs.place(x=410, y=8)

    with open(arq_os, "r", encoding="utf-8") as file_os:
        conteudo_os = file_os.read()
    osBox.insert("0.0", conteudo_os)
    global btnSave
    btnSave = customtkinter.CTkButton(
        configWindow, 
        text="Salvar configurações",
          command=text_os
    ).place(x=150, y=300)

    btnConfig = customtkinter.CTkButton(
        configWindow, 
        text="Carregar texto personalizado", 
        command=texto_personalizado
    ).place(x=500, y=300)

def selection():
    t = 0
    if int(current_apre) < 12:
        apre = "Bom dia"
    elif int(current_apre) >= 12 and int(current_apre) <= 18:
        apre = "Boa tarde"
    else:
        apre = "Boa noite"
    optSelect = str(radio.get())

    #Ler o conteúdo dos tempos
    with open(arq_conf, "r", encoding="utf-8") as config:
        vars = config.read()
    lines = vars.split("\n")
    list_vars = {}
    for linha in lines:
        if "=" in linha:
            nome, valor = linha.split("=")
            list_vars[nome.strip()] = valor.strip()

    send_messages = int(list_vars["time_send"])
    close_tab = int(list_vars["time_close_tab"])

    if optSelect == str(1):
        try:
            name = (data_frame['Nome'].tolist())
            tels = (data_frame['Telefone'].tolist())
            props = (data_frame['Proposta'].tolist())
            text_file = open(text_pgto, "r", encoding="utf-8")
            conteudo = text_file.read()
        except:
            CTkMessagebox(title="Base com erros!", 
    message="Verifique os títulos da base gerada. Caso tenha dúvidas, gere uma nova base no local correspondente, e tente novamente.", 
    icon="cancel", 
    option_1="OK",
    width=500, 
    height=200, 
    border_color="white", 
    corner_radius=10, 
    justify="center")
            return False
        for nome, prop in zip(name, props):
            texto_formatado = conteudo.format(apre=apre, nomes=nome, props=prop)
            pywhatkit.sendwhatmsg_instantly("+"+str(tels[t]), texto_formatado, send_messages, True, close_tab)
            t = t +1
    elif optSelect == str(2):
        try:
            name = (data_frame['Nome'].tolist())
            tels = (data_frame['Telefone'].tolist())
            props = (data_frame['Proposta'].tolist())
        except:
            CTkMessagebox(title="Base com erros!", 
    message="Verifique os títulos da base gerada. Caso tenha dúvidas, gere uma nova base no local correspondente, e tente novamente.", 
    icon="cancel", 
    option_1="OK",
    width=500, 
    height=200, 
    border_color="white", 
    corner_radius=10, 
    justify="center")
            return False
        text_file = open(arq_os, "r", encoding="utf-8")
        conteudo = text_file.read()
        for nome, prop in zip(name, props):
            texto_os = conteudo.format(apre=apre, nomes=nome, props=prop)
            pywhatkit.sendwhatmsg_instantly("+"+str(tels[t]), texto_os, send_messages, True, close_tab)
            t = t +1
    elif optSelect == str(3):
        try:
            name = (data_frame['Nome'].tolist())
            tels = (data_frame['Telefone'].tolist())
        except:
            CTkMessagebox(title="Base com erros!", 
    message="Verifique os títulos da base gerada. Caso tenha dúvidas, gere uma nova base no local correspondente, e tente novamente.", 
    icon="cancel", 
    option_1="OK",
    width=500, 
    height=200, 
    border_color="white", 
    corner_radius=10, 
    justify="center")
            return False
        questbases.destroy()
        text_file = open(f"{folder_destiny}{new_file_path}", "r", encoding="utf-8")
        person_text = text_file.read()
        for nome in name:
            texto_os = person_text.format(apre=apre, nomes=nome)
            pywhatkit.sendwhatmsg_instantly("+"+str(tels[t]), texto_os, send_messages, True, close_tab)
            t = t +1
        print (t)
        print (qtdNomes)
        if int(t) == int(qtdNomes):
            messagebox.showinfo("Finalizado!", "Foram processados " + str(qtdNomes) + "Telefones")

        

def questBases():
    global questbases
    questbases = customtkinter.CTkToplevel(app)
    questbases.title("Qual base está tentando enviar?")
    questbases.geometry("660x150")
    questbases.resizable(False, False)
    global radio
    radio = IntVar()
    r1 = customtkinter.CTkRadioButton(questbases, text="Aguardando Pagamento", variable=radio, value=1).place(x=80, y=35)

    r2 = customtkinter.CTkRadioButton(questbases, text="        O.S         ", variable=radio, value=2).place(x=270, y=35)

    r3 = customtkinter.CTkRadioButton(questbases, text="Texto Customizado   ", variable=radio, value=3).place(x=400, y=35)

    customtkinter.CTkButton(
    questbases, 
    text="Processar Telefones", 
    command=selection, 
    fg_color="#545455", 
    text_color="white"
).place(x=275, y=75)

def send_messages():
    if qtdNomes == 0:
        CTkMessagebox(title="Base ainda não carregada", 
    message="Você ainda não carregou nenhuma base para o sistema. Clique em OK para carregar agora.", 
    icon="warning", 
    option_1="Sair e carregar a base.",
    width=500, 
    height=200, 
    border_color="white", 
    corner_radius=10, 
    justify="center")
        load_base()
    else:
        confirmMessage = CTkMessagebox(title="Atenção no envio!", 
    message="Não use em nenhum momento o PC.\nO Whatsapp Web terá que ser logado primeiro. Clique em continuar para iniciar o processo, ou cancelar para sair.", 
    icon="warning", 
    option_1="Continuar", 
    option_2="Sair", 
    width=500, 
    height=200, 
    border_color="white", 
    fade_in_duration=5, 
    corner_radius=10, 
    justify="center")
        response = confirmMessage.get()
        if response == "Continuar":
            questBases()
        else:
            return False


img_exa = customtkinter.CTkImage(Image.open("images/assets/logo.png"), size=(100,130))

frameimg = customtkinter.CTkFrame(
    app,
    width=150,
    height=150,
    border_color="black",
    border_width=1,
    corner_radius=20,
).place(x=40, y=45)

image_label = customtkinter.CTkLabel(app, image=img_exa, text="", corner_radius=8).place(x=55, y=53)

frameform = customtkinter.CTkFrame(
    app, 
    width=300, 
    height=150, 
    border_color="black", 
    border_width=1, 
    corner_radius=8,
).place(x=210, y=45)

label = customtkinter.CTkLabel(app, 
                               text="Nenhuma base selecionada ainda.", fg_color="#DBDBDB").place(x=225, y=50)
app.update()

btnConfig = customtkinter.CTkButton(
    app, 
    text="Configurar Textos", 
    command=config_button, 
    fg_color="#545455", 
    text_color="white"
).place(x=400, y=5)

upload_img = customtkinter.CTkImage(Image.open("images/upload.png"))
send_img = customtkinter.CTkImage(Image.open("images/send.png"))

btnSend = customtkinter.CTkButton(
    app, 
    text="Enviar Mensagens!", 
    command=send_messages,
    image=send_img
).place(x=95, y=210)

btnload = customtkinter.CTkButton(
    app, 
    text="Carregar base", 
    command=load_base, 
    image=upload_img
).place(x=295, y=210)

img_exa = customtkinter.CTkImage(Image.open("images/assets/excel.png"))

example_base = customtkinter.CTkButton(
    app, 
    text="Gerar base de Exemplo", 
    command=generate_bases, 
    image=img_exa
).place(x=150, y=5)

img_config = customtkinter.CTkImage(Image.open("images/config.png"))

btnconfig = customtkinter.CTkButton(
    app, text="", 
    command=config, 
    image=img_config, 
    height=20, 
    width=20).place(x=5, y=5)

app.mainloop()
