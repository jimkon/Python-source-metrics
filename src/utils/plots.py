import matplotlib.pyplot as plt

import numpy as np


def plot_hist_and_quartiles(data, bins=30):
    plt.hist(data, bins=bins, orientation="horizontal")

    plt.axhline(data.mean(), color='0.05', linewidth=1, label=f"mean: {data.mean():.2f}")

    plt.axhline(np.quantile(data, .25), color='0.25', linewidth=1, label=f"q 0.25")
    plt.axhline(np.quantile(data, .75), color='0.25', linewidth=1, label=f"q 0.75")

    plt.axhline(np.quantile(data, .05), color='0.45', linewidth=1, label=f"q 0.05")
    plt.axhline(np.quantile(data, .95), color='0.45', linewidth=1, label=f"q 0.95")

