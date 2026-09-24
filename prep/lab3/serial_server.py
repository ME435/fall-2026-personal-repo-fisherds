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
