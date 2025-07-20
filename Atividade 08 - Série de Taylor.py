import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- 1. Paleta de Cores e Fontes (Inspirado no CSS) ---
COR_FUNDO_JANELA = "#0d0d1a"     # Cor de fundo principal
COR_FUNDO_PAINEL = "#0f1428"     # Cor dos "cards" (aproximação do rgba)
COR_BORDA_PAINEL = "#0f3460"     # Borda sutil dos painéis
COR_TEXTO_GERAL = "#c0c0c0"       # Cinza claro para textos
COR_TEXTO_TITULO = "#ffffff"       # Branco para o título principal
COR_DESTAQUE_CIANO = "#00aaff"    # Ciano para subtítulo e resultados
COR_DESTAQUE_MAGENTA = "#ff00ff"  # Magenta para títulos de seção

# Fontes (usando fontes comuns como substitutas)
FONTE_TITULO_PRINCIPAL = ("Impact", 28) # "Orbitron" substitute
FONTE_SUBTITULO = ("Consolas", 12, "bold")
FONTE_TITULO_PAINEL = ("Impact", 18)    # "Orbitron" substitute
FONTE_TEXTO_COMUM = ("Consolas", 10)
FONTE_RESULTADO = ("Consolas", 11, "bold")
FONTE_BOTAO = ("Consolas", 11, "bold")

# --- Lógica de Cálculo (Inalterada) ---
def calcular_ln_taylor(x, erro_max):
    if x <= -1 or x > 1:
        return None, 0
    soma_aproximada = 0
    termo_atual = x
    n = 1
    max_iteracoes = 1000
    while abs(termo_atual) > erro_max and n <= max_iteracoes:
        soma_aproximada += termo_atual
        sinal = (-1)**n
        n += 1
        termo_atual = sinal * (x**n) / n
    if n > max_iteracoes:
        return float('inf'), n - 1
    return soma_aproximada, n - 1

# --- Funções da Interface ---
def executar_calculo_ln1_5():
    try:
        x = 0.5
        erro_desejado = 10**(-4)
        valor_aprox, termos = calcular_ln_taylor(x, erro_desejado)
        valor_exato = math.log(1 + x)
        resultado_aprox_var.set(f"{valor_aprox:.6f}")
        resultado_exato_var.set(f"{valor_exato:.6f}")
        resultado_termos_var.set(f"{termos} iterações")
    except Exception as e:
        messagebox.showerror("Erro de Cálculo", f"Ocorreu uma falha no subsistema de cálculo: {e}")

# --- 2. Configuração da Janela e Estilos ---
janela = tk.Tk()
janela.title("Painel de Análise Computacional")
janela.configure(bg=COR_FUNDO_JANELA)

# ✨ ALTERAÇÃO PARA INICIAR EM TELA CHEIA (MAXIMIZADO) ✨
janela.state('zoomed')


# Estilos dos Widgets
style = ttk.Style(janela)
style.theme_use('clam')

# Estilos Gerais
style.configure('TFrame', background=COR_FUNDO_JANELA)
style.configure('TLabel', background=COR_FUNDO_JANELA, foreground=COR_TEXTO_GERAL, font=FONTE_TEXTO_COMUM)

# Estilo para os Paineis (LabelFrames)
style.configure('Card.TLabelframe',
                background=COR_FUNDO_PAINEL,
                bordercolor=COR_BORDA_PAINEL,
                relief="solid")
style.configure('Card.TLabelframe.Label',
                background=COR_FUNDO_PAINEL,
                foreground=COR_DESTAQUE_MAGENTA,
                font=FONTE_TITULO_PAINEL)

# Estilo para Frames DENTRO dos painéis
style.configure('Card.TFrame', background=COR_FUNDO_PAINEL)

# Estilo para Labels de texto DENTRO dos painéis
style.configure('Card.TLabel', background=COR_FUNDO_PAINEL, foreground=COR_TEXTO_GERAL, font=FONTE_TEXTO_COMUM)

# Estilo para Labels de resultado DENTRO dos painéis
style.configure('Result.TLabel', background=COR_FUNDO_PAINEL, foreground=COR_DESTAQUE_CIANO, font=FONTE_RESULTADO)

# Estilo do Botão Principal
style.configure('ActionButton.TButton',
                background=COR_DESTAQUE_CIANO,
                foreground=COR_FUNDO_PAINEL,
                font=FONTE_BOTAO,
                borderwidth=0,
                relief='flat',
                padding=8)
