import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
import cv2
import numpy as np

from model_loader import load_prediction_assets
from image_processing_pipeline import run_recognition_pipeline

class CoinRecognizerApp(App):
    def build(self):
        self.title = "SA Coin Recognizer"
        self.assets_loaded = False
        self.scaler, self.feature_names, self.type_clf, self.side_clf = None, None, None, None
        self.app_mode = 'connecting'
        self.capture = None
        self.processing_active = False
        self.frame_to_process = None
        self.root_layout = BoxLayout(orientation='vertical')
        self.setup_connection_screen()
        return self.root_layout

    def setup_connection_screen(self):
        self.root_layout.clear_widgets()
        conn_layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        title_label = Label(text="Select Camera Source", font_size='28sp', size_hint_y=None, height=50)
        mode_box = GridLayout(cols=3, size_hint_y=None, height=40)
        wifi_box = BoxLayout()
        self.cb_wifi = CheckBox(group='conn_mode', active=True)
        self.cb_wifi.bind(active=self.update_connection_hint)
        wifi_box.add_widget(self.cb_wifi)
        wifi_box.add_widget(Label(text="Wi-Fi"))
        usb_box = BoxLayout()
        self.cb_usb = CheckBox(group='conn_mode')
        self.cb_usb.bind(active=self.update_connection_hint)
        usb_box.add_widget(self.cb_usb)
        usb_box.add_widget(Label(text="USB"))
        webcam_box = BoxLayout()
        self.cb_webcam = CheckBox(group='conn_mode')
        self.cb_webcam.bind(active=self.update_connection_hint)
        webcam_box.add_widget(self.cb_webcam)
        webcam_box.add_widget(Label(text="Webcam"))
        mode_box.add_widget(wifi_box)
        mode_box.add_widget(usb_box)
        mode_box.add_widget(webcam_box)
        self.ip_input = TextInput(hint_text='Enter Phone Wi-Fi IP', multiline=False, font_size='22sp', size_hint_y=None, height=60)
        connect_button = Button(text="Connect", font_size='22sp', on_press=self.attempt_connection, size_hint_y=None, height=60)
        self.conn_status_label = Label(text="Select a connection mode.", font_size='18sp', size_hint_y=None, height=40)
        for widget in [Label(size_hint_y=0.2), title_label, mode_box, self.ip_input, connect_button, self.conn_status_label, Label(size_hint_y=0.3)]:
            conn_layout.add_widget(widget)
        self.root_layout.add_widget(conn_layout)
        self.update_connection_hint(self.cb_wifi, True)

    def update_connection_hint(self, checkbox, value):
        if value:
            if checkbox == self.cb_wifi: self.ip_input.disabled = False; self.ip_input.text = ""; self.ip_input.hint_text = "Enter Phone Wi-Fi IP"; self.conn_status_label.text = "Enter IP from phone app."
            elif checkbox == self.cb_usb: self.ip_input.disabled = False; self.ip_input.text = ""; self.ip_input.hint_text = "Enter IP from DroidCam PC Client"; self.conn_status_label.text = "Connect via USB. Get IP from PC client."
            elif checkbox == self.cb_webcam: self.ip_input.disabled = True; self.ip_input.text = "N/A"; self.ip_input.hint_text = "IP address not needed"; self.conn_status_label.text = "Will use the default PC camera."

    def attempt_connection(self, instance):
        source = None
        if self.cb_wifi.active or self.cb_usb.active:
            ip_address = self.ip_input.text.strip()
            if not ip_address: self.conn_status_label.text = "[color=ff3333]IP address is required.[/color]"; self.conn_status_label.markup = True; return
            source = f'http://{ip_address}:4747/video'; self.conn_status_label.text = f"Connecting to {source}..."
        elif self.cb_webcam.active: source = 0; self.conn_status_label.text = "Opening built-in webcam..."
        if source is not None and self.init_camera(source): Logger.info(f"App: Camera connection to '{source}' successful."); self.load_models_and_setup_main_screen()
        else: Logger.error(f"App: Camera connection to '{source}' failed."); self.conn_status_label.text = "[color=ff3333]Connection failed.[/color]"; self.conn_status_label.markup = True

    def init_camera(self, source):
        try:
            if isinstance(source, int): self.capture = cv2.VideoCapture(source);_ = self.capture.isOpened() or setattr(self, 'capture', cv2.VideoCapture(1))
            elif isinstance(source, str): self.capture = cv2.VideoCapture(source)
            else: return False
            return self.capture.isOpened()
        except Exception as e: Logger.error(f"App: Camera init exception: {e}"); self.capture = None; return False

    def load_models_and_setup_main_screen(self):
        self.scaler, self.feature_names, self.type_clf, self.side_clf = load_prediction_assets()
        if all([self.scaler, self.feature_names, self.type_clf, self.side_clf]): self.assets_loaded = True; self.setup_main_app_screen()

    def setup_main_app_screen(self):
        self.root_layout.clear_widgets()
        self.app_mode = 'live'
        main_layout = self.create_main_app_layout()
        self.root_layout.add_widget(main_layout)
        Clock.schedule_interval(self.update_camera_feed, 1.0 / 30.0)
        Clock.schedule_interval(self.process_frame_if_active, 0.5)

    def create_main_app_layout(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.camera_view = KivyImage(fit_mode="fill")
        layout.add_widget(self.camera_view)
        self.status_label = Label(text="Ready.", size_hint_y=None, height=35)
        self.type_label = Label(text="Coin Type: N/A", font_size='20sp', size_hint_y=None, height=40)
        self.side_label = Label(text="Coin Side: N/A", font_size='20sp', size_hint_y=None, height=40)
        self.confidence_label = Label(text="Confidence: N/A", size_hint_y=None, height=30)
        for widget in [self.status_label, self.type_label, self.side_label, self.confidence_label]: layout.add_widget(widget)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        self.live_button = Button(text="Start Live Rec", on_press=self.toggle_processing)
        self.capture_button = Button(text="Capture & Predict", on_press=self.capture_and_predict)
        self.back_button = Button(text="Back to Live", on_press=self.go_back_to_live, disabled=True)
        for widget in [self.live_button, self.capture_button, self.back_button]: button_box.add_widget(widget)
        layout.add_widget(button_box)
        return layout

    def display_frame(self, frame):
        buf = cv2.flip(frame, 0).tobytes(); texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr'); texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte'); self.camera_view.texture = texture

    def capture_and_predict(self, instance):
        Logger.info("APP: 'Capture & Predict' button pressed.")
        if self.frame_to_process is None: return
        self.app_mode = 'captured'
        self.processing_active = False
        self.live_button.disabled = True
        self.capture_button.disabled = True
        self.back_button.disabled = False
        self.status_label.text = "Processing captured image..."
        processed_image = self.run_prediction_pipeline(self.frame_to_process)
        if processed_image is not None: self.display_frame(processed_image)
    
    def _reset_prediction_labels(self):
        self.type_label.text = "Coin Type: N/A"
        self.side_label.text = "Coin Side: N/A"
        self.confidence_label.text = "Confidence: N/A"

    def go_back_to_live(self, instance):
        Logger.info("APP: 'Back to Live' button pressed.")
        self.app_mode = 'live'
        self.live_button.disabled = False
        self.capture_button.disabled = False
        self.back_button.disabled = True
        self.status_label.text = "Ready."
        self._reset_prediction_labels()

    # <<< MODIFIED: This function has the core changes. ---
    def run_prediction_pipeline(self, frame):
        if not self.assets_loaded:
            self.status_label.text = "Error: AI Models are not loaded."
            return None
        
        Logger.info("PIPELINE: Running prediction...")
        results, visualized_frame = run_recognition_pipeline(frame.copy(), self.scaler, self.type_clf, self.side_clf, self.feature_names)
        
        #Logging of the results dictionary.
        Logger.info(f"PIPELINE RESULTS: {results}")

        if results:
            if results.get('error'):
                self.status_label.text = f"Status: {results['error']}"
                self._reset_prediction_labels()
            else:
                self._reset_prediction_labels() 
                
                self.status_label.text = "Prediction Complete" if self.app_mode == 'captured' else "Recognizing..."
                self.type_label.text = f"Coin Type: {results['coin_type']}"
                self.side_label.text = f"Coin Side: {results['coin_side']}"
                self.confidence_label.text = f"Conf: T {results['type_confidence']:.0f}%, S {results['side_confidence']:.0f}%"
        else:
            self.status_label.text = "Status: Pipeline returned no results."
            self._reset_prediction_labels()
            
        return visualized_frame

    def toggle_processing(self, instance):
        self.processing_active = not self.processing_active
        instance.text = "Stop Live Rec" if self.processing_active else "Start Live Rec"
        self.capture_button.disabled = self.processing_active
        if not self.processing_active:
            self.status_label.text = "Live recognition paused."
            self._reset_prediction_labels()

    def update_camera_feed(self, dt):
        if self.app_mode != 'live' or not self.capture or not self.capture.isOpened(): return
        ret, frame = self.capture.read()
        if ret:
            self.frame_to_process = frame
            if not self.processing_active: self.display_frame(self.frame_to_process)

    def process_frame_if_active(self, dt):
        if self.processing_active and self.app_mode == 'live' and self.frame_to_process is not None:
            processed_image = self.run_prediction_pipeline(self.frame_to_process)
            if processed_image is not None: self.display_frame(processed_image)

    def on_stop(self):
        if self.capture: self.capture.release()

if __name__ == '__main__':
    CoinRecognizerApp().run()

