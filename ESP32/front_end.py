import Libraries.ftp
import play
def server_front():
    html = """
<head>
    <meta name="Self-playing guitar" content="width=device-width, initial-scale=1">
</head>

<body>
    <h2>Self-playing guitar</h2>
    <p>
        <a href=\"?play\"<button>Play</button></a>
    </p>
    <p>
        <a href=\"?upload\"><button>Upload</button></a>
    </p>
</body>
</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        start = 0;
        ftp.ftpserver(21)
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Get Request Content = %s' % request)
        start = request.find('/?play')
        if start == 6:
            play.main()
        response = server_front()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
        
            