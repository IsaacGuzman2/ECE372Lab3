import socket
import asyncio
import os
os.chdir('myfiles')


INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100

async def gatekeep(writer):
    password_message = "Welcome, whats the password?\n"

    writer.write(password_message.encode())
    await writer.drain()


# TODO: Implement me for Part 1!
async def send_intro_message(writer):
    intro_message = "Hello! Welcome to my guzmange and flintbr server! I'm majoring in ECE\n"

    writer.write(intro_message.encode())
    await writer.drain()


# TODO: Implement me for Part 2!
async def receive_long_message(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    # Note: `socket.MSG_WAITALL` is just to make sure the data is received in this case.
    data_length_hex = await reader.readexactly(8)

    # Then we convert it from hex to integer format that we can work with
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    return full_data.decode()


async def handle_client(reader, writer):
    """
    Part 1: Introduction
    """
    await gatekeep(writer)
    #recieve password
    #check password

    # TODO: send the introduction message by implementing `send_intro_message` above.
    await send_intro_message(writer)

    """
    Part 2: Long Message Exchange Protocol
    """
    # TODO: Implement function above
    message = await receive_long_message(reader)

    # I'm only printing the last 8 characters of the message here because it's long
    print(message)

    writer.close()
    await writer.wait_closed()


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
