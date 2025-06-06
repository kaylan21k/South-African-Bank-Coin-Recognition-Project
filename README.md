# South-African-Bank-Coin-Recognition-Project

**INSTRUCTIONS**

**FOR USE WITH DROIDCAM REQUIREMENTS**
1.Navigate to https://www.dev47apps.com/ and download the required application for pc
2.Install droidcam webcam(classic) for your mobile device's app store

**GENERAL INSTRUCTIONS**
1.Download an extract the Desktop_app zip file
2.Open in VS Code or preferred code editor
3.(Optional download a virtaul enviroment to store libaries and dependencies)
Command for above
Windows:
python -m venv venv
venv\Scripts\activate
Linus:
python3 -m venv venv
source venv/bin/activate

4.Install all requirements using command below:
pip install -r requirements.txt

**Run Application**
python3/python main.py

**Walkthrough**
 After running the main.py file, you are met with the following screen:
![image](https://github.com/user-attachments/assets/054b5d0d-a093-4de3-84c6-aab81090de3f)
As can be seen, you are given 3 selectable options: Wi-Fi, USB and Webcam.

The Wi-Fi option allows you to use the DROIDCAM Mobile application.

The USB option allows you to connect your mobile device via USB:
![image](https://github.com/user-attachments/assets/42097c9c-7ca9-4b66-b7f1-30c76d225a67)

The Webcam option will allow you to use your PC's webcam.
![image](https://github.com/user-attachments/assets/b4bbb40e-5775-486e-ac28-e7c3d9ea9e4f)

For the wifi option using DROIDCAM, you need to enter your WiFi IP that will appear once you open the app on your mobile device, exactly as it appears.
Once you have entered it, click Connect and you can then use your mobile device to view the coin.
You can then click on either 'Start Live Rec' for live recognition or 'Capture & Predict' to take an image of the coin and predict the coin type.
![image](https://github.com/user-attachments/assets/e1e794d9-d393-48e3-a30e-24b519855d6c)
For the Webcam option, you simply need to select it and click connect. It will then use your webcam, and you can hold a coin in front of it.
You can then click on either 'Start Live Rec' for live recognition or 'Capture & Predict' to take an image of the coin and predict the coin type.
![image](https://github.com/user-attachments/assets/119141f3-c0d7-449c-ac57-7c6bc28295f2)

Note: Please hold the coin as close as you can, and allow the camera to focus for a more accurate prediction.


