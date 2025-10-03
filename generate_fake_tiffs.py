import numpy as np
import rasterio
import os

# --- Configuration ---
OUTPUT_DIR = "tiff_data/"
YEARS = ["2020", "2021", "2022"]
BANDS = ["green", "red", "nir", "swir", "thermal"]

# --- Create folder if not exists ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Generate fake TIFFs ---
for year in YEARS:
    for band in BANDS:
        # create random 5x5 array for demo
        arr = np.random.rand(5,5).astype(np.float32)  # values 0-1

        file_path = os.path.join(OUTPUT_DIR, f"{band}_{year}.tif")

        with rasterio.open(
            file_path, 'w',
            driver='GTiff',
            height=arr.shape[0],
            width=arr.shape[1],
            count=1,
            dtype=arr.dtype
        ) as dst:
            dst.write(arr, 1)

print("Fake TIFF files created in folder:", OUTPUT_DIR)
