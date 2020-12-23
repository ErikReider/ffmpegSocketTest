import numpy as np
import subprocess as sp
import socket
import threading
import atexit
import shlex
from functools import partial
import io
import cv2

# 1920×1080×3 = 6220800

width, height = 1920, 1080
timesValue = width * height * 3

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 6969)
sock.bind(server_address)
sock.listen(1)

thread = threading.Thread(target=lambda x: sp.Popen("./" + x, stdin=sp.DEVNULL,
                                                    stderr=sp.DEVNULL, stdout=sp.DEVNULL, bufsize=10**8), args=("send.sh",))
print('Waiting for a connection')
thread.start()

connection, client_address = sock.accept()
stream = io.BytesIO()


def close():
    stream.close()
    connection.close()
    thread.join()
    cv2.destroyAllWindows()


atexit.register(close)

try:
    print('Connection from', client_address)
    index = 0
    while True:
        data = connection.recv(timesValue)
        if not data:
            break
        stream.write(data)
        stream.seek(0, 2)

        if stream.tell() >= index + timesValue:
            in_bytes = stream.getvalue()[index: index + timesValue]
            # print(in_bytes)
            index += timesValue
            if not in_bytes:
                break
            in_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
            cv2.imshow('in_frame', in_frame)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
finally:
    exit(0)
