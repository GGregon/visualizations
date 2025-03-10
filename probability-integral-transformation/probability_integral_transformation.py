# Reimportando as bibliotecas necessárias, pois o estado foi resetado
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family']='latinmodern-math'
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

# Função de transformação usando a inversa da CDF da normal
def transform_to_normal(uniform_value):
    return norm.ppf(uniform_value)

# Parâmetros da animação
num_frames = 200
x_uniform = np.linspace(0, 1, 1000)
x_normal = np.linspace(-4, 4, 1000)

# Criação da figura com GridSpec
fig = plt.figure(figsize=(8, 8))
gs = GridSpec(2, 2, figure=fig, width_ratios=[3, 1], height_ratios=[1, 3], hspace=0.1, wspace=0.1)

# Gráficos
ax_relation = fig.add_subplot(gs[1, 0])
ax_pdf_x = fig.add_subplot(gs[0, 0], sharex=ax_relation)
ax_pdf_y = fig.add_subplot(gs[1, 1], sharey=ax_relation)

# Gráfico da relação entre X (normal) e Y (uniforme)
ax_relation.set_xlim(-4, 4)
ax_relation.set_xticklabels([])
ax_relation.set_ylim(0, 1)
ax_relation.set_xlabel(r'$X$',fontsize=16)
ax_relation.set_ylabel(r'$Y=F_X(X)$',fontsize=16)
ax_relation.grid(alpha=0.3)

# Gráfico da PDF da distribuição normal (superior)
# ax_pdf_x.plot(x_normal, norm.pdf(x_normal), color='tab:red')
ax_pdf_x.set_title(r'$X \sim \mathcal{N}(\mu,\sigma)$',loc='left',fontsize=16)
ax_pdf_x.set_ylim(0, .45)
ax_pdf_x.tick_params(axis='y',width =0)
ax_pdf_x.set_yticklabels([])
ax_pdf_x.spines[['left','top','right']].set_visible(False)

# Gráfico da PDF da distribuição uniforme (direito)
ax_pdf_y.plot(np.ones_like(x_uniform), x_uniform, color='teal')
ax_pdf_y.set_yticklabels([])
ax_pdf_y.set_xticklabels([])

ax_pdf_y.tick_params(axis='x',width =0)
ax_pdf_y.yaxis.set_label_position("right")
ax_pdf_y.yaxis.tick_right()  # Move ticks to the right
ax_pdf_y.set_title(r'$Y \sim \mathcal{U}(0,1)$',fontsize=16,loc='left')
# ax_pdf_y.set_ylabel(r'$Y \sim \mathcal{U}$',fontsize=16)
ax_pdf_y.spines[['bottom','top','right']].set_visible(False)

# Scatter plots para os pontos no gráfico de relação e no gráfico da normal
scat_relation = ax_relation.scatter([], [], edgecolor='None',color='k', alpha=0.2)
scat_pdf_x = ax_pdf_x.scatter([], [], edgecolor='None',color='tab:red', alpha=0.3)
scat_pdf_y = ax_pdf_y.scatter([], [], color='teal', alpha=0.4)

# Inicializa os stems
# stem_x = ax_pdf_x.stem([0], [0], linefmt='k-', markerfmt='ko', basefmt=' ')
stem_x = ax_pdf_x.stem([0], [0], linefmt='tab:red', markerfmt='o', basefmt=' ')
stem_y = ax_pdf_y.stem([0], [0], linefmt='teal', markerfmt='o', basefmt=' ', orientation='horizontal')

# Função de inicialização
def init():
    scat_pdf_x.set_offsets(np.empty((0, 2)))
    scat_pdf_y.set_offsets(np.empty((0, 2)))
    stem_x.markerline.set_data([], [])
    stem_x.stemlines.set_segments([])
    stem_y.markerline.set_data([], [])
    stem_y.stemlines.set_segments([])
    return (scat_relation, scat_pdf_x, scat_pdf_y, stem_x.markerline, stem_x.stemlines,
            stem_y.markerline, stem_y.stemlines)


# Função de atualização para a animação
def update(frame):
    uniform_value = np.random.rand()
    normal_value = transform_to_normal(uniform_value)
    
    # Atualiza scatter no gráfico relação
    x_data_rel = scat_relation.get_offsets()[:, 0] if len(scat_relation.get_offsets()) > 0 else []
    y_data_rel = scat_relation.get_offsets()[:, 1] if len(scat_relation.get_offsets()) > 0 else []
    x_data_rel = np.append(x_data_rel, normal_value)
    y_data_rel = np.append(y_data_rel, uniform_value)
    scat_relation.set_offsets(np.column_stack((x_data_rel, y_data_rel)))
    

    # Atualiza scatter no gráfico PDF Normal
    x_data_pdf = scat_pdf_x.get_offsets()[:, 0] if len(scat_pdf_x.get_offsets()) > 0 else []
    y_data_pdf = scat_pdf_x.get_offsets()[:, 1] if len(scat_pdf_x.get_offsets()) > 0 else []
    
    x_data_pdf = np.append(x_data_pdf, normal_value)
    y_data_pdf = np.append(y_data_pdf, norm.pdf(normal_value))
    scat_pdf_x.set_offsets(np.column_stack((x_data_pdf, y_data_pdf)))
    
   # Atualiza scatter no gráfico PDF Uniforme
    x_data_pdf_y = scat_pdf_y.get_offsets()[:,0] if len(scat_pdf_y.get_offsets()) > 0 else []
    y_data_pdf_y = scat_pdf_y.get_offsets()[:,1] if len(scat_pdf_y.get_offsets()) > 0 else []

    x_data_pdf_y = np.append(x_data_pdf_y, 1)  # Sempre no eixo x=1
    y_data_pdf_y = np.append(y_data_pdf_y, uniform_value)

    scat_pdf_y.set_offsets(np.column_stack((x_data_pdf_y, y_data_pdf_y)))


    # Atualiza stem X (normal)
    stem_x.markerline.set_data([normal_value], [norm.pdf(normal_value)])
    stem_x.stemlines.set_segments([[[normal_value, 0], [normal_value, norm.pdf(normal_value)]]])

    # Atualiza stem Y (uniforme)
    stem_y.markerline.set_data([1], [uniform_value])
    stem_y.stemlines.set_segments([[[0, uniform_value], [1, uniform_value]]])
    return (scat_relation, scat_pdf_x, scat_pdf_y, stem_x.markerline, stem_x.stemlines,
        stem_y.markerline, stem_y.stemlines)

# Criar a animação mais suave
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=100)

# Salvar a animação como GIF
ani.save('animacao_distribuicao_gridspec_final.gif', writer='pillow', fps=10)

plt.show()
