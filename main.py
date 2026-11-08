import tkinter as tk
import threading
import time
import os
import sys
import ctypes

from PIL import Image
import pystray


# =====================================================
# WINDOWS API
# =====================================================

user32 = ctypes.windll.user32

# Left mouse button
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# Right mouse button
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Keys
VK_ESCAPE = 0x1B
VK_F6 = 0x75

# Arrow keys
VK_UP = 0x26
VK_DOWN = 0x28

# Numpad
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65


# =====================================================
# RESOURCE PATH
# =====================================================

def caminho_recurso(nome_arquivo):

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(
            sys._MEIPASS,
            nome_arquivo
        )

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        nome_arquivo
    )


# =====================================================
# SETTINGS
# =====================================================

ativo = False
executando = True
nivel_atual = 3

icone_tray = None
janela_oculta = False

# False = Arrow keys
# True = Numpad
usar_numpad = False

# False = Left mouse button
# True = Right mouse button
usar_botao_direito = False

velocidades = {
    1: 0.50,
    2: 0.25,
    3: 0.10,
    4: 0.05,
    5: 0.02
}


# =====================================================
# COLORS
# =====================================================

COR_FUNDO = "#101018"
COR_CARD = "#1B1725"
COR_TEXTO = "#F3EFFA"
COR_TEXTO_SECUNDARIO = "#ADA4BF"

# Previous variable names are preserved for compatibility.
COR_AZUL = "#8B5CF6"          # JakkByte purple
COR_AZUL_ESCURO = "#6D28D9"
COR_AZUL_CLARO = "#38294F"
COR_VERDE = "#A3E635"         # JakkByte neon green
COR_VERMELHO = "#B84568"
COR_VERMELHO_ESCURO = "#923653"
COR_BORDA = "#392D4B"
COR_ATALHOS = "#171320"
COR_SWITCH_DESLIGADO = "#51465F"
COR_CABECALHO = "#181020"


# =====================================================
# CHECK KEY
# =====================================================

def tecla_pressionada(codigo):

    return bool(
        user32.GetAsyncKeyState(codigo) & 0x8000
    )


# =====================================================
# MOUSE CLICK
# =====================================================

def clicar():

    if usar_botao_direito:

        user32.mouse_event(
            MOUSEEVENTF_RIGHTDOWN,
            0,
            0,
            0,
            0
        )

        user32.mouse_event(
            MOUSEEVENTF_RIGHTUP,
            0,
            0,
            0,
            0
        )

    else:

        user32.mouse_event(
            MOUSEEVENTF_LEFTDOWN,
            0,
            0,
            0,
            0
        )

        user32.mouse_event(
            MOUSEEVENTF_LEFTUP,
            0,
            0,
            0,
            0
        )


# =====================================================
# STATUS
# =====================================================

def atualizar_status():

    if ativo:

        status_label.config(
            text="●  ACTIVE  |  JAKKBYTE",
            fg=COR_VERDE
        )

        botao_iniciar.config(
            text="STOP",
            bg=COR_VERMELHO,
            fg="#FFFFFF",
            activebackground=COR_VERMELHO_ESCURO
        )

        descricao_status.config(
            text="Automatic clicking is running"
        )

    else:

        status_label.config(
            text="●  READY",
            fg=COR_TEXTO_SECUNDARIO
        )

        botao_iniciar.config(
            text="START",
            bg=COR_VERDE,
            fg=COR_FUNDO,
            activeforeground=COR_FUNDO,
            activebackground="#84CC16"
        )

        descricao_status.config(
            text="Press F6 or click START"
        )


# =====================================================
# START / STOP
# =====================================================

def alternar():

    global ativo

    ativo = not ativo

    atualizar_status()


# =====================================================
# SPEED
# =====================================================

def mudar_velocidade(nivel):

    global nivel_atual

    nivel = max(
        1,
        min(5, nivel)
    )

    nivel_atual = nivel

    velocidade.set(nivel)

    nivel_label.config(
        text=f"Level {nivel}"
    )


