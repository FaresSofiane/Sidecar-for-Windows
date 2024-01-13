import d3dshot
from flask import Flask, render_template, Response
from PIL import ImageGrab, Image
import numpy as np
import io
import flask_socketio
import mouse

old_x = None
old_y = None

app = Flask(__name__)
socketio = flask_socketio.SocketIO(app)


def generate_frames():
    d = d3dshot.create(capture_output="numpy", frame_buffer_size=120)
    d.display = d.displays[0]
    while True:
        img = d.screenshot()
        frame = np.array(img)

        pil_image = Image.fromarray(frame)
        with io.BytesIO() as buffer:
            pil_image.save(buffer, format="JPEG")
            frame_bytes = buffer.getvalue()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@socketio.on('connect')
def connect():
    print('Client connected')


@socketio.on('pencil')
def pencil(data):
    global old_x, old_y
    initial_resolution = (2778, 1550)

    target_resolution = (1920, 1080)

    x = data["x"]
    y = data["y"]
    converted_x = int(x * (target_resolution[0] / initial_resolution[0]))
    converted_y = int(y * (target_resolution[1] / initial_resolution[1]))
    mouse.move(converted_x + 1920 * 0, converted_y, absolute=True)


@socketio.on('click')
def click(data):
    global old_x, old_y
    initial_resolution = (2778, 1550)

    target_resolution = (1920, 1080)

    x = data["x"]
    y = data["y"]
    converted_x = int(x * (target_resolution[0] / initial_resolution[0]))
    converted_y = int(y * (target_resolution[1] / initial_resolution[1]))
    mouse.move(converted_x, converted_y, absolute=True)
    mouse.click()


@socketio.on('end')
def end(data):
    global old_x, old_y
    old_x = None
    old_y = None


@socketio.on('info')
def info(data):
    print(data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True, host='0.0.0.0')
