"""
main.py
--------
Arquivo principal que inicializa o programa, cria a figura e gerencia as atualizações
dos gráficos conforme os valores dos sliders são alterados.
"""

import numpy as np
import matplotlib.pyplot as plt
from plotting import plot_distribuicoes, plot_diferenca_pmf_surface, configurar_estetica_3d, inicializar_figura_eixos
from funcoes import gerar_matriz_parametros
from sliders import criar_sliders_controle, atualizar_graficos
from config import NUM_SUCESSOS_MIN, NUM_SUCESSOS_MAX, NUM_SUCESSOS_INICIAL, PROBABILIDADE_INICIAL, TAM_MARKER

# Gera a matriz de sucessos e probabilidades
N, P, Z = gerar_matriz_parametros(NUM_SUCESSOS_MIN, NUM_SUCESSOS_MAX)

# Cria a figura e os eixos
fig, ax_pmf, ax_mgf, ax_diff = inicializar_figura_eixos()

# Adiciona a superfície da diferença entre as PMFs
plot_diferenca_pmf_surface(ax_diff, N, P, Z)
point, = ax_diff.plot([], [], [], 'ko', ms=TAM_MARKER)

# Plota os gráficos iniciais das distribuições e das MGFs
configurar_estetica_3d(ax_diff)
plot_distribuicoes(ax_pmf, ax_mgf, NUM_SUCESSOS_INICIAL, PROBABILIDADE_INICIAL)

# Configura os sliders para controle dos parâmetros
slider_n, slider_p = criar_sliders_controle(fig)
slider_n.on_changed(lambda val: atualizar_graficos(val, slider_n, slider_p, ax_pmf, ax_mgf, ax_diff, fig, point))
slider_p.on_changed(lambda val: atualizar_graficos(val, slider_n, slider_p, ax_pmf, ax_mgf, ax_diff, fig, point))

# Exibe a interface gráfica
plt.show()