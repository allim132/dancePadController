import serial
import time
import uinput

SERIAL_PORT = '/dev/ttyACM0'   # /dev or /dev/ttyACM0
BAUD_RATE = 115200

PRESS_THRESHOLD = 8.0
RELEASE_THRESHOLD = 20.0
RELEASE_DEBOUNCE_SEC = 0.12

KEYS = ['w', 'a', 's', 'd']

UINPUT_KEYS = {
    'w': uinput.KEY_W,
    'a': uinput.KEY_A,
    's': uinput.KEY_S,
    'd': uinput.KEY_D,
}

device = uinput.Device([
    uinput.KEY_W,
    uinput.KEY_A,
    uinput.KEY_S,
    uinput.KEY_D,
])

state = {
    key: {
        'is_pressed': False,
        'below_since': None
    }
    for key in KEYS
}

def press_key(key: str):
    device.emit(UINPUT_KEYS[key], 1)

def release_key(key: str):
    device.emit(UINPUT_KEYS[key], 0)

def update_key(key, value, now):
    s = state[key]

    # Press immediately when threshold is exceeded
    if not s['is_pressed']:
        if value >= PRESS_THRESHOLD:
            press_key(key)
            s['is_pressed'] = True
            s['below_since'] = None
        return

    # If already pressed, keep holding unless value stays low long enough
    if value > RELEASE_THRESHOLD:
        s['below_since'] = None
        return

    # Value is below release threshold
    if s['below_since'] is None:
        s['below_since'] = now
    elif now - s['below_since'] >= RELEASE_DEBOUNCE_SEC:
        release_key(key)
        s['is_pressed'] = False
        s['below_since'] = None

def release_all_keys():
    for key in KEYS:
        if state[key]['is_pressed']:
            release_key(key)
            state[key]['is_pressed'] = False
            state[key]['below_since'] = None

def open_serial():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)

    # Useful for many Arduino-like boards that reset on serial open
    ser.setDTR(False)
    time.sleep(1)
    ser.reset_input_buffer()
    ser.setDTR(True)
    time.sleep(2)

    return ser

def main():
    serialCom = open_serial()

    try:
        while True:
            raw = serialCom.readline()
            if not raw:
                print("Initializing...")
                continue

            line = raw.decode('utf-8', errors='ignore').strip()
            if not line:
                print("not line")
                continue

            parts = line.split(' ')
            parts = parts[1::2]
            print(parts)
            
            if len(parts) != 4:
                print("hghfgzvbfhjgf ", raw)
                continue

            try:
                values = [abs(float(x)) for x in parts]
            except ValueError:
                print("you suck")
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

if __name__ == "__main__":
    main()
