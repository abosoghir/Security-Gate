#include <Keypad.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>


#define WIFI_SSID "AhmedA33"
#define WIFI_PASSWORD "123456789a"
#define API_KEY "AIzaSyB2ptEHahA0z76PDvUfqdxcTKxLue2ZfIY"
#define DATABASE_URL "https://fir-basic-e2df0-default-rtdb.firebaseio.com/" 
#define USER_EMAIL "ahmedelbnna38@gmail.com"
#define USER_PASSWORD "Ahmed@133"

// Define Firebase Data object
FirebaseData f1;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;

// Password Length
const int Password_Length = 4;

// Character to hold password input
int laserpin = 25;
int buzzerpin = 33;
int ldr=26;
int ldrValue=0;
int ledPin = 22;
// states from mobile app
String laserState;
String buzzerState;
// Password
String Master = "1234";
String Data;

// Variables for attempts
const int max_attempts = 3; // Maximum number of attempts allowed
int attempts = 0; // Counter for incorrect attempts

// Counter for character entries
int data_count = 0;

// Character to hold key input
char customKey;

// Constants for row and column sizes
const byte ROWS = 4;
const byte COLS = 4;

// Array to represent keys on keypad
char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// Connections to Arduino
byte rowPins[ROWS] = {18,5,17,16};
byte colPins[COLS] = {4,0,2,15};

// Create keypad object
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);


void setup() {

  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the user sign in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  // Comment or pass false value when WiFi reconnection will control by your code or third party library e.g. WiFiManager
  Firebase.reconnectNetwork(true);

  // Since v4.4.x, BearSSL engine was used, the SSL buffer need to be set.
  // Large data transmission may require larger RX buffer, otherwise connection issue or data read time out can be occurred.
  f1.setBSSLBufferSize(4096 /* Rx buffer size in bytes from 512 - 16384 */, 1024 /* Tx buffer size in bytes from 512 - 16384 */);

  // Limit the size of response payload to be collected in FirebaseData
  f1.setResponseSize(2048);
  Firebase.begin(&config, &auth);
  Firebase.setDoubleDigits(5);
  config.timeout.serverResponse = 10 * 1000;
  
  pinMode(laserpin, OUTPUT);
  pinMode(buzzerpin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  Serial.println("Enter Password:");
}

void loop() {
   // Firebase.ready() should be called repeatedly to handle authentication tasks.
  if (Firebase.ready() && (millis() - sendDataPrevMillis > 1000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();

   if(Firebase.RTDB.getString(&f1, "/gate_state", &laserState)){
     if(laserState=="LASER OFF")
         digitalWrite(laserpin, 0);
         else{
          digitalWrite(laserpin,1);
         }
   }
   if(Firebase.RTDB.getString(&f1, "/buzzer_state", &buzzerState)){
     if(buzzerState=="BUZZER OFF")
         digitalWrite(buzzerpin, 0);
         else{
          digitalWrite(buzzerpin,1);
         }
   }
  
  // Infinite loop for password attempts
    // Look for keypress
    digitalWrite(laserpin,1);
     ldrValue = analogRead(ldr); // Read the LDR value
   // Serial.println(ldrValue);            // Print the value to the Serial Monitor

    // Control the LED based on the LDR value
    if (ldrValue < 2000) { // Adjust this threshold as needed
        Firebase.RTDB.setString(&f1, "/buzzer_state", "BUZZER ON");
        digitalWrite(ledPin, 1);
        digitalWrite(buzzerpin, 1);
        delay(5000);
        digitalWrite(ledPin, 0);
        digitalWrite(buzzerpin,0); // Turn on the LED
        Firebase.RTDB.setString(&f1, "/buzzer_state", "BUZZER OFF");
    } 

    delay(100); // Delay for stability
    customKey = customKeypad.getKey();
    if (customKey) {
      // Enter keypress into array and increment counter
      Data += customKey;
      Serial.print(Data[data_count]);
      data_count++;
    }

    // See if we have reached the password length
    if (data_count == Password_Length) {
      if (Data == Master) {
        // Correct password
        digitalWrite(laserpin,0);
        Firebase.RTDB.setString(&f1, "/gate_state", "LASER OFF");
        delay(5000);
        digitalWrite(laserpin,1);
        Firebase.RTDB.setString(&f1, "/gate_state", "LASER ON");
        Serial.println("\nPassword correct");
        
        
        Data = "";
        data_count = 0;
        attempts = 0; // Reset attempts
        Serial.println("Enter new password:");
      } else {
        // Incorrect password
        attempts++;
        Serial.println("\nPassword incorrect");
        Data = "";
        data_count = 0;
        digitalWrite(buzzerpin, HIGH);
        delay(1000);
        digitalWrite(buzzerpin, LOW);
        delay(1000);

        if (attempts >= max_attempts) { 
          // Max attempts reached
          Serial.println("Maximum attempts reached. Access denied.");
            digitalWrite(ledPin, 1);
            digitalWrite(buzzerpin, 1); // Keep buzzer on
            Firebase.RTDB.setString(&f1, "/buzzer_state", "BUZZER ON");
            delay(4000);
            digitalWrite(buzzerpin, 0);
            digitalWrite(ledPin, 0);
            Firebase.RTDB.setString(&f1, "/buzzer_state", "BUZZER OFF");
           
        } else {
          // Allow retry
          Serial.println("Try again:");
        }
      }
    }
  }
}