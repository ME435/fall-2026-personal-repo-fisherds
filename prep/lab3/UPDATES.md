# Lab 3 Notes Updates

Things to change in the Day 1 (serial menu) and Day 2 (Flask) Google Docs so they match the tested code in `prep/lab3`. As of 2026-09-24, all of it works on the Pi with the FakePlateloader Arduino.


## Folder layout

```
prep/lab3/
├── plateloader.py        # PlateLoader class only (shared by both apps)
├── serial_menu.py        # Day 1: terminal menu
├── serial_server.py      # Day 2: Flask server
├── learning_serial.py
└── public/
    ├── index.html        # Day 2: web page
    └── main.js
```

`serial_menu.py` and `serial_server.py` sit in the same folder as `plateloader.py`, so `from plateloader import PlateLoader` just works. Python puts the running script's folder on the import path.

---

## Day 1: what to change

- [ ] **Split `plateloader.py` into two files.** The class stays in `plateloader.py`, and the menu (the old `if __name__ == "__main__":` block) moves to `serial_menu.py`.
- [ ] **Default port:** change `/dev/cu.usbmodem21101` (Mac) to `/dev/ttyACM0` (Pi). Also pass the port in explicitly: `PlateLoader(port="/dev/ttyACM0")` and then `connect()`.
- [ ] **`connect()`** now prints `Connected to {self.port}`.
- [ ] **Timeout check in `send_command`:** if `readline()` returns `b""` after 15 s, print a message and return `"TIMEOUT"` instead of a blank string.
- [ ] **`try:` / `finally: plateloader.disconnect()`** around the menu loop. This replaces the "Add a disconnect" line in the Day 2 notes and releases the port even after a crash or Ctrl+C.
- [ ] **Six-option menu** (see the code below):
  - MOVE asks two questions and sends `MOVE 1 4`: spaces, **no comma**.
  - GRIPPER: 0 = Open, 1 = Close.
  - Z-AXIS: 0 = Retract, 1 = Extend.
  - X-AXIS and MOVE positions are checked against 1–5.
  - An invalid choice uses `continue`, so no empty `Response:` is printed.
- [ ] **FakePlateloader.ino:** `MOVE` and `SET_DELAY` now read their numbers separated by **spaces, not commas**, to match the real robot. Students with the old sketch will get `Unknown command --> MOVE 1 4` until they re-upload.
- [ ] `initial_pyserial_learning.py` needs no changes.

### Plate loader commands (the real robot's format)

| Command | Example | Reply from the fake loader |
|---|---|---|
| RESET | `RESET` | `READY, SAGIAN PE Loader, ROM Ver. 1.1.6, 12APR2001` |
| X-AXIS | `X-AXIS 3` | `READY` |
| MOVE | `MOVE 5 1` | `READY` (after about 3 s) |
| GRIPPER | `GRIPPER OPEN` / `GRIPPER CLOSE` | `READY, OPEN` / `READY, CLOSED, PLATE` |
| Z-AXIS | `Z-AXIS EXTEND` / `Z-AXIS RETRACT` | `READY, EXTENDED` / `READY, RETRACTED` |
| LOADER_STATUS | `LOADER_STATUS` | `READY, POSITION 3, ZAXIS RETRACTED, GRIPPER CLOSED, PLATE_STATUS PLATE` |
| SET_DELAY | `SET_DELAY 1 2 60` (from, to, delay) | `READY, TO 2, FROM 1, DELAY 60` |

Only positions 1–5 are valid. The menu skips SET_DELAY because it's too complex for the lab. The 12 SET_DELAY commands actually used are:

```
Going to position 2          Going to position 3          Going to position 4
SET_DELAY 1 2 60             SET_DELAY 1 3 20             SET_DELAY 1 4 30
SET_DELAY 3 2 30             SET_DELAY 2 3 30             SET_DELAY 2 4 30
SET_DELAY 4 2 30             SET_DELAY 4 3 30             SET_DELAY 3 4 30
SET_DELAY 5 2 30             SET_DELAY 5 3 20             SET_DELAY 5 4 60
```

### plateloader.py (final)

