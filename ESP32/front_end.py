import socket
import ESP32.Generate_list
import ESP32.play_test

def server_front():
    html_file = open("ESP32/midi_list.html")
    html = html_file.read()
    html_file.close()
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
ESP32.Generate_list.Midi_select()
while True:
    try:
        
        start = 0;
        if gc.mem_free() < 102000:
            gc.collect()
        #print("Frontend running...")
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Get Request Content = %s' % request)
        start_condition = request.find('?play')
        print(start_condition)
        if start_condition > 10 and start_condition < 100:
            start = request.split('?')
            temp = start[0]
            temp1 = temp.split('/')
            decision = temp1[1]
            print(decision)
            # Uncomment when connected to the guitar       
            ESP32.play_test.main(decision)
        response = server_front()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
        
            
