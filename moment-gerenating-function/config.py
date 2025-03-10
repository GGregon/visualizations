"""
config.py
---------
Arquivo com as configurações gerais do projeto.
Modifique os valores abaixo para personalizar o comportamento.
"""

# ==============================
# CONFIGURAÇÕES GERAIS
# ==============================

PROJECT_NAME = "Visualização Binomial vs Poisson"
VERSION = "1.0.0"
DEBUG_MODE = True  # Defina como False em produção

# ==============================
# CONFIGURAÇÕES DE PLOTAGEM
# ==============================

FIGURE_SIZE = (15, 5)           # Tamanho padrão da figura para todos os gráficos
COLORMAP = "inferno"            # Mapa de cores usado para a superfície 3D
GRID_ALPHA = 0.5                # Transparência das linhas da grade
SUBPLOT_BOTTOM_ADJUST = 0.25    # Ajuste do espaçamento inferior dos subplots

# Configurações do gráfico de PMF
PMF_Y_LIM = (0, 0.6)        # Limite do eixo Y para a PMF
PMF_BAR_ALPHA = 0.3         # Transparência das barras
PMF_LINESTYLE = '-'    # Estilo da linha da Poisson
PMF_MARKER_SIZE = 3         # Tamanho do marcador para a Poisson

# Configurações do gráfico de MGF
MGF_T_RANGE = (-1, 1)  # Intervalo de t para a MGF
MGF_T_POINTS = 100  # Número de pontos para a curva da MGF

# Configurações do gráfico 3D
SURFACE_ALPHA = 0.7  # Transparência da superfície
GRID_LINEWIDTH = 0.2  # Espessura das linhas da grade
COLORMAP = 'cool'

# ==============================
# PARÂMETROS DO MODELO
# ==============================

NUM_SUCESSOS_MAX = 50  # Número máximo de sucessos
NUM_SUCESSOS_MIN = 1  # Número mínimo de sucessos
PROBABILIDADE_MIN = 0.01  # Valor mínimo da probabilidade
PROBABILIDADE_MAX = 1.0  # Valor máximo da probabilidade
PROBABILIDADE_INICIAL = 0.5  # Probabilidade inicial padrão
NUM_SUCESSOS_INICIAL = 10  # Número inicial de sucessos padrão

# ==============================
# CONFIGURAÇÕES DOS SLIDERS
# ==============================

SLIDER_N_MIN = 1
SLIDER_N_MAX = 49
SLIDER_N_STEP = 1
SLIDER_N_INIT = 10

SLIDER_P_MIN = 0.01
SLIDER_P_MAX = 1.0
SLIDER_P_STEP = 0.01
SLIDER_P_INIT = 0.5

# ==============================
# CONFIGURAÇÕES DOS MARCADORES
# ==============================

TAM_MARKER = 5  # Tamanho do ponto móvel no gráfico 3D

# ==============================
# CONFIGURAÇÕES DE LOG (Opcional)
# ==============================

LOGGING_LEVEL = "INFO"  # Opções: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "app.log"  # Localização do arquivo de log

# ==============================
# FUNÇÃO PARA EXIBIR CONFIGURAÇÕES
# ==============================

def print_config():
    """Exibe todas as configurações do projeto."""
    print(f"Projeto: {PROJECT_NAME} (v{VERSION})")
    print(f"Tamanho da Figura: {FIGURE_SIZE}")
    print(f"Máx. Sucessos: {NUM_SUCESSOS_MAX}, Mín. Sucessos: {NUM_SUCESSOS_MIN}")
    print(f"Probabilidade Inicial: {PROBABILIDADE_INICIAL}")
    print(f"Mapa de Cores: {COLORMAP}")
    print(f"Modo Debug: {'Ativado' if DEBUG_MODE else 'Desativado'}")

if __name__ == "__main__":
    print_config()  # Exibir configurações se este arquivo for executado diretamente