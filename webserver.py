#https://gist.github.com/aallan/3d45a062f26bc425b22a17ec9c81e3b6
# asyncio: https://docs.python.org/3/library/asyncio-task.html
import network
import socket
import time
import re
from machine import Pin
import uasyncio as asyncio
import json

def index():
    f = open("index.html", "r")
    return f.read()

def example():
    f = open("example.json", "r")
    return f.read()

def favicon():
    f = open("favicon.ico", "rb")


async def serve_client(reader, writer):
    print("Client connected")
    
    headers = []
    while True:
        line = await reader.readline()
        line = line.decode('utf-8').strip()
        if line == "":
            break
        headers.append(line)
    
    print("before join:", headers)
    request_raw = str("\r\n".join(headers))
    print("after join:", request_raw)
    
    method = headers[0].split(" ")[0]
    url = headers[0].split(" ")[1]
    protocol = headers[0].split(" ")[2]

    print(method, url, protocol)
    
    
    if method == "GET":
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        
        #add the payload
        if url == "/":
            payload = index()
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
        content_length_pattern = re.compile(r"Content-Length:\s+(\d+)")
        match = content_length_pattern.search(request_raw)
        boundary_patern = re.compile(r"boundary=(\S*)")
        boundary = boundary_patern.search(request_raw)
        print(request_raw)
        print("boundary == ", boundary.group(1))
        
        if match:
            content_length = int(match.group(1))
            print("content_length: "+str(content_length))
        
        if content_length > 0:
            post_data_raw = await reader.readexactly(content_length)
            post_data = post_data_raw.decode("utf-8")
            print("post_data == ",  post_data)
            
            #Fuck this!!!! there goes my evening: https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2
            delimiter1 = "--" + boundary.group(1)
            delimiter2 = "Content-Type: application/json"
            
            post_data = post_data.replace(delimiter2, "*")
            post_data = post_data.replace(delimiter1, "*")

            post_data = post_data.split("*")[2].strip()
            print("post_data === " , post_data)
            
            response = post_data
            content_type = 'Content-Type: application/json\r\n'
            
            
            writer.write('HTTP/1.1 200 OK\r\n')
            writer.write(content_type)
            writer.write('Connection: close\r\n')
            writer.write('\n')
            await writer.drain()
            writer.write(str(post_data))
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