```python
import serial
import time

class PlateLoader:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.ser = None

    def connect(self):
        if self.ser and self.ser.is_open:
            return
        self.ser = serial.Serial(self.port, baudrate=19200, timeout=15.0)
        time.sleep(2.0)  # Arduino resets when the port opens
        self.ser.reset_input_buffer()
        print(f"Connected to {self.port}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected.")

    def send_command(self, command):
        if not self.ser or not self.ser.is_open:
            self.connect()

        # Sending
        self.ser.reset_input_buffer()
        message_bytes = (command + "\n").encode()
        print("Sending:", message_bytes)
        self.ser.write(message_bytes)

        # Receiving
        response_bytes = self.ser.readline()
        if not response_bytes:
            print(f"Timeout: no response to {command}")
            return "TIMEOUT"
        response = response_bytes.decode().strip()
        print(f"Received: {response}")

        return response
```

### serial_menu.py (final)

```python
from plateloader import PlateLoader

VALID_POSITIONS = ["1", "2", "3", "4", "5"]

if __name__ == "__main__":
    print("Serial Menu")
    plateloader = PlateLoader(port="/dev/ttyACM0")
    plateloader.connect()
    try:
        while True:
            print("\n\n0. Exit")
            print("1. RESET")
            print("2. X-AXIS")
            print("3. MOVE")
            print("4. GRIPPER")
            print("5. Z-AXIS")
            print("6. LOADER_STATUS")
            selection = input("Make a selection: ")

            if selection == "0":
                break
            elif selection == "1":
                response = plateloader.send_command("RESET")
            elif selection == "2":
                to_where = input("Enter X-AXIS position (1-5): ")
                if to_where not in VALID_POSITIONS:
                    print("Invalid X-AXIS position", to_where)
                    continue
                response = plateloader.send_command(f"X-AXIS {to_where}")
            elif selection == "3":
                from_where = input("Enter MOVE from position (1-5): ")
                to_where = input("Enter MOVE to position (1-5): ")
                if from_where not in VALID_POSITIONS or to_where not in VALID_POSITIONS:
                    print("Invalid MOVE positions", from_where, to_where)
                    continue
                response = plateloader.send_command(f"MOVE {from_where} {to_where}")
            elif selection == "4":
                state = input("Enter GRIPPER state (0 = Open, 1 = Close): ")
                if state == "0":
                    response = plateloader.send_command("GRIPPER OPEN")
                elif state == "1":
                    response = plateloader.send_command("GRIPPER CLOSE")
                else:
                    print("Invalid GRIPPER state", state)
                    continue
            elif selection == "5":
                state = input("Enter Z-AXIS state (0 = Retract, 1 = Extend): ")
                if state == "0":
                    response = plateloader.send_command("Z-AXIS RETRACT")
                elif state == "1":
                    response = plateloader.send_command("Z-AXIS EXTEND")
                else:
                    print("Invalid Z-AXIS state", state)
                    continue
            elif selection == "6":
                response = plateloader.send_command("LOADER_STATUS")
            else:
                print("Invalid selection", selection)
                continue

            print("Response:", response)
    finally:
        plateloader.disconnect()  # Ensure cleanup
        print("Goodbye!")
```

---

## Day 2: what to change

- [ ] **Add a Pi setup step:** `sudo apt install python3-flask`. Flask isn't preinstalled on Raspberry Pi OS (Debian 13 trixie), and `pip install flask` fails with the "externally-managed-environment" error. pyserial is already installed as the apt package `python3-serial`.
- [ ] **Remove the second copy of `plateloader.py`** from the Day 2 notes and say "reuse `plateloader.py` from Day 1, in the same folder."
- [ ] **Remove the "Add a disconnect" line.** That's covered on Day 1 now.
- [ ] **Final `serial_server.py`** (code below):
  - `app.run(host='0.0.0.0', port=8080, use_reloader=False)` with **no `debug=True`**. With `0.0.0.0`, `debug=True` lets anyone on the network use the Werkzeug debugger, which can run arbitrary Python.
  - Keep **`use_reloader=False`**. The reloader starts a second process that would also try to open the serial port. (`debug=True` turns the reloader on by default; `use_reloader=False` turns it off.)
  - Delete the commented-out `print`/`return` lines and the commented-out second `app.run`.
  - Explain the `threading.Lock` in one line: Flask handles requests on multiple threads, and the lock lets only one request use the serial port at a time.
