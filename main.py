# main.py
import numpy as np
import matplotlib.pyplot as plt
from utils import plot_histogram, save_table
from analysis import index, get_index_means, calculate_LST
import os

# --- Configuration ---
USE_DUMMY = True   # True = no TIFFs, False = integrate real TIFFs later
INDEX_CHOICE = 1   # 1=NDVI, 2=NDWI, 3=NDBI
OUTPUT_DIR = "output/"
EXCEL_FILE = OUTPUT_DIR + "result.xlsx"
HIST_FILE = OUTPUT_DIR + "histogram.png"

# --- Create output folder if it doesn't exist ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Generate varied dummy data ---
l = []
years = ['2020','2021','2022']
for i, year in enumerate(years):
    # simulate realistic variation per year and band
    arr_g = np.random.rand(50,50) * (0.3 + 0.1*i) + 0.1*i
    arr_r = np.random.rand(50,50) * (0.3 + 0.05*i) + 0.05*i
    arr_n = np.random.rand(50,50) * (0.3 + 0.15*i) + 0.1*i
    arr_s = np.random.rand(50,50) * (0.3 + 0.1*i) + 0.05*i
    arr_t = np.random.rand(50,50) * 10 + 20 + 5*i  # thermal increases per year
    l.append((arr_g, arr_r, arr_n, arr_s, arr_t, 8, year))

# --- Prepare data ---
green, red, nir, swir, thermal, dates = zip(*[(x[0], x[1], x[2], x[3], x[4], x[6]) for x in l])
bands = list(zip(green, red, nir, swir))

# --- Thresholds & Categories ---
if INDEX_CHOICE == 1:
    thresholds = {'No Vegetation':0.0, 'Lowest':0.15, 'Low':0.3, 'Dense':0.6, 'Highest':1.0}
elif INDEX_CHOICE == 2:
    thresholds = {'No Water':0.0, 'Lowest':0.15, 'Less':0.3, 'Dense':0.6, 'Highest':1.0}
else:
    thresholds = {'No Built-up':0.0, 'Lowest':0.15, 'Less':0.3, 'Dense':0.6, 'Highest':1.0}
categories = list(thresholds.keys())

# --- Compute indices ---
indices = []
for g,r,n,s in bands:
    if INDEX_CHOICE == 1:
        indices.append(index(n,r))
    elif INDEX_CHOICE == 2:
        indices.append(index(g,s))
    else:
        indices.append(index(s,n))

# --- Convert indices arrays to percentage per category ---
percent_all = []
for arr in indices:
    arr_flat = arr.flatten()
    total = arr_flat.size
    cat_percent = []
    thresh_vals = list(thresholds.values())
    for i, val in enumerate(thresh_vals):
        lower = val
        upper = thresh_vals[i+1] if i+1 < len(thresh_vals) else 1.0
        count = np.sum((arr_flat >= lower) & (arr_flat < upper))
        cat_percent.append(count / total * 100)
    percent_all.append(cat_percent)

# --- Save table & plot histogram ---
save_table(percent_all, thresholds, dates, categories, EXCEL_FILE)
plot_histogram(percent_all, dates, categories, HIST_FILE)

# --- Compute LST & correlation plots ---
lst_list = [calculate_LST(t) for t in thermal]
ndvi_list, ndwi_list, ndbi_list = [], [], []
for g,r,n,s in bands:
    ndvi, ndwi, ndbi = get_index_means(g,r,n,s)
    ndvi_list.append(ndvi)
    ndwi_list.append(ndwi)
    ndbi_list.append(ndbi)

fig, axs = plt.subplots(1,3,figsize=(15,5))
axs[0].scatter(lst_list, ndvi_list, color='green'); axs[0].set_title('LST vs NDVI')
axs[1].scatter(lst_list, ndwi_list, color='blue'); axs[1].set_title('LST vs NDWI')
axs[2].scatter(lst_list, ndbi_list, color='red'); axs[2].set_title('LST vs NDBI')
for ax in axs:
    ax.grid(True)
plt.show()
