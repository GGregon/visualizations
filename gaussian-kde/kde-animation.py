import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.animation as animation

# Set plot styles
plt.rcParams.update({'font.family': 'Latin Modern Math'})
plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})
plt.rcParams.update({'xtick.minor.visible': True, 'ytick.minor.visible': True})
plt.rcParams.update({
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12
})

# Parameters
n_total = 100  # Maximum number of observations for animation
x_range_points = 10  # Number of points for KDE evaluation
bandwidth = 0.5  # Fixed bandwidth

# Sample data
x_obs = np.random.normal(3, 1, 1000)  # Larger sample for consistent distribution
x_range_static = np.linspace(min(x_obs) - 1, max(x_obs) + 1, x_range_points)
true_distribution = norm.pdf(np.sort(x_obs), loc=3, scale=1)  # True distribution

# Create figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8), width_ratios=[2, 1], gridspec_kw={'wspace': 0.05})
ax_est = ax1.twinx()

# Function to update animation
def update(frame):
    ax1.clear()
    ax2.clear()
    ax_est.clear()
    
    n = frame + 1  # Increment observations gradually
    x_obs_subset = x_obs[:n]
    x_range = np.linspace(min(x_obs_subset) - 1, max(x_obs_subset) + 1, x_range_points)
    
    pdfs_sum = np.zeros_like(x_range)
    offset = 1
    
    for x in x_obs_subset:
        
        # Observações sendo adicionadas
        ax1.scatter(x, offset, color="violet", edgecolor='blueviolet', s=5, alpha=0.6)      
        
        # Normais centradas nas observações
        pdf_kernel = norm.pdf(x_range, loc=x, scale=bandwidth)
        ax1.plot(x_range, pdf_kernel + offset, color="blueviolet", alpha=0.3, lw=1)         
        
        # Adiciona contribuição do Kernel na observação na KDE
        pdfs_sum += pdf_kernel
        pdf_estimate = pdfs_sum / n
        offset += 1
    
    # Aspectos dos gráficos das observações (ax1)
    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.set_xlim(x_range.min(), x_range.max())
    # Display the number of observations in the top center of ax1
    ax1.text(0.5, 1.05, f"Observations: {n}", 
         transform=ax1.transAxes, ha="center", fontsize=16)

    
    # Plot da KDE e da curva da população
    ax_est.plot(x_range, pdf_estimate, label="KDE", color="blueviolet")
    ax_est.plot(np.sort(x_obs), true_distribution, label="Population", lw=2, color="darkorange")
    ax_est.legend(loc='upper left', fancybox=False, edgecolor='k')
    ax_est.set_yticklabels([])
    ax_est.set_ylim(0,.5)
    ax_est.set_xlim(x_range.min(), x_range.max())  # Ensure KDE plot aligns

    # Compute error
    kde_values = np.interp(x_obs_subset, x_range, pdf_estimate)
    true_values = norm.pdf(x_obs_subset, loc=3, scale=1)
    error = true_values - kde_values
    
    # Compute MSE and RSE
    mse = np.mean(error ** 2)
    rse = np.sqrt(mse)
    text_str = f"MSE: {mse:.3f}\nRSE: {rse:.3f}"
    ax2.text(0.05, 0.95, text_str, transform=ax2.transAxes, fontsize=16, verticalalignment='top')
    
    ax2.scatter(x_obs_subset, error, edgecolor="blueviolet", color='None', s=50, alpha=0.5)
    ax2.axhline(0, color='black', linestyle='dotted')
    ax2.yaxis.set_label_position("right")
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.yaxis.tick_right()
    ax2.set_xlim(min(x_obs) - 1, max(x_obs) + 1)
    ax2.set_ylim(-0.3, 0.3)
    ax2.grid(alpha=0.2, which='major')  


# Create animation
ani = animation.FuncAnimation(fig, update, frames=n_total, interval=50, repeat=False)
# ani.save("animation.gif", writer="pillow", fps=10)

plt.show()