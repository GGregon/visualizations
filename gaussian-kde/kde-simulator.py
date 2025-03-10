import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.widgets import Slider

# plt.rcParams['text.usetex'] = True
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


# Initial parameters
n_total = 1000  # Total number of observations
n_init = 5  # Start with a small subset
x_range_init = 10  # Number of points for KDE evaluation
bandwidth_init = 0.5  # Bandwidth

# Sample initial data (fixed for updates)
x_obs = np.random.normal(3, 1, n_total)
x_range_static = np.linspace(min(x_obs) - 1, max(x_obs) + 1, x_range_init)  # Static range for true distribution
true_distribution = norm.pdf(np.sort(x_obs), loc=3, scale=1)  # Static true distribution

# Create figure and axes
fig, (ax2, ax3) = plt.subplots(1,2,figsize=(15, 8), width_ratios=[2,1],gridspec_kw={'wspace': 0.05})
plt.subplots_adjust(bottom=0.25)
ax_est = ax2.twinx()  # Create secondary axis for estimated PDF

# Define the update function
def update(val):
        
    # Temporarily disable event listeners
    slider_n.eventson = False
    slider_x_range.eventson = False
    slider_bandwidth.eventson = False
    
    ax2.clear()
    ax3.clear()
    ax_est.clear()
    
    # Get slider values
    n = int(slider_n.val)  # Number of observations to use
    x_range_points = int(slider_x_range.val)
    bandwidth = slider_bandwidth.val
    
    # Use a subset of the initial sample points
    x_obs_subset = x_obs[:n]
    x_range = np.linspace(min(x_obs_subset) - 1, max(x_obs_subset) + 1, x_range_points)
    
    pdfs_sum = np.zeros_like(x_range)
    offset = 1
    color = 'tab:blue'
    
    for x in x_obs_subset:
        ax2.scatter(x, offset, color="violet", edgecolor='blueviolet',s=5,alpha=0.6)
                
        pdf_kernel = norm.pdf(x_range, loc=x, scale=bandwidth)
        pdfs_sum += pdf_kernel
        pdf_estimate = pdfs_sum / n
        
        ax2.plot(x_range, pdf_kernel + offset, color="blueviolet", alpha=0.3, lw=1)
        offset += 1
    
    ax_est.plot(x_range, pdf_estimate, color="blueviolet", label="KDE")
    ax_est.plot(np.sort(x_obs), true_distribution, label="Population", lw=2, color="darkorange")
    ax_est.legend(loc='upper left',fancybox=False,edgecolor='k')
    
    # Compute error
    kde_values = np.interp(x_obs_subset, x_range, pdf_estimate)
    true_values = norm.pdf(x_obs_subset, loc=3, scale=1)
    error = true_values - kde_values
    
    # Compute MSE and RSE
    mse = np.mean(error ** 2)
    rse = np.sqrt(mse)

    # Display text in the upper-left corner of ax3
    text_str = f"MSE: {mse:.3f}\nRSE: {rse:.3f}"
    ax3.text(0.05, 0.95, text_str, transform=ax3.transAxes, fontsize=16,
            verticalalignment='top')


    ax3.scatter(x_obs_subset, error, edgecolor="blueviolet", color='None',s=50, alpha=0.5)
    ax3.axhline(0, color='black', linestyle='dotted')
    ax3.yaxis.set_label_position("right")
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.yaxis.tick_right()
    ax3.set_xlim(min(x_obs) - 1, max(x_obs) + 1)  # Fix x-axis range
    ax3.set_ylim(-0.3, 0.3)  # Adjust this range based on expected error values
    ax3.grid(alpha=0.2,which='major')
    
    ax2.set_xlim(x_range.min(), x_range.max())
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax_est.set_yticklabels([])
    
    fig.canvas.draw_idle()
    # Re-enable event listeners
    slider_n.eventson = True
    slider_x_range.eventson = True
    slider_bandwidth.eventson = True


# Create sliders
axcolor = 'lightgoldenrodyellow'
ax_n = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_x_range = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor=axcolor)
ax_bandwidth = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor=axcolor)

slider_n = Slider(ax_n, 'Observations', valmin=n_init, valmax=50, valinit=n_init, valstep=1)
slider_x_range = Slider(ax_x_range, 'X-Range Points', valmin=x_range_init, valmax=200, valinit=x_range_init, valstep=1)
slider_bandwidth = Slider(ax_bandwidth, 'Bandwidth', valmin=0.1, valmax=2.0, valinit=bandwidth_init, valstep=0.05)

slider_n.on_changed(update)
slider_x_range.on_changed(update)
slider_bandwidth.on_changed(update)


update(None)  # Initial plot
plt.show()