import socket
import os

HOST = ''
PORT = 65432
BUFF = 2048
username = False

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect((HOST, PORT))


# os independent clear screen method
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# client side of the gameplay. Run in a threaded server to 
# both clients with wait stages to keep player actions in sync.
def gameplay():

    while True:

        clear()

        # receive two messages from Server, a refreshed map
        # and turn information
        MAP = CLIENT.recv(BUFF).decode()
        TURN = CLIENT.recv(BUFF).decode()

        print(MAP)
        print(TURN)

        # this is a pretty hacky/brute way to do this, but the message
        # from the server is interpreted to choose the output to the player
        if TURN.lower() == '> your turn':    
            # final valid input from pl to send to server
            opt = ''

            # get valid input from player before sending
            while True:

                print('[1] Sword    [2] Spell')
                move = input('>> ')
                
                if move != '1' and move != '2':
                    print('> Invalid Move')
                else:
                    opt = move
                    break

            # send attacking pl input to server
            CLIENT.send(opt.encode())

        # RECV A - refreshed map after outcome and for screen clarity
        MAP_REFRESH = CLIENT.recv(BUFF).decode()
        # RECV B - receive your attack outcome
        OUTCOME = CLIENT.recv(BUFF).decode()

        clear()

        print(MAP_REFRESH)
        print(OUTCOME)

        # receive continue confirmation
        CLIENT.recv(BUFF)


# Connect to the lobby and get the player username
while True:
    data = CLIENT.recv(BUFF)

    # game begins by interpreted message from server once two players connect
    if data.decode() == 'start':
        print('[*] GAME STARTING')
        gameplay()
        break
    print(data.decode())

    if not username:
        username = input('> ')
        CLIENT.send(username.encode())
        



    