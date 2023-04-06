# import ESP32.Libraries.ftp
import socket
import ESP32.play

def server_front():
    
    html_file = open("GuitarUI.html")
    html = html_file.read()
    html_file.close()

    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        start = 0;
        # ESP32.Libraries.ftp.ftpserver()
        if gc.mem_free() < 102000:
            gc.collect()
        print("Frontend running...")
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Get Request Content = %s' % request)
        start = request.find('/?play')
        print(start)
        
        # Uncomment when connected to the guitar
        if start == 6:            
            ESP32.play.main()
            
        response = server_front()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
        
            
