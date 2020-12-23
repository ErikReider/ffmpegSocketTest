import numpy as np
import subprocess as sp
import socket
import threading
import atexit
import io
import cv2

# 1920×1080×3 = 6220800

width, height = 1920, 1080
timesValue = width * height * 3

# Create the socket and only listen to 1 connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 6969)
sock.bind(server_address)
sock.listen(1)

thread = threading.Thread(target=lambda x: sp.Popen("./" + x, stdin=sp.DEVNULL,
                                                    stderr=sp.DEVNULL, stdout=sp.DEVNULL, bufsize=10**8), args=("send.sh",))
print("Waiting for a connection")
thread.start()

cv2.namedWindow("window", flags=cv2.WINDOW_GUI_NORMAL)

connection, client_address = sock.accept()
stream = io.BytesIO()


def close():
    stream.close()
    connection.close()
    thread.join()
    cv2.destroyAllWindows()


atexit.register(close)

print('Connection from', client_address)
while True:
    # Get 6220800 bytes of data from the socket (not always that amount)
    data = connection.recv(timesValue)
    if not data:
        break
    stream.write(data)
    stream.seek(0, 2)
    # When the stream index reaches 6220800, show a new frame (Each frame is W * H * 3 (R,G,B))
    if stream.tell() >= timesValue:
        in_bytes = stream.getvalue()[0: timesValue]
        stream = io.BytesIO(stream.getvalue()[timesValue:])
        if not in_bytes:
            break
        # Convert the raw bytes to rgb values and show the image
        cv2.imshow("window", np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3]))
        # Wait for 1ms to prevent closing
        cv2.waitKey(1)
