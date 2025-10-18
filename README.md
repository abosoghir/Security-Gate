Security Gate

A simple gate security project with laser intrusion detection and keypad access.

Description

This project implements a security gate protected by a laser beam. If someone attempts to enter by crossing the gate and interrupts the laser, the system will trigger an alarm and send a mobile notification reporting an unauthorized entry attempt. The gate also includes a keypad for entering a passcode. Users have up to three attempts to enter the correct passcode; after three consecutive wrong attempts the system triggers the alarm, indicating a possible breach.

Features

Laser-based intrusion detection (interrupting the laser triggers the alarm).

Keypad for passcode entry.

Mobile notification when an intrusion or unauthorized access occurs.

Three-attempt limit for the keypad; three wrong attempts trigger the alarm.

Components (example)

Microcontroller (Arduino / ESP32 / Raspberry Pi Pico — specify your board)

Laser emitter and receiver (photoresistor or photodiode)

Buzzer or siren for alarm

Keypad (3x4 or 4x4)

Optional: GSM module or Wi‑Fi module for mobile notifications

Power supply and wiring

Replace or add components according to your actual hardware.

How it works

The laser beam forms a line across the gate between the emitter and the receiver.

When the beam is uninterrupted, the system remains in a safe state.

If the beam is interrupted (someone passes through), the system immediately triggers the alarm and sends a mobile notification.

If a user tries to enter using the keypad, the system reads the passcode:

If the passcode is correct: access is granted and no alarm is triggered.

If the passcode is incorrect: the user may try again.

After three incorrect attempts in a row, the system triggers the alarm and sends a notification.

Installation & Setup (general guidance)

Clone the repository.

Open the microcontroller project in your IDE (Arduino IDE, PlatformIO, etc.).

Connect the laser emitter to a digital output and the receiver to an analog/digital input, depending on the sensor you use.

Wire the keypad to the appropriate digital pins and configure the library settings.

Connect the alarm (buzzer / relay) to a digital output.

Set up mobile notifications:

If using GSM, configure the SIM card and AT commands.

If using Wi‑Fi, configure your network credentials and a cloud notification method (Firebase, HTTP webhook, etc.).

Upload the code to the microcontroller.

Configuration

Edit the passcode in the source code if needed.

Configure notification credentials locally (do not commit private keys or service account JSON files to the repository).

Important: keep any service credentials (Firebase keys, GSM API tokens, etc.) out of the public repository. Add them to .gitignore and load them from environment variables or a local configuration file.

Usage

Power the system and ensure the laser beam is aligned with the receiver.

Use the keypad to enter the passcode. On success, the system allows access.

If the laser is broken or the keypad triggers three wrong attempts, an alarm sounds and a notification is sent.

Troubleshooting

If the alarm triggers unexpectedly, check laser alignment and ambient light interference.

Make sure the keypad wiring and scanning code match your keypad's pinout.

Verify the notification module (GSM/Wi‑Fi) has proper network connectivity.

License

Specify your preferred license (e.g., MIT). If you are unsure, add an LICENSE file.

Contact

For questions or improvements, open an issue or submit a pull request.