def barra_alterada(valor):

    global nivel_atual

    nivel_atual = int(
        float(valor)
    )

    nivel_label.config(
        text=f"Level {nivel_atual}"
    )


# =====================================================
# CONTROL MODE SWITCH
# =====================================================

def desenhar_switch(event=None):

    switch_canvas.delete("all")

    if usar_numpad:
        cor_fundo = COR_AZUL
        posicao_x = 21
    else:
        cor_fundo = COR_SWITCH_DESLIGADO
        posicao_x = 4

    switch_canvas.create_oval(
        1, 2, 21, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_canvas.create_oval(
        19, 2, 39, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_canvas.create_rectangle(
        11, 2, 29, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_canvas.create_oval(
        posicao_x,
        5,
        posicao_x + 12,
        17,
        fill=COR_TEXTO,
        outline=COR_TEXTO
    )


def alternar_modo_controle():

    global usar_numpad

    usar_numpad = not usar_numpad

    if usar_numpad:

        modo_label.config(
            text="Numpad 1–5"
        )

    else:

        modo_label.config(
            text="Arrow keys ↑ / ↓"
        )

    desenhar_switch()


# =====================================================
# MOUSE BUTTON SWITCH
# =====================================================

def desenhar_switch_mouse(event=None):

    switch_mouse_canvas.delete("all")

    if usar_botao_direito:
        cor_fundo = COR_AZUL
        posicao_x = 21
    else:
        cor_fundo = COR_SWITCH_DESLIGADO
        posicao_x = 4

    switch_mouse_canvas.create_oval(
        1, 2, 21, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_mouse_canvas.create_oval(
        19, 2, 39, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_mouse_canvas.create_rectangle(
        11, 2, 29, 20,
        fill=cor_fundo,
        outline=cor_fundo
    )

    switch_mouse_canvas.create_oval(
        posicao_x,
        5,
        posicao_x + 12,
        17,
        fill=COR_TEXTO,
        outline=COR_TEXTO
    )


def alternar_botao_mouse():

    global usar_botao_direito

    usar_botao_direito = not usar_botao_direito

    if usar_botao_direito:

        botao_mouse_label.config(
            text="Right"
        )

    else:

        botao_mouse_label.config(
            text="Left"
        )

    desenhar_switch_mouse()


# =====================================================
# AUTO CLICK
# =====================================================

def auto_click():

    while executando:

        if ativo:

            clicar()

            time.sleep(
                velocidades[nivel_atual]
            )

        else:

            time.sleep(0.02)


# =====================================================
# MONITOR KEYBOARD
# =====================================================

def monitorar_teclas():

    global ativo

    estado_f6 = False
    estado_esc = False

    estado_cima = False
    estado_baixo = False

    estados_numpad = {
        VK_NUMPAD1: False,
        VK_NUMPAD2: False,
        VK_NUMPAD3: False,
        VK_NUMPAD4: False,
        VK_NUMPAD5: False
    }

    teclas_numpad = {
        VK_NUMPAD1: 1,
        VK_NUMPAD2: 2,
        VK_NUMPAD3: 3,
        VK_NUMPAD4: 4,
        VK_NUMPAD5: 5
    }

    while executando:

        # =================================================
        # F6 - START / STOP
        # =================================================

        pressionado_f6 = tecla_pressionada(
            VK_F6
        )

        if pressionado_f6 and not estado_f6:

            ativo = not ativo

            janela.after(
                0,
                atualizar_status
            )

        estado_f6 = pressionado_f6


        # =================================================
        # ARROW KEY CONTROL
        # =================================================

        if not usar_numpad:

            pressionado_cima = tecla_pressionada(
                VK_UP
            )

            pressionado_baixo = tecla_pressionada(
                VK_DOWN
            )

            if pressionado_cima and not estado_cima:

                novo_nivel = min(
                    5,
                    nivel_atual + 1
                )

                janela.after(
                    0,
                    mudar_velocidade,
                    novo_nivel
                )

            if pressionado_baixo and not estado_baixo:

                novo_nivel = max(
                    1,
                    nivel_atual - 1
                )

                janela.after(
                    0,
                    mudar_velocidade,
                    novo_nivel
                )

            estado_cima = pressionado_cima
            estado_baixo = pressionado_baixo

        else:

            estado_cima = False
            estado_baixo = False


        # =================================================
        # NUMPAD CONTROL
        # =================================================

        if usar_numpad:

            for codigo, numero in teclas_numpad.items():

                pressionado = tecla_pressionada(
                    codigo
                )

                if pressionado and not estados_numpad[codigo]:

                    janela.after(
                        0,
                        mudar_velocidade,
                        numero
                    )

                estados_numpad[codigo] = pressionado

        else:

            for codigo in estados_numpad:
                estados_numpad[codigo] = False


        # =================================================
        # ESC - EXIT
        # =================================================

        pressionado_esc = tecla_pressionada(
            VK_ESCAPE
        )

        if pressionado_esc and not estado_esc:

            janela.after(
                0,
                fechar
            )

            break

        estado_esc = pressionado_esc

        time.sleep(0.015)


# =====================================================
# WINDOWS SYSTEM TRAY
# =====================================================

def criar_icone_tray():

    global icone_tray

    imagem = Image.open(
        caminho_recurso(
            "autoclickac.ico"
        )
    )

    menu = pystray.Menu(

        pystray.MenuItem(
            "Open AutoClick AC",
            restaurar_janela,
            default=True
        ),

        pystray.Menu.SEPARATOR,

        pystray.MenuItem(
            "Exit",
            sair_tray
        )
    )

    icone_tray = pystray.Icon(
        "AutoClickAC",
        imagem,
        "AutoClick AC",
        menu
    )

    icone_tray.run()


def minimizar_para_tray():

    global janela_oculta

    if janela_oculta:
        return

    janela_oculta = True

    janela.withdraw()

    threading.Thread(
        target=criar_icone_tray,
        daemon=True
    ).start()


def restaurar_janela(
    icon=None,
    item=None
):

    janela.after(
        0,
        restaurar_janela_principal
    )


def restaurar_janela_principal():

    global janela_oculta
    global icone_tray

    janela_oculta = False

    if icone_tray is not None:

        icone_tray.stop()

        icone_tray = None

    janela.deiconify()
    janela.lift()
    janela.focus_force()


def sair_tray(
    icon=None,
    item=None
):

    janela.after(
        0,
        fechar
    )


# =====================================================
# DETECT MINIMIZATION
# =====================================================

def verificar_estado_janela(event=None):

    if janela.state() == "iconic":

        janela.after(
            10,
            minimizar_para_tray
        )


# =====================================================
# CLOSE APPLICATION
# =====================================================

def fechar():

    global executando
    global ativo
    global icone_tray

    ativo = False
    executando = False

    if icone_tray is not None:

        icone_tray.stop()
        icone_tray = None

    janela.destroy()


# =====================================================
# WINDOW
# =====================================================

janela = tk.Tk()

janela.title(
    "AutoClick AC  |  JakkByte"
)

# Existing icon; do not modify or recreate the mascot.
# The interface can still open if the icon file is missing.
try:
    janela.iconbitmap(caminho_recurso("autoclickac.ico"))
except (OSError, tk.TclError):
    pass

# A few extra pixels for the new option
janela.geometry(
    "410x410"

)

janela.resizable(
    False,
    False
)

janela.configure(
    bg=COR_FUNDO
)


# =====================================================
# HEADER
# =====================================================

cabecalho = tk.Frame(
    janela,
    bg=COR_CABECALHO,
    height=65
)

cabecalho.pack(
    fill="x"
)

cabecalho.pack_propagate(
    False
)


titulo = tk.Label(
    cabecalho,
    text="AUTOCLICK AC",
    font=("Segoe UI", 19, "bold"),
    bg=COR_CABECALHO,
    fg="#FFFFFF"
)

titulo.pack(
    pady=(1, 0)
)


subtitulo = tk.Label(
    cabecalho,
    text="JAKKBYTE  /  INDIE SOFTWARE",
    font=("Segoe UI", 8),
    bg=COR_CABECALHO,
    fg="#B9A1E9"
)

subtitulo.pack()


# =====================================================
# MAIN CONTAINER
# =====================================================

container = tk.Frame(
    janela,
    bg=COR_FUNDO
)

container.pack(
    padx=18,
    pady=10,
    fill="both",
    expand=True
)


# =====================================================
# STATUS
# =====================================================

status_card = tk.Frame(
    container,
    bg=COR_CARD,
    highlightthickness=1,
    highlightbackground=COR_BORDA
)

status_card.pack(
    fill="x"
)


status_label = tk.Label(
    status_card,
    text="●  READY",
    font=("Segoe UI", 11, "bold"),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

status_label.pack(
    pady=(7, 0)
)


descricao_status = tk.Label(
    status_card,
    text="Press F6 or click START",
    font=("Segoe UI", 8),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

descricao_status.pack(
    pady=(0, 7)
)


# =====================================================
# SPEED
# =====================================================

velocidade_card = tk.Frame(
    container,
    bg=COR_CARD,
    highlightthickness=1,
    highlightbackground=COR_BORDA
)

velocidade_card.pack(
    fill="x",
    pady=(7, 0)
)


linha_velocidade = tk.Frame(
    velocidade_card,
    bg=COR_CARD
)

linha_velocidade.pack(
    fill="x",
    padx=22,
    pady=(6, 0)
)


texto_velocidade = tk.Label(
    linha_velocidade,
    text="CLICK SPEED",
    font=("Segoe UI", 9, "bold"),
    bg=COR_CARD,
    fg=COR_TEXTO
)

texto_velocidade.pack(
    side="left"
)


nivel_label = tk.Label(
    linha_velocidade,
    text="Level 3",
    font=("Segoe UI", 9, "bold"),
    bg=COR_CARD,
    fg=COR_VERDE
)

nivel_label.pack(
    side="right"
)


velocidade = tk.IntVar(
    value=3
)


barra = tk.Scale(
    velocidade_card,

    from_=1,
    to=5,

    orient="horizontal",

    variable=velocidade,

    length=300,

    resolution=1,

    command=barra_alterada,

    bg=COR_CARD,
    fg=COR_TEXTO,

    troughcolor=COR_AZUL_CLARO,
    activebackground=COR_VERDE,

    highlightthickness=0,
    borderwidth=0,

    font=("Segoe UI", 8),
    sliderrelief="flat",
    showvalue=False
)

barra.pack(
    pady=(0, 3)
)


# =====================================================
# CONTROL SWITCH
# =====================================================

controle_frame = tk.Frame(
    velocidade_card,
    bg=COR_CARD
)

controle_frame.pack(
    padx=(22, 18),
    pady=(1, 3),
    fill="x"
)


controle_label = tk.Label(
    controle_frame,
    text="Control:",
    font=("Segoe UI", 8),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

controle_label.pack(
    side="left"
)


switch_area = tk.Frame(
    controle_frame,
    bg=COR_CARD
)

switch_area.pack(
    side="right",
    padx=(4, 4)
)


modo_label = tk.Label(
    switch_area,
    text="Arrow keys ↑ / ↓",
    font=("Segoe UI", 8),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

modo_label.pack(
    side="left",
    padx=(0, 7)
)


switch_canvas = tk.Canvas(
    switch_area,
    width=40,
    height=22,
    bg=COR_CARD,
    highlightthickness=0,
    borderwidth=0,
    cursor="hand2"
)

switch_canvas.pack(
    side="left"
)


switch_canvas.bind(
    "<Button-1>",
    lambda event: alternar_modo_controle()
)


switch_canvas.bind(
    "<Configure>",
    desenhar_switch
)


# =====================================================
# MOUSE BUTTON SWITCH
# =====================================================

mouse_frame = tk.Frame(
    velocidade_card,
    bg=COR_CARD
)

mouse_frame.pack(
    padx=(22, 18),
    pady=(0, 8),
    fill="x"
)


mouse_texto = tk.Label(
    mouse_frame,
    text="Mouse button:",
    font=("Segoe UI", 8),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

mouse_texto.pack(
    side="left"
)


switch_mouse_area = tk.Frame(
    mouse_frame,
    bg=COR_CARD
)

switch_mouse_area.pack(
    side="right",
    padx=(4, 4)
)


botao_mouse_label = tk.Label(
    switch_mouse_area,
    text="Left",
    font=("Segoe UI", 8),
    bg=COR_CARD,
    fg=COR_TEXTO_SECUNDARIO
)

botao_mouse_label.pack(
    side="left",
    padx=(0, 7)
)


switch_mouse_canvas = tk.Canvas(
    switch_mouse_area,
    width=40,
    height=22,
    bg=COR_CARD,
    highlightthickness=0,
    borderwidth=0,
    cursor="hand2"
)

switch_mouse_canvas.pack(
    side="left"
)


switch_mouse_canvas.bind(
    "<Button-1>",
    lambda event: alternar_botao_mouse()
)


switch_mouse_canvas.bind(
    "<Configure>",
    desenhar_switch_mouse
)


# Initial rendering of both switches
janela.after_idle(
    desenhar_switch
)

janela.after_idle(
    desenhar_switch_mouse
)


# =====================================================
# START BUTTON
# =====================================================

botao_iniciar = tk.Button(
    container,

    text="START",

    font=("Segoe UI", 10, "bold"),

    height=1,

    bg=COR_VERDE,
    fg=COR_FUNDO,

    activebackground="#84CC16",
    activeforeground=COR_FUNDO,

    relief="flat",
    borderwidth=0,

    cursor="hand2",

    command=alternar
)

botao_iniciar.pack(
    fill="x",
    ipady=5,
    pady=(8, 0)
)


# =====================================================
# SHORTCUTS
# =====================================================

atalhos_card = tk.Frame(
    container,
    bg=COR_ATALHOS,
    highlightthickness=1,
    highlightbackground=COR_BORDA
)

atalhos_card.pack(
    fill="x",
    pady=(8, 0)
)


titulo_atalhos = tk.Label(
    atalhos_card,
    text="SHORTCUTS  /  CONTROLS",
    font=("Segoe UI", 9, "bold"),
    bg=COR_ATALHOS,
    fg=COR_TEXTO
)

titulo_atalhos.pack(
    pady=(5, 2)
)


atalho_f6 = tk.Label(
    atalhos_card,
    text="F6     •     Start / Stop",
    font=("Segoe UI", 8),
    bg=COR_ATALHOS,
    fg=COR_TEXTO_SECUNDARIO
)

atalho_f6.pack()


atalho_esc = tk.Label(
    atalhos_card,
    text="ESC     •     Exit application",
    font=("Segoe UI", 8),
    bg=COR_ATALHOS,
    fg=COR_TEXTO_SECUNDARIO
)

atalho_esc.pack(
    pady=(0, 3)
)


# =====================================================
# SIGNATURE
# =====================================================

rodape = tk.Label(
    container,
    text="AutoClick AC  •  Developed by JakkByte",
    font=("Segoe UI", 8),
    bg=COR_FUNDO,
    fg="#B9A1E9"
)

rodape.pack(
    pady=(4, 0)
)


# =====================================================
# EVENTOS DA WINDOW
# =====================================================

janela.protocol(
    "WM_DELETE_WINDOW",
    fechar
)

janela.bind(
    "<Unmap>",
    verificar_estado_janela
)


# =====================================================
# AUTO CLICK THREAD
# =====================================================

threading.Thread(
    target=auto_click,
    daemon=True
).start()


# =====================================================
# KEYBOARD THREAD
# =====================================================

threading.Thread(
    target=monitorar_teclas,
    daemon=True
).start()


# =====================================================
# START APPLICATION
# =====================================================

janela.mainloop()


# =====================================================
# AutoClick AC — JakkByte
# Automatic clicking application for Windows.
# Review and test the application before publishing a release.
# =====================================================
# If you’ve reached this point, thank you for using my program.
# It is simple and straightforward.
# I created it for personal use, so it is safe.
# =====================================================