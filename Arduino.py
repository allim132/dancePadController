import serial
import time
import pydirectinput

SERIAL_PORT = 'COM8'
BAUD_RATE = 115200

PRESS_THRESHOLD = 8.0
RELEASE_THRESHOLD = 5.5

# How long the signal must stay below RELEASE_THRESHOLD before keyUp
RELEASE_DEBOUNCE_SEC = 0.12

KEYS = ['w', 'a', 's', 'd']

state = {
    key: {
        'is_pressed': False,
        'below_since': None
    }
    for key in KEYS
}

def update_key(key, value, now):
    s = state[key]

    # Press immediately when threshold is exceeded
    if not s['is_pressed']:
        if value >= PRESS_THRESHOLD:
            pydirectinput.keyDown(key)
            s['is_pressed'] = True
            s['below_since'] = None
        return

    # If already pressed, do not release instantly
    if value > RELEASE_THRESHOLD:
        s['below_since'] = None
        return

    # Value is below release threshold
    if s['below_since'] is None:
        s['below_since'] = now
    elif now - s['below_since'] >= RELEASE_DEBOUNCE_SEC:
        pydirectinput.keyUp(key)
        s['is_pressed'] = False
        s['below_since'] = None

def release_all_keys():
    for key in KEYS:
        if state[key]['is_pressed']:
            pydirectinput.keyUp(key)
            state[key]['is_pressed'] = False
            state[key]['below_since'] = None

serialCom = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)

serialCom.setDTR(False)
time.sleep(1)
serialCom.reset_input_buffer()
serialCom.setDTR(True)
time.sleep(2)

try:
    while True:
        line = serialCom.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue

        parts = line.split(',')
        if len(parts) != 4:
            continue

        try:
            values = [abs(float(x)) for x in parts]
        except ValueError:
            continue

        now = time.monotonic()

        for key, value in zip(KEYS, values):
            update_key(key, value, now)

        print(dict(zip(KEYS, values)))

except KeyboardInterrupt:
    print("Stopping...")
finally:
    release_all_keys()
    serialCom.close()