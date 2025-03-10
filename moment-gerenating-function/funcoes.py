"""
funcoes.py
-----------
Módulo com funções auxiliares para cálculos estatísticos, incluindo:
- Geração de grids de parâmetros para distribuições Binomial e Poisson
- Cálculo das funções geradoras de momentos (MGFs)
- Cálculo da diferença entre funções de massa de probabilidade (PMFs)
"""


import numpy as np
import scipy.stats as stats
from config import PROBABILIDADE_MIN, PROBABILIDADE_MAX

def gerar_matriz_parametros(n_min: int, n_max: int):
    """
    Cria uma malha de parâmetros para os valores de n (sucessos) e p (probabilidades).

    Parâmetros:
    - n_min (int): Número mínimo de sucessos
    - n_max (int): Número máximo de sucessos

    Retorna:
    - N (np.ndarray): Matriz de sucessos
    - P (np.ndarray): Matriz de probabilidades
    - Z (np.ndarray): Diferença entre as PMFs Binomial e Poisson
    """
    n_values = np.arange(n_min, n_max)
    p_values = np.linspace(PROBABILIDADE_MIN, PROBABILIDADE_MAX, 50)
    N, P = np.meshgrid(n_values, p_values)
    Z = calcular_diferenca_pmfs_matriz(N, P)  # Computa a diferença uma única vez
    return N, P, Z  

def mgf_binomial(t: np.ndarray, n: int, p: float) -> np.ndarray:
    """
    Calcula a função geradora de momentos (MGF) para a distribuição Binomial.

    Parâmetros:
    - t (np.ndarray): Valores da variável t
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso

    Retorna:
    - np.ndarray: Valores da MGF
    """
    return (p * np.exp(t) + (1 - p)) ** n

def mgf_poisson(t: np.ndarray, lambda_poisson: float) -> np.ndarray:
    """
    Calcula a função geradora de momentos (MGF) para a distribuição de Poisson.

    Parâmetros:
    - t (np.ndarray): Valores da variável t
    - lambda_poisson (float): Parâmetro lambda_poissonbda da distribuição de Poisson

    Retorna:
    - np.ndarray: Valores da MGF
    """
    return np.exp(lambda_poisson * (np.exp(t) - 1))

def pmf_difference(n: int, p: float):
    """
    Calcula a diferença entre as funções de massa de probabilidade (PMFs)
    da distribuição Binomial e da distribuição de Poisson.

    Parâmetros:
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso

    Retorna:
    - sucessos (np.ndarray): Valores discretos da variável aleatória
    - np.ndarray: Diferença entre PMF Binomial e Poisson
    """
    sucessos, binom_pmf, poisson_pmf = calcular_pmfs(n, p)
    return sucessos, binom_pmf - poisson_pmf



def calcular_diferenca_pmfs_matriz(N_mesh: np.ndarray, P_mesh: np.ndarray) -> np.ndarray:
    """
    Calcula a diferença agregada entre as PMFs Binomial e Poisson para
    cada ponto da malha de parâmetros (N, P).

    Parâmetros:
    - N_mesh (np.ndarray): Matriz de valores de n
    - P_mesh (np.ndarray): Matriz de valores de p

    Retorna:
    - Z (np.ndarray): Matriz com as diferenças agregadas entre as PMFs
    """
    vectorized_pmf_diff = np.vectorize(lambda n, p: np.sum(pmf_difference(n, p)[1]))
    return vectorized_pmf_diff(N_mesh, P_mesh)


def calcular_pmfs(n: int, p: float):
    """
    Calcula as funções de massa de probabilidade (PMF) para as distribuições
    Binomial e Poisson.

    Parâmetros:
    - n (int): Número de sucessos
    - p (float): Probabilidade de sucesso

    Retorna:
    - sucessos (np.ndarray): Valores discretos da variável aleatória
    - binom_pmf (np.ndarray): PMF da distribuição Binomial
    - poisson_pmf (np.ndarray): PMF da distribuição de Poisson
    """
    sucessos = np.arange(0, n + 1)
    binom_pmf = stats.binom.pmf(sucessos, n, p)
    poisson_lambda = n * p
    poisson_pmf = stats.poisson.pmf(sucessos, poisson_lambda)
    return sucessos, binom_pmf, poisson_pmf
