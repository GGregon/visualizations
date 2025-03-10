"""
plotting.py
-----------
Módulo responsável por gerar os gráficos das distribuições Binomial e Poisson,
assim como a diferença entre suas PMFs em um gráfico 3D.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from funcoes import mgf_binomial, mgf_poisson
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from config import (
    FIGURE_SIZE, SUBPLOT_BOTTOM_ADJUST,
    PMF_Y_LIM, PMF_BAR_ALPHA, PMF_LINESTYLE, PMF_MARKER_SIZE,
    MGF_T_RANGE, MGF_T_POINTS,
    SURFACE_ALPHA, GRID_LINEWIDTH, COLORMAP
)

plt.rcParams['font.family'] = 'Latin Modern Math'  # Substitua pelo nome da fonte desejada
plt.rcParams['text.usetex'] = True  # Ativa suporte ao LaTeX

COR_POISSON  = 'darkviolet'
COR_BINOMIAL = 'darkturquoise'

def plot_pmf_distributions(ax_pmf, n: int, p: float):
    """
    Plota as funções de massa de probabilidade (PMF) para as distribuições Binomial e Poisson.

    Parâmetros:
    - ax_pmf (Axes): Eixo do gráfico de PMFs
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso
    """
    x = np.arange(0, n + 1)
    binom_y = stats.binom.pmf(x, n, p)
    poisson_lambda = n * p
    poisson_y = stats.poisson.pmf(x, poisson_lambda)

    ax_pmf.clear()
    ax_pmf.bar(x, binom_y, color='None', edgecolor=COR_BINOMIAL,label='Binomial')
    ax_pmf.plot(x, poisson_y, linestyle=PMF_LINESTYLE, color=COR_POISSON,label='Poisson')
    ax_pmf.set_xlabel('Sucessos')
    ax_pmf.set_ylabel('Densidade de probabilidade')
    ax_pmf.set_title(f'$n$={n}, $p$={p:.2f}, $\lambda$={poisson_lambda:.2f}')
    ax_pmf.grid(axis='y', linestyle='-', alpha=GRID_LINEWIDTH)
    ax_pmf.set_yticklabels([])
    ax_pmf.legend(fancybox=False,edgecolor='k',loc='upper left')

def plot_mgf_distributions(ax_mgf, n: int, p: float):
    """
    Plota as funções geradoras de momentos (MGF) para as distribuições Binomial e Poisson.

    Parâmetros:
    - ax_mgf (Axes): Eixo do gráfico de MGFs
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso
    """
    t_vals = np.linspace(MGF_T_RANGE[0], MGF_T_RANGE[1], MGF_T_POINTS)
    poisson_lambda = n * p
    mgf_binom_vals = mgf_binomial(t_vals, n, p)
    mgf_poisson_vals = mgf_poisson(t_vals, poisson_lambda)

    ax_mgf.clear()
    ax_mgf.plot(t_vals, mgf_binom_vals, color=COR_BINOMIAL)
    ax_mgf.plot(t_vals, mgf_poisson_vals, color=COR_POISSON)
    ax_mgf.axvline(x=0,c='k',alpha=0.5,ls='--')
    ax_mgf.set_xlabel('t')
    ax_mgf.set_title('MGF')
    ax_mgf.grid(linestyle='-', alpha=GRID_LINEWIDTH)
    ax_mgf.set_yticklabels([])

    # Criar um eixo auxiliar para o zoom em t=0
    ax_inset = inset_axes(ax_mgf, width="40%", height="40%", loc='upper left',borderpad=1)
    zoom_t_vals = np.linspace(-0.05, 0.05, MGF_T_POINTS)
    zoom_mgf_binom = mgf_binomial(zoom_t_vals, n, p)
    zoom_mgf_poisson = mgf_poisson(zoom_t_vals, poisson_lambda)
    
    ax_inset.plot(zoom_t_vals, zoom_mgf_binom, color=COR_BINOMIAL)
    ax_inset.plot(zoom_t_vals, zoom_mgf_poisson, linestyle='-', color=COR_POISSON)
    ax_inset.axvline(x=0,c='k',alpha=0.5,ls='--')
    epsilon = 0.05  # Define o valor de ε
    ax_inset.set_xticks([-epsilon, 0, epsilon])
    ax_inset.set_xticklabels([r'$-\varepsilon$', r'$0$', r'$+\varepsilon$'])
    ax_inset.set_yticks([])
    ax_inset.set_xlim(-0.05, 0.05)
    ax_inset.set_ylim(min(zoom_mgf_binom.min(), zoom_mgf_poisson.min()), max(zoom_mgf_binom.max(), zoom_mgf_poisson.max()))
    # ax_inset.set_title("Vizinhança de t=0", fontsize=8)
    

def plot_distribuicoes(ax_pmf, ax_mgf, n: int, p: float):
    """
    Plota as distribuições PMF e MGF para as distribuições Binomial e Poisson.

    Parâmetros:
    - ax_pmf (Axes): Eixo do gráfico de PMFs
    - ax_mgf (Axes): Eixo do gráfico de MGFs
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso
    """
    plot_pmf_distributions(ax_pmf, n, p)
    plot_mgf_distributions(ax_mgf, n, p)
    plt.draw()

def plot_diferenca_pmf_surface(ax_3d, n_grid: np.ndarray, p_grid: np.ndarray, diferenca_pmf_grid: np.ndarray):
    """
    Plota a superfície da diferença entre as PMFs Binomial e Poisson em um gráfico 3D.

    Parâmetros:
    - ax_3d (Axes3D): Eixo do gráfico 3D
    - n_grid (np.ndarray): Matriz dos valores de n
    - p_grid (np.ndarray): Matriz dos valores de p
    - diferenca_pmf_grid (np.ndarray): Matriz das diferenças entre as PMFs
    """
    ax_3d.clear()
    ax_3d.plot_surface(n_grid, p_grid, diferenca_pmf_grid, cmap=COLORMAP, alpha=SURFACE_ALPHA)
    # ax_3d.set_box_aspect([1,1,1])
    ax_3d.set_xlabel('n')
    ax_3d.set_ylabel('p')
    ax_3d.set_title("Erro entre as PMFs")

def configurar_estetica_3d(ax):
    """
    Configura a estética do gráfico 3D, removendo cores dos planos e ajustando a grade.

    Parâmetros:
    - ax (Axes3D): Eixo do gráfico 3D a ser configurado
    """
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.xaxis._axinfo['grid'].update(color='lightgray', linewidth=GRID_LINEWIDTH)
    ax.yaxis._axinfo['grid'].update(color='lightgray', linewidth=GRID_LINEWIDTH)
    ax.zaxis._axinfo['grid'].update(color='lightgray', linewidth=GRID_LINEWIDTH)
    
    ax.set_zticklabels([])

def inicializar_figura_eixos():
    """
    Inicializa a figura principal e os eixos para os gráficos de PMF, MGF e Superfície 3D.

    Retorna:
    - fig (Figure): Figura principal
    - ax_pmf (Axes): Eixo do gráfico de PMFs
    - ax_mgf (Axes): Eixo do gráfico de MGFs
    - ax_3d (Axes3D): Eixo do gráfico 3D
    """
    fig = plt.figure(figsize=FIGURE_SIZE)
    fig.subplots_adjust(bottom=SUBPLOT_BOTTOM_ADJUST,wspace=0.05)
    ax_pmf = fig.add_subplot(131)
    ax_mgf = fig.add_subplot(132)
    ax_3d = fig.add_subplot(133, projection='3d')
    return fig, ax_pmf, ax_mgf, ax_3d