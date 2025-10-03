import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- Ensure output directory exists ---
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --- Normalize array to 0-1 ---
def normalize(arr):
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    if arr_max - arr_min == 0:
        return np.zeros_like(arr)
    return (arr - arr_min) / (arr_max - arr_min)

# --- Save table as Excel ---
def save_table(percent_all, thresholds, dates, categories, file_path):
    ensure_dir(os.path.dirname(file_path))
    # convert list of arrays to percentages
    data = []
    for i, date in enumerate(dates):
        row = [np.mean(percent_all[i])] * len(categories)  # dummy uniform percentage
        data.append(row)
    df = pd.DataFrame(data, columns=categories)
    df.insert(0, "Date", dates)
    df.to_excel(file_path, index=False)
    print(f"Saved Excel table at: {file_path}")

# --- Plot histogram ---
def plot_histogram(percent_all, dates, categories, file_path):
    ensure_dir(os.path.dirname(file_path))
    percent_all = [np.mean(p) for p in percent_all]  # average for dummy
    ind = np.arange(len(dates))
    width = 0.35

    fig, ax = plt.subplots()
    for i, cat in enumerate(categories):
        bottom = np.zeros(len(dates))
        ax.bar(ind, percent_all, width, bottom=bottom, label=cat)
    ax.set_xticks(ind)
    ax.set_xticklabels(dates)
    ax.set_ylabel('Percentage')
    ax.set_title('Dummy Histogram')
    ax.legend()
    plt.savefig(file_path)
    plt.show()
    print(f"Saved histogram at: {file_path}")
