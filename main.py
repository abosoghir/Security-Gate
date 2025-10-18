import firebase_admin
from firebase_admin import credentials, db
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.utils import get_color_from_hex
from threading import Thread



class CircularButton(Button):
    def __init__(self, text, size, pos_hint, on_press, button_bg_color, button_text_color, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = (None, None)
        self.size = size
        self.pos_hint = pos_hint
        self.font_size = 30
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)  # جعل خلفية الزر شفافة
        self.color = button_text_color

        # رسم الشكل الدائري
        with self.canvas.before:
            self.circle_color = Color(*button_bg_color)
            self.circle = Ellipse(pos=self.pos, size=self.size)

        # تحديث شكل الدائرة عند تغيير الحجم أو الموضع
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(on_press=on_press)

    def update_canvas(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

class LaserGateApp(App):
    def build(self):
        # Initialize Firebase
        self.init_firebase()
        
        layout = FloatLayout()

        # Add Background Image
        with layout.canvas.before:

            self.bg = Rectangle(source="background.png", size=layout.size, pos=layout.pos)
            layout.bind(size=self.update_bg, pos=self.update_bg)

        # Notification Label
        self.notification_label = Label(
            text="Notification: None",
            font_size=45,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "y": 0.8},
            color=get_color_from_hex("#1C325B"),
        )
        layout.add_widget(self.notification_label)

        # Circular Buttons
        button_size = (120, 120)
        btn_on = CircularButton(
            text="ON",
            size=(120, 120),
            pos_hint={"center_x": 0.3, "center_y": 0.5},
            on_press=self.turn_on_gate,
            button_bg_color=(1, 1, 1, 1),
            button_text_color=get_color_from_hex("#1C325B"),
        )

        btn_off = CircularButton(
            text="OFF",
            size=(120, 120),
            pos_hint={"center_x": 0.7, "center_y": 0.5},
            on_press=self.turn_off_gate,
            button_bg_color=(1, 1, 1, 1),
            button_text_color=get_color_from_hex("#1C325B"),
        )

        btn_buzzer = CircularButton(
            text="B",
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_press=self.toggle_buzzer,
            button_bg_color=get_color_from_hex("#0B3774"),
            button_text_color=(1, 1, 1, 1)
        )


        layout.add_widget(btn_on)
        layout.add_widget(btn_off)
        layout.add_widget(btn_buzzer)
        
        
          # Initial States
        self.gate_on = False
        self.buzzer_on = False
        self.first_run = True

         # Start Firebase listener in a separate thread
        Thread(target=self.listen_to_firebase, daemon=True).start()

        return layout
    
    
    def init_firebase(self):
        """Initialize Firebase with service account."""
        cred = credentials.Certificate(r"D:\_field_training\fir-basic-e2df0-firebase-adminsdk-bejoq-4094500c61.json")  
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://fir-basic-e2df0-default-rtdb.firebaseio.com/' 
        })
    
    def listen_to_firebase(self):
        """Listen to Firebase changes."""
        ref = db.reference('/')  # الاستماع لجميع البيانات
        ref.listen(self.firebase_update)
    
    def firebase_update(self, event):
        """Handle updates from Firebase."""
        if self.first_run:
            # Skip handling the first update (initial state) and set first_run to False
            self.first_run = False
            return 
       
        if event.path and event.data:
          print(f"Firebase Notification: {event.data}")
          self.notification_label.text = f"{event.data}"
            
    def update_bg(self, *args):
        """Update background when resizing."""
        self.bg.size = self.root.size
        self.bg.pos = self.root.pos

    # Button actions
    def turn_on_gate(self, instance):
        self.gate_on = True
        print("Gate ON")
        db.reference('gate_state').set('LASER ON')  # Send the state to Firebase


    def turn_off_gate(self, instance):
        self.gate_on = False
        print("Gate OFF")
        db.reference('gate_state').set('LASER OFF')  # Send the state to Firebase

        
        
    def toggle_buzzer(self, instance):

            if not self.buzzer_on:
                self.buzzer_on = True
                print("ACTIVATE_BUZZER")
                db.reference('buzzer_state').set('BUZZER ON')  # Send the buzzer state to Firebase

            else:
                self.buzzer_on = False
                print("DEACTIVATE_BUZZER")
                db.reference('buzzer_state').set('BUZZER OFF')  # Send the buzzer state to Firebase




if __name__ == "__main__":
    LaserGateApp().run()
