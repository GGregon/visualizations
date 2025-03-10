"""
sliders.py
-----------
Módulo responsável por criar e atualizar os sliders que controlam os parâmetros
(número de sucessos e probabilidade de sucesso) e atualizam os gráficos.
"""

from matplotlib.widgets import Slider
import numpy as np
from plotting import plot_distribuicoes
from funcoes import pmf_difference
from config import (
    SLIDER_N_MIN, SLIDER_N_MAX, SLIDER_N_STEP, SLIDER_N_INIT, 
    SLIDER_P_MIN, SLIDER_P_MAX, SLIDER_P_STEP, SLIDER_P_INIT
)

def criar_sliders_controle(figura):
    """
    Cria os sliders para controlar os parâmetros n e p.

    Parâmetros:
    - figura (Figure): Figura do Matplotlib onde os sliders serão adicionados.

    Retorna:
    - slider_sucessos (Slider): Slider para o número de sucessos (n)
    - slider_probabilidade (Slider): Slider para a probabilidade de sucesso (p)
    """
    ax_n = figura.add_axes([0.2, 0.08, 0.65, 0.03])
    ax_p = figura.add_axes([0.2, 0.03, 0.65, 0.03])
    
    slider_sucessos = Slider(ax_n, 'n', SLIDER_N_MIN, SLIDER_N_MAX, valinit=SLIDER_N_INIT, valstep=SLIDER_N_STEP)
    slider_probabilidade = Slider(ax_p, 'p', SLIDER_P_MIN, SLIDER_P_MAX, valinit=SLIDER_P_INIT, valstep=SLIDER_P_STEP)
    
    return slider_sucessos, slider_probabilidade

def atualizar_ponto_3d(n: int, p: float, point):
    """
    Atualiza a posição do ponto no gráfico 3D com base nos novos valores de n e p.

    Parâmetros:
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso
    - point (Line3D): Objeto do ponto no gráfico 3D
    """
    _, diff = pmf_difference(n, p)
    point.set_data([n], [p])
    point.set_3d_properties(np.sum(diff))  # Computa apenas uma vez

def atualizar_graficos(valor, slider_sucessos: Slider, slider_probabilidade: Slider, ax_pmf, ax_mgf, ax_diff, figura, point):
    """
    Atualiza os gráficos de PMF, MGF e a posição do ponto no gráfico 3D
    com base nos valores dos sliders.

    Parâmetros:
    - valor: Valor do slider (não usado diretamente, mas necessário para callback)
    - slider_sucessos (Slider): Slider para o número de sucessos (n)
    - slider_probabilidade (Slider): Slider para a probabilidade de sucesso (p)
    - ax_pmf (Axes): Eixo do gráfico de PMFs
    - ax_mgf (Axes): Eixo do gráfico de MGFs
    - ax_diff (Axes3D): Eixo do gráfico 3D de diferença das PMFs
    - figura (Figure): Figura do Matplotlib para atualização
    - point (Line3D): Ponto móvel no gráfico 3D
    """
    n = int(slider_sucessos.val)
    p = slider_probabilidade.val
    
    # Atualiza os gráficos
    plot_distribuicoes(ax_pmf, ax_mgf, n, p)
    
    # Atualiza o ponto 3D
    atualizar_ponto_3d(n, p, point)

    # Atualiza a figura
    figura.canvas.draw_idle()
