import numpy as np
from utils import normalize

# --- Compute indices (dummy) ---
def index(b1, b2):
    """Compute dummy index from two bands"""
    arr = np.zeros_like(b1)
    # For dummy, just subtract one from the other and normalize
    arr = normalize(b1 - b2)
    return arr

def get_index_means(g, r, n, s):
    """Return mean NDVI, NDWI, NDBI for dummy arrays"""
    ndvi = np.mean(index(n, r))
    ndwi = np.mean(index(g, s))
    ndbi = np.mean(index(s, n))
    return ndvi, ndwi, ndbi

def calculate_LST(thermal):
    """Dummy Land Surface Temperature"""
    return np.mean(thermal) * 50 + 20  # just a fake temp between 20-70
