# South African Bank Coin Recognition Project

A computer vision system for accurate recognition and classification of South African bank coins using deep learning techniques.

## Important Note

Before running the application, you must unzip the `models_final.zip` file as the main.py requires these model files to run.

## Project Structure

```
South-African-Bank-Coin-Recognition-Project/
├── README.md
├── image_processing_pipeline.py
├── main.py
├── model_loader.py
├── models_final.zip (must be unzipped before running)
└── requirements.txt
```

## Model Training Notebook

The model training notebook is a crucial component of this project. It contains the complete pipeline for developing the coin recognition system, including:

- Processing 714 original coin images
- Performing multiple augmentations to increase dataset size to 7,854 images
- Image preprocessing and enhancement
- Image segmentation
- Feature extraction
- Coin classification (both denomination and side)
- Model comparison and selection

**Access the notebook here:** [COMP702_PROJECT.ipynb](https://stuukznac-my.sharepoint.com/:u:/g/personal/221011891_stu_ukzn_ac_za/EeHjMwCz_6ZDp5CFJLoUwpEBM4FjmUMieBCVFRQb7VHkFA?e=srrRMW)

## Installation Instructions

### Prerequisites
- Python 3.7 or higher
- For mobile camera integration: DROIDCAM application

### Setup

1. Clone or download this repository
2. **Important:** Unzip the `models_final.zip` file in the same directory
3. Open the project in VS Code or your preferred code editor
4. (Optional) Create a virtual environment:

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

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Ensure you've unzipped the `models_final.zip` file
2. Run the application:
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
- Download DROIDCAM from https://www.dev47apps.com/ for your PC
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

###Live Rec
![image](https://github.com/user-attachments/assets/e1e794d9-d393-48e3-a30e-24b519855d6c)

###Capture & Predict
![image](https://github.com/user-attachments/assets/119141f3-c0d7-449c-ac57-7c6bc28295f2)


## Tips for Best Results

- Hold the coin as close to the camera as possible while maintaining focus
- Allow the camera to focus for more accurate predictions
- Ensure good lighting conditions