style.map('ActionButton.TButton',
          background=[('active', COR_FUNDO_PAINEL)],
          foreground=[('active', COR_DESTAQUE_CIANO)])


# --- 3. Layout da Interface ---

# Frame do Cabeçalho
frame_header = ttk.Frame(janela, padding=(0, 20))
frame_header.pack(fill='x')
ttk.Label(frame_header, text="PAINEL DE ANÁLISE", font=FONTE_TITULO_PRINCIPAL, foreground=COR_TEXTO_TITULO, anchor='center').pack()
ttk.Label(frame_header, text="SIMULAÇÃO DE SÉRIE DE TAYLOR", font=FONTE_SUBTITULO, foreground=COR_DESTAQUE_CIANO, anchor='center').pack()

# Frame principal para os dois painéis
frame_main = ttk.Frame(janela)
frame_main.pack(expand=True, fill='both', padx=20, pady=20)
frame_main.columnconfigure(0, weight=1)
frame_main.columnconfigure(1, weight=1)
frame_main.rowconfigure(0, weight=1)

# PAINEL 1: CÁLCULO
painel_calculo = ttk.LabelFrame(frame_main, text="MÓDULO DE CÁLCULO", style='Card.TLabelframe')
painel_calculo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

# Conteúdo do Painel de Cálculo
inner_frame_calc = ttk.Frame(painel_calculo, style='Card.TFrame')
inner_frame_calc.pack(expand=True, fill='both', padx=20, pady=15)

ttk.Label(inner_frame_calc, text="Computar ln(1.5) via Série de Taylor:", style='Card.TLabel').pack(pady=(0,10))

btn_calcular = ttk.Button(inner_frame_calc, text="INICIAR COMPUTAÇÃO", style="ActionButton.TButton", command=executar_calculo_ln1_5, cursor="hand2")
btn_calcular.pack(pady=15, fill='x')

ttk.Separator(inner_frame_calc, orient='horizontal').pack(fill='x', pady=20)

# Resultados
frame_resultados = ttk.Frame(inner_frame_calc, style='Card.TFrame')
frame_resultados.pack(fill='x')

resultado_aprox_var = tk.StringVar(value="---")
resultado_exato_var = tk.StringVar(value="---")
resultado_termos_var = tk.StringVar(value="---")

ttk.Label(frame_resultados, text="Valor Aproximado:", style='Card.TLabel').grid(row=0, column=0, sticky="w", pady=2)
ttk.Label(frame_resultados, textvariable=resultado_aprox_var, style='Result.TLabel').grid(row=0, column=1, sticky="e", pady=2)

ttk.Label(frame_resultados, text="Valor de Referência:", style='Card.TLabel').grid(row=1, column=0, sticky="w", pady=2)
ttk.Label(frame_resultados, textvariable=resultado_exato_var, style='Result.TLabel').grid(row=1, column=1, sticky="e", pady=2)

ttk.Label(frame_resultados, text="Termos Necessários:", style='Card.TLabel').grid(row=2, column=0, sticky="w", pady=2)
ttk.Label(frame_resultados, textvariable=resultado_termos_var, style='Result.TLabel').grid(row=2, column=1, sticky="e", pady=2)

frame_resultados.columnconfigure(1, weight=1)

# PAINEL 2: ALERTA
painel_alerta = ttk.LabelFrame(frame_main, text="ALERTA DE SISTEMA", style='Card.TLabelframe')
painel_alerta.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

texto_explicacao = """
Análise de Convergência para ln(2.71828):

ENTRADA:
x = 1.71828

STATUS:
FALHA CRÍTICA DE CONVERGÊNCIA

MOTIVO:
O valor de entrada 'x' excede o raio de convergência da série de Taylor para f(x)=ln(1+x), que é definido como -1 < x ≤ 1. A computação resulta em uma série divergente, tornando o resultado inválido.
"""

text_widget = tk.Text(painel_alerta, wrap="word", bg=COR_FUNDO_PAINEL, fg=COR_TEXTO_GERAL, font=FONTE_TEXTO_COMUM, borderwidth=0, relief="flat", highlightthickness=0)
text_widget.insert("1.0", texto_explicacao)
text_widget.config(state="disabled")
text_widget.pack(expand=True, fill="both", padx=20, pady=20)


# --- 4. Inicia a Interface ---
janela.mainloop()