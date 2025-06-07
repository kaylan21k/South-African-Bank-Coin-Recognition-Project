# South African Bank Coin Recognition Project

A computer vision system for accurate recognition and classification of South African bank coins using deep learning techniques.

## Model Training Notebook

**The model training notebook is a crucial component of this project. It contains the complete pipeline for developing the coin recognition system, including:**

- Processing 714 original coin images
- Performing multiple augmentations to increase dataset size to 7,854 images
- Image preprocessing and enhancement
- Image segmentation
- Feature extraction
- Coin classification (both denomination and side)
- Model comparison and selection

**Access the notebook here:** [COMP702_PROJECT.ipynb](https://stuukznac-my.sharepoint.com/:u:/g/personal/221011891_stu_ukzn_ac_za/EeHjMwCz_6ZDp5CFJLoUwpEBM4FjmUMieBCVFRQb7VHkFA?e=srrRMW)

**Original images required by notebook(COMP702_PROJECT.ipynb) here:** [original_coins.zip](https://stuukznac-my.sharepoint.com/:u:/g/personal/221011891_stu_ukzn_ac_za/EWiUNrIe1m1Bn1OdoFhpce0BQzscKWbYdvpc40XVhunh9w?e=hQOszK)

## Important Note

The application requires model files located in the `models_final.zip` archive. You must extract these files before running the application.

**1. Unzip the Archive**

Open a terminal or command prompt in the project's root directory and use the appropriate command for your operating system.

* **On macOS or Linux:**
    ```bash
    unzip models_final.zip
    ```

* **On Windows (using PowerShell):** The `tar` command is generally more reliable for avoiding nested directories.
    ```powershell
    tar -xf models_final.zip
    ```

**2. Verify the Directory Structure**

After unzipping, you must have a single `models_final` directory containing the model files. Please verify that your folder structure looks like the Project Structure Below.

## Project Structure

```
South-African-Bank-Coin-Recognition-Project/
├── README.md
├── image_processing_pipeline.py
├── main.py
├── models_final.py (After Unzipped)
│   ├── feature_names.json
│   ├── random_forest_side_model.joblib
│   ├── random_forest_type_model.joblib
│   ├── scaler.joblib
├── model_loader.py
├── models_final.zip (must be unzipped before running)
└── requirements.txt
```

## Installation Instructions

### Prerequisites
- Python 3.7 or higher
- For mobile camera integration: DROIDCAM application

### Setup

1. Clone or download this repository (Make sure the extracted South-African-Bank-Coin-Recognition-Project/ folder contains the Project files directly, not another nested South-African-Bank-Coin-Recognition-Project/ directory inside it, else follow instructions of how to unzip the `models_final.zip` file in the Important Note section for the main Project file that you downloaded. In the end you need to have the same structure specified in the Project Structure section)
2. **Important:** Unzip the `models_final.zip` file in the same directory (Make sure the extracted models_final/ folder contains the model files directly, not another nested models_final/ directory inside it)
3. Open the project in VS Code or your preferred code editor
4. Ensure code editor is in the South-African-Bank-Coin-Recognition-Project folder that contains all project files
5. (Optional) Create a virtual environment:

   **Windows:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Ubuntu:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

6. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Ensure code editor is in the South-African-Bank-Coin-Recognition-Project folder that contains all project files
2. Ensure you've unzipped the `models_final.zip` file (Make sure the extracted models_final/ folder contains the model files directly, not another nested models_final/ directory inside it)
3. Run the application:
   ```
   python main.py
   ```
   or
   ```
   python3 main.py
   ```

## Using the Application

After running the main.py file, you'll see three connection options:

![image](https://github.com/user-attachments/assets/054b5d0d-a093-4de3-84c6-aab81090de3f)

### Wi-Fi Option (DROIDCAM)
- Install DROIDCAM Webcam (Classic) on your mobile device
- Open the app on your mobile device and note the WiFi IP
- Select "Wi-Fi" in the application, enter the IP, and click "Connect"
- Use "Start Live Rec" for live recognition or "Capture & Predict" for single image recognition

### USB Option
- Connect your mobile device via USB
- Select "USB" in the application and click "Connect"
- Use "Start Live Rec" or "Capture & Predict" for recognition

### Webcam Option
- Select "Webcam" in the application and click "Connect"
- Use "Start Live Rec" or "Capture & Predict" for recognition

### Live Rec Capture
![image](https://github.com/user-attachments/assets/e1e794d9-d393-48e3-a30e-24b519855d6c)

### Capture & Predict
![image](https://github.com/user-attachments/assets/119141f3-c0d7-449c-ac57-7c6bc28295f2)


## Tips for Best Results

- Hold the coin as close to the camera as possible while maintaining focus
- Allow the camera to focus for more accurate predictions
- Ensure good lighting conditions