- [ ] **Warn that only one program can use `/dev/ttyACM0` at a time.** Quit `serial_menu.py` before starting the server, and stop the server before uploading to the Arduino. A "port busy" or "could not open port" error almost always means this.
- [ ] **URLs:** `localhost:8080` only works in a browser on the Pi itself. From a laptop, use `http://<pi-ip>:8080`, in both Chrome and MATLAB. `hostname -I` on the Pi shows its IP address.
- [ ] **Fix `sendCommand.m`** (see below). The current version, `'http://localhost:8080/api/' + command`, uses **single quotes**, which makes a char array in MATLAB. `+` on char arrays adds the character codes as numbers instead of joining the text. Use double quotes (string) or brackets.
- [ ] **Test MATLAB with a command that has a space,** such as `X-AXIS 3`. Chrome turns the space into `%20` automatically. This hasn't been checked with MATLAB's `webread`; if it fails, use `"X-AXIS%203"`.
- [ ] **Optional:** `hello_world.py`, `file_server_only.py` and `api_route_server_only.py` also use `debug=True` with `0.0.0.0`. That's fine on a laptop, but on a shared network add the same one-line warning.
- [ ] `index.html` and `main.js` need **no changes**. The Move button already sends `MOVE 1 5` with a space, which is correct.

### serial_server.py (final)

```python
import flask
from plateloader import PlateLoader
import threading

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='public')

serial_lock = threading.Lock()
# Intentionally global persistent instance
loader = PlateLoader(port="/dev/ttyACM0")

@app.get("/")
def handle_naked_domain():
    return flask.redirect("/index.html")

@app.route('/api/<command>')
def api_command(command):
    with serial_lock:
        response = loader.send_command(command)
    return response

if __name__ == '__main__':
    loader.connect()
    # No debug=True: the Werkzeug debugger would be reachable from the network.
    # use_reloader=False: a reloader process would try to open the serial port too.
    app.run(host='0.0.0.0', port=8080, use_reloader=False)
```

Run it from `prep/lab3` with `python3 serial_server.py`, then open `http://<pi-ip>:8080`.

### sendCommand.m (fixed)

```matlab
function response = sendCommand(command)
  % Double quotes make a string, so + joins the text
  response = webread("http://localhost:8080/api/" + command);
end
```

Or with char arrays: `webread(['http://localhost:8080/api/' command])`.

---

## Programming the Arduino from the Pi (VS Code Remote-SSH)

The Arduino Community Edition extension works on the Pi over Remote-SSH, but the Mac's settings get in the way.

- Install the extension **in `SSH: fisherds-pi5`** when VS Code asks. It comes with its own `arduino-cli`, so you don't need the Arduino IDE on the Pi.
- **The Mac's User setting `arduino.path=/opt/homebrew/bin` also applies in the remote window** and breaks Verify/Upload with a spawn `ENOENT` error. The fix is in `~/.vscode-server/data/Machine/settings.json` on the Pi:
  ```jsonc
  {
      "arduino.useArduinoCli": true,
      "arduino.path": "",
      "arduino.commandPath": ""
  }
  ```
  Then run **Developer: Reload Window**. The extension only reads these settings when it starts.
- The AVR core has to be installed once (already done on this Pi, in `~/.arduino15`).
- **`.vscode/arduino.json` is in git and its `port` differs by machine:** `/dev/tty.usbmodem…` on the Mac and `/dev/ttyACM0` on the Pi. Run **Arduino: Select Serial Port** on whichever machine you're using.
- The board is an Arduino Mega 2560 (`arduino:avr:mega`).
- **Command-line fallback** (from the repo root):
  ```
  ~/.vscode-server/extensions/vscode-arduino.vscode-arduino-community-0.7.2-linux-arm64/assets/platform/linux-arm64/arduino-cli/arduino-cli.app \
      upload -p /dev/ttyACM0 --fqbn arduino:avr:mega ArduinoCode/FakePlateloader
  ```

---

## Not yet done

- [ ] Commit the `prep/lab3` changes, the `FakePlateloader.ino` changes and `.vscode/arduino.json`.
- [ ] Check whether `webread` in MATLAB handles spaces in the URL.
- [ ] Optional: the fake loader accepts any position number (`X-AXIS 9`). If you know what the real robot replies to a bad position, the fake could copy it.
- [ ] Optional: in `FakePlateloader.ino`, RESET sets `xPosition = 5;` and then `xPosition = 3;` straight away. Delete the first line if the real robot just goes to 3.
