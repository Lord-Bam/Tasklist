#https://gist.github.com/aallan/3d45a062f26bc425b22a17ec9c81e3b6
# asyncio: https://docs.python.org/3/library/asyncio-task.html
import network
import socket
import time
import re
from machine import Pin
import uasyncio as asyncio
import json
import tasklist
import taskWebsite






def favicon():
    f = open("favicon.ico", "rb")
    return f.read()


async def serve_client(reader, writer):
    print("Client connected")
    
    headers = []
    while True:
        line = await reader.readline()
        line = line.decode('utf-8').strip()
        if line == "":
            break
        headers.append(line)
    
    request_raw = str("\r\n".join(headers))
    
    method = headers[0].split(" ")[0]
    url = headers[0].split(" ")[1]
    protocol = headers[0].split(" ")[2]

    print(method, url, protocol)
    
    
    if method == "GET":
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        
        #add the payload
        if url == "/":
            payload = taskWebsite.index()
            content_type = 'Content-Type: text/html\n'
               
               
        elif url == "/example.json":
            payload =  example()
            content_type = 'Content-Type: application/json\n'
            
        elif url == "/favicon.ico":
            payload =  favicon()
            content_type = 'Content-Type: image/x-icon\n'
                
        else:
            payload = "404 Page not found."
            content_type = 'Content-Type: text/plain\n'
        
        writer.write(payload)

        await writer.drain()
        await writer.wait_closed()
        print("Client disconnected")
        
    if method == "POST":
        print(headers)
        
        content_length = ""
        for line in headers:
            if "Content-Length: " in line:
                line = line.split(" ")
                content_length = int(line[1])
                break
        

        #this also contains the button that was pressed!!!
        if content_length > 0:
            post_data_raw = await reader.readexactly(content_length)
            post_data = post_data_raw.decode("utf-8")
            print(post_data)
            post_data = post_data.split("&")
            post_dict = {}
            for data in post_data:
                data = data.split("=")
                post_dict[data[0]] = data[1]
            
            print(post_dict)
            

        payload = taskWebsite.index(method, url, post_dict)
        content_type = 'Content-Type: text/html\n'
            
        
            
        writer.write('HTTP/1.1 200 OK\r\n')
        writer.write(content_type)
        writer.write('Connection: close\r\n')
        writer.write('\n')
        await writer.drain()
        writer.write(payload)
        await writer.drain()
        await writer.wait_closed()



async def start_web_server():
    try:
        print('Setting up webserver...')
        asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
        while True:
            await asyncio.sleep(3)
    finally:
        print("finally")
        asyncio.new_event_loop()
