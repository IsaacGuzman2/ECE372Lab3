import os
os.chdir('myfiles')
import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

# Helper function that converts integer into 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def recv_intro_message(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

    

async def send_long_message(writer: asyncio.StreamWriter, data):
    await asyncio.sleep(1)

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()

# Function processes messages from client
async def receive_long_message(reader: asyncio.StreamReader):

    data_length_hex = await reader.readexactly(8)

    data_length = int(data_length_hex, 16)
    full_data = await reader.readexactly(data_length)
    return full_data.decode()


async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    """
    Part 1: Introduction
    """
    # TODO: receive the introduction message by implementing `recv_intro_message` above.
    intro = await receive_long_message(reader)
    print(intro)
    x = 1
    while x < 3:

        password = input("Enter Password: ")
        await send_long_message(writer, password)
        message = await receive_long_message(reader)
        #print(message)
        if message == "NAK incorrectPassword\n":

            #print("Attempt "+i+" of 3")
            x = x+1
            
            print(message)

        if message == "ACK correctPassword\n":
            #print("fuck")
            break
    await menu(i,reader,writer)
    return 0

async def menu(i,reader,writer):
    intro = await recv_intro_message(reader)
    print(intro)
    while True:
        message = input("Enter command >>")
        await send_long_message(writer,message)
        answer = await receive_long_message(reader)
        print(answer)
        command = message.split()
        if command[0] == "close":
            return 0
        elif command[0] == "put":
            list = os.listdir(path='.')
            if command[1] in list:
                with open(command[1],'r') as f:
                    content = f.read()
                await send_long_message(writer,content)
                message = await receive_long_message(reader)
                print(message)
            else:
                content = "file not found"
                await send_long_message(writer,content)
                message = await receive_long_message(reader)
                print(message)

        elif command[0] == "get":

            if answer == "NAK File does not exist":
                print("\n")
            else:
                towrite = await receive_long_message(reader)
                with open(command[1],'w') as f:
                    f.write(towrite)

async def main():
    tasks = []
    for i in range(1):
        tasks.append(connect(str(i).rjust(8, '0')))

    await asyncio.gather(*tasks)
    print("done")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
