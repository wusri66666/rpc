import json
import time
import struct
import socket


def rpc(sock, in_, params):
    request = json.dumps({"in":in_, "params":params})
    req_length_prefix = struct.pack("I", len(request))
    sock.sendall(req_length_prefix)
    sock.sendall(request.encode())

    res_length_prefix = sock.recv(4)
    length, = struct.unpack("I",res_length_prefix)
    body = sock.recv(length)
    response = json.loads(body.decode())
    return response['out'], response['result']


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))
    for i in range(10):
        out, result = rpc(s, "ping", "ireader %s"%i)
        print(out, result)
        time.sleep(1)
    s.close()