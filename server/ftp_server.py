import socket
import asyncio
import os
os.chdir('myfiles')


INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100

# Helper function that converts integer into 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

#This function asks for the password
#Similar setup to send_intro_message
async def gatekeep(writer):
    password_message = "Whats the password?\n"

    await send_long_message(writer, password_message)


#This function tells the client that they failed the password attempt
async def denied(writer):
    password_message = "NAK incorrectPassword\n"

    await send_long_message(writer, password_message)


#This function tells the client that they passed the password attempt
async def granted(writer):
    password_message = "ACK correctPassword\n"

    await send_long_message(writer, password_message)


#Function sends intro message to client
async def send_intro_message(writer):
    #Store message into intro_message variable
    intro_message = "Hello! Welcome to my guzmange and flintbr server! I'm majoring in ECE\n"

    #write encoded intro message to the writer variable
    writer.write(intro_message.encode()) 
    
    #send intro message
    await writer.drain()


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

async def end_program(writer: asyncio.StreamWriter):
    print("Closing Connection to Client")
    writer.close()
    await writer.wait_closed()
# TODO - Make function that checks password attempts and either continues the connection or cuts connection


#the "middle man" fuction once connection is achieved this function is called to handle the connection
async def handle_client(reader, writer):

    #ask for password
    await gatekeep(writer)
    #recieve password
    
    #Check password
    i = 1
    while i < 3:
        # Waits for client to send password and stores it in the "password" variable
        password = await receive_long_message(reader)
        print(password)
        # Check if password is incorrect
        if password != "1234":
            i = i+1                                     #Increment the attempt counter
            await denied(writer)                        # Inform the client that their attempt failed
        # Check if password is correct
        if password == "1234":      
            #print("fuck")               
            await granted(writer)                    # Inform client that their attempt was correct
            #print("bitch")
            await menu(reader,writer)                   # Jump to "Menu" routine to begin command parsing
    await end_program(writer)

async def menu(reader,writer):
    #print("asshole")
    #Send intro message once password is correct
    await send_intro_message(writer)
    while True:
        message = await receive_long_message(reader)
        print(message)
        command = message.split()
        print(message)

        if command[0] == "list":
            os.listdir("server/myfiles")
        #if command[0] == "put":
        #if command[0] == "get":
        #if command[0] == "remove":
        if command[0] == "close":
            insert = "ACK Closing Program"
            await send_long_message(writer,insert)
            await end_program(writer)
    """
    Part 2: Long Message Exchange Protocol
    """
    
    

async def main():
    server = await asyncio.start_server(
            handle_client,
            INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
