import customtkinter
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
from CTkMessagebox import CTkMessagebox
import os
import pandas as pd


text_pgto = "configs/text_pgto.txt"
arq_os = "configs/text_os.txt"
arq_conf = "configs/send_whats.conf"
# qtdNomes = 0

customtkinter.set_appearance_mode("light")
app = customtkinter.CTk()
app.geometry("550x250")
app.title("Send Whats")
app.resizable(False, False)


def btnyes():
    messagebox.showinfo("Certo!", "Certo! Os nomes serão processados agora.")


def btnno():
    messagebox.showinfo(
        "Certo!",
        "Reveja os valores do arquivo de texto. Lebre-se de trocar o nome para {nomes}.\nEste script somente envia textos com um nome.",
    )

def text_os():
    text_file = open(arq_os, "w", encoding="utf-8")
    text_file.write(osBox.get(1.0, END))
    text_file.close()

    text_file = open(text_pgto, "w", encoding="utf-8")
    text_file.write(textPgto.get(1.0, END),)
    text_file.close()

def texto_personalizado():
    apre = "Bom dia"
    nomes = ["Nome 1", "Nome 2"]
    txt_personalizado = filedialog.askopenfilename(
        filetypes=[("Carregar texto personalizado", "*.txt")]
    )
    if txt_personalizado:
        folder_destiny = "upload/"
        filename_person = txt_personalizado.split("/")[-1]
        folder_desti = f"{folder_destiny}/{filename_person}"
        shutil.copy2(txt_personalizado, folder_desti)
        #
    file_personalized = folder_desti
    with open(file_personalized, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    for nome in nomes:
        conteudo_interpretado = conteudo.format(apre=apre, nomes=nome)
    windowPerson = customtkinter.CTkToplevel(app)
    windowPerson.geometry("1500x250")
    windowPerson.title("Texto Personalizado. Teste de visualização")
    windowPerson.resizable(True, False)
    lblPerson = customtkinter.CTkLabel(
        windowPerson, text=conteudo_interpretado, font=("", 20), justify="center"
    )
    lblPerson.place(relx=0.1, rely=0.5, anchor="nw")
    lblyesno = customtkinter.CTkLabel(
        windowPerson,
        text="Está aparecendo todos os nomes normalmente?",
        font=("", 20),
        justify="center",
    )
    lblyesno.place(relx=0.1, rely=0.1, anchor="nw")
    btnYes = customtkinter.CTkButton(windowPerson, text="Sim", command="").place(
        relx=0.2, rely=0.2
    )
    btnNo = customtkinter.CTkButton(windowPerson, text="Não", command=btnno).place(
        relx=0.4, rely=0.2
    )



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
    label = customtkinter.CTkLabel(config, text="Tempo para aguardar o envio de mensagens.", justify="center")
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
        font=("", 20)
    )
    close_config.pack()
    close_config.place(x=480, y=65)
    save_img = customtkinter.CTkImage(Image.open("images/salvar-arquivo.png"))
    btnConfig = customtkinter.CTkButton(
        config, text="Salvar", command=save_config, image=save_img
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
        print(f"Arquivo salvo em: {caminho_destino}")
    else:
        CTkMessagebox(title="Base não selecionada", message="Nenhuma base carregada.")
    load_file.destroy()
    app.deiconify()
    n = 0
    i = 0
    p = 0
    pc = 0
    global nomes, tels, props, qtdNomes, soma
    data_frame = pd.read_excel(f"{caminho_destino}")
    nomes = (data_frame['Nome'].tolist())
    tels = (data_frame['Telefone'].tolist())
    props = (data_frame['Proposta'].tolist())
    #pacote = (data_frame['Pacote'].tolist())
    qtdNomes = len(nomes)
    soma = 1
    print(qtdNomes)
    label2 = None
    label = customtkinter.CTkLabel(app, text=f"Nomes a processar: {qtdNomes}", fg_color="#DBDBDB").place(x=225, y=50)



def config_button():
    app.withdraw()
    def ao_fechar_segunda_janela():
        configWindow.destroy()
        app.deiconify()
    configWindow = customtkinter.CTkToplevel(app)
    configWindow.protocol("WM_DELETE_WINDOW", ao_fechar_segunda_janela)
    configWindow.title("Configuração de Texto")
    configWindow.geometry("900x350")
    configWindow.resizable(False, False)
    # ---#
    label = customtkinter.CTkLabel(configWindow, text="Texto de Aguardando Pagamento")
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
        configWindow, text="Salvar configurações", command=text_os
    ).place(x=350, y=300)
    btnConfig = customtkinter.CTkButton(
        configWindow, text="Carregar texto personalizado", command=texto_personalizado
    ).place(x=700, y=5)


frameimg = customtkinter.CTkFrame(
    app,
    width=150,
    height=150,
    border_color="black",
    border_width=1,
    corner_radius=20,
).place(x=40, y=45)

frameform = customtkinter.CTkFrame(
    app, width=300, height=150, border_color="black", border_width=1, corner_radius=8,
).place(x=210, y=45)
label2 = customtkinter.CTkLabel(app, text="Nenhuma base selecionada ainda.", fg_color="#DBDBDB").place(x=225, y=50)
label2 = 0
btnConfig = customtkinter.CTkButton(
    app, text="Configurar Textos", command=config_button, fg_color="#545455", text_color="white"
).place(x=400, y=5)

upload_img = customtkinter.CTkImage(Image.open("images/upload.png"))

btnSend = customtkinter.CTkButton(
    app, text="Enviar Mensagens!", command=config_button
).place(x=95, y=210)
btnload = customtkinter.CTkButton(
    app, text="Carregar base", command=load_base, image=upload_img
).place(x=295, y=210)

img_config = customtkinter.CTkImage(Image.open("images/config.png"))

btnconfig = customtkinter.CTkButton(
    app, text="", command=config
,image=img_config, height=20, width=20).place(x=5, y=5)








app.mainloop()
