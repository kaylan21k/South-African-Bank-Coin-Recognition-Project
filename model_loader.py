import joblib
import json
from pathlib import Path
from kivy.logger import Logger

MODEL_DIR_NAME = 'models_final'
try:
    from kivy.app import App
    if App.get_running_app(): 
        APP_ROOT = Path(App.get_running_app().directory)
        MODEL_DIR = APP_ROOT / MODEL_DIR_NAME
        if not MODEL_DIR.exists():
             MODEL_DIR = Path(__file__).parent / MODEL_DIR_NAME
    else: 
        MODEL_DIR = Path(__file__).parent / MODEL_DIR_NAME
except Exception:
    MODEL_DIR = Path(__file__).parent / MODEL_DIR_NAME


TYPE_MODEL_FILENAME = "random_forest_type_model.joblib"
SIDE_MODEL_FILENAME = "random_forest_side_model.joblib"
SCALER_FILENAME = "scaler.joblib"
FEATURE_NAMES_FILENAME = "feature_names.json"

SCALER_PATH = MODEL_DIR / SCALER_FILENAME
FEATURE_NAMES_PATH = MODEL_DIR / FEATURE_NAMES_FILENAME
TYPE_MODEL_PATH = MODEL_DIR / TYPE_MODEL_FILENAME
SIDE_MODEL_PATH = MODEL_DIR / SIDE_MODEL_FILENAME


def load_prediction_assets():
    """Loads the scaler, feature names, and trained models."""
    Logger.info(f"ModelLoader: Attempting to load assets from: {MODEL_DIR}")
    assets = {'scaler': None, 'feature_names': None, 'type_clf': None, 'side_clf': None}
    all_loaded = True

    if not MODEL_DIR.exists():
        Logger.error(f"ModelLoader: CRITICAL - Model directory not found at {MODEL_DIR}")
        return None, None, None, None

    try:
        assets['scaler'] = joblib.load(SCALER_PATH)
        Logger.info(f"ModelLoader: Scaler loaded from {SCALER_PATH}")
    except FileNotFoundError:
        Logger.error(f"ModelLoader: CRITICAL - Scaler file not found at {SCALER_PATH}")
        all_loaded = False
    except Exception as e:
        Logger.error(f"ModelLoader: CRITICAL - Error loading scaler: {e}")
        all_loaded = False

    try:
        with open(FEATURE_NAMES_PATH, 'r') as f:
            assets['feature_names'] = json.load(f)
        Logger.info(f"ModelLoader: Feature names loaded from {FEATURE_NAMES_PATH}")
    except FileNotFoundError:
        Logger.error(f"ModelLoader: CRITICAL - Feature names file not found at {FEATURE_NAMES_PATH}")
        all_loaded = False
    except Exception as e:
        Logger.error(f"ModelLoader: CRITICAL - Error loading feature names: {e}")
        all_loaded = False

    try:
        assets['type_clf'] = joblib.load(TYPE_MODEL_PATH)
        Logger.info(f"ModelLoader: Type classifier ('{TYPE_MODEL_FILENAME}') loaded from {TYPE_MODEL_PATH}")
    except FileNotFoundError:
        Logger.error(f"ModelLoader: CRITICAL - Type model file ('{TYPE_MODEL_FILENAME}') not found at {TYPE_MODEL_PATH}")
        all_loaded = False
    except Exception as e:
        Logger.error(f"ModelLoader: CRITICAL - Error loading type model: {e}")
        all_loaded = False

    try:
        assets['side_clf'] = joblib.load(SIDE_MODEL_PATH)
        Logger.info(f"ModelLoader: Side classifier ('{SIDE_MODEL_FILENAME}') loaded from {SIDE_MODEL_PATH}")
    except FileNotFoundError:
        Logger.error(f"ModelLoader: CRITICAL - Side model file ('{SIDE_MODEL_FILENAME}') not found at {SIDE_MODEL_PATH}")
        all_loaded = False
    except Exception as e:
        Logger.error(f"ModelLoader: CRITICAL - Error loading side model: {e}")
        all_loaded = False

    if all_loaded:
        Logger.info("ModelLoader: All prediction assets loaded successfully.")
        return assets['scaler'], assets['feature_names'], assets['type_clf'], assets['side_clf']
    else:
        Logger.error("ModelLoader: One or more prediction assets failed to load.")
        return None, None, None, None


if __name__ == '__main__':
    print("Testing asset loading (run this from main.py context or ensure paths are correct)...")
    s, fn, tc, sc = load_prediction_assets()
    if s and fn and tc and sc:
        print(f"Test load successful. Number of features expected: {len(fn)}")
    else:
        print("Test load failed. Check paths, file existence in 'models_final' and error logs.")
