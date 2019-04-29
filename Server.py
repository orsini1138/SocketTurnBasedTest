import socket
from _thread import *
import threading
import os
import time
import attacks

HOST = ''
PORT = 65432
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

CLIENTS = {}
ADDRESSES = {}

# Initiate server socket obj
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


print('[*] WORKING')


# Store alternating player variable here for choosing the current player later
# where a local variable shared by threads will be messy, especially since it MUST
# stay consistent between players. This works lol
class playerData():
    
    PLAYER = 0

    PLAYER_HP = {}



# Send info to both players
def broadcast(message):
    for user in CLIENTS:
        user.send(f"{message}".encode())


# Render game and send to clients concurrently 
def gameloop(pl_A, pl_B):

    playerData.PLAYER_HP[pl_A] = 20
    playerData.PLAYER_HP[pl_B] = 20

    print('[*] GAME RUNNING')

    # Map to send to clients
    map = f'''
    ...X.............X...'''+ (f'\n    {CLIENTS[pl_A]}').ljust(15)+(f'{CLIENTS[pl_B]}').rjust(11)+'\n'
    
    while True:
        # concatenate map and the updating health data into one
        # send map to players each round
        health_and_map = map + f'    {str(playerData.PLAYER_HP[pl_A])}'+(f'{str(playerData.PLAYER_HP[pl_B])}\n').rjust(20)
        broadcast(health_and_map)

        ## CHECK WIN CONDITION
        if playerData.PLAYER_HP[pl_A] <= 0 or playerData.PLAYER_HP[pl_B] <= 0:
            if playerData.PLAYER_HP[pl_A] <= 0:
                broadcast(f'> {CLIENTS[pl_B]} Wins!')
                time.sleep(2)
            elif playerData.PLAYER_HP[pl_B] <= 0:
                broadcast(f'> {CLIENTS[pl_A]} Wins!')
                time.sleep(2)
            for client in CLIENTS:
                client.close()
            SERVER.close()
            os.sys.exit(0)
            

        # re-assign players each turn to these vars, alternating
        player_a = None
        player_b = None
        defending_player = None

        # assigning the players to the above vars based on playerdata variable.
        # This keeps the code shorter below and reuses almost nothing now. It also
        # makes adding combat easier and keeps it from being an if statement that
        # contains two identical blocks that only differentiate in which pl its sending to
        if playerData.PLAYER % 2 == 0:
            player_a = pl_A
            player_b = defending_player = pl_B
        else:
            player_a = pl_B
            player_b = defending_player = pl_A
        
        # Send players their turn or their wait status
        player_a.send('> Your turn'.encode())
        player_b.send(f'> {CLIENTS[player_a]}\'s turn'.encode())
        action = player_a.recv(BUFFER_SIZE).decode()

        #SEND A-  resend map with updated info and screen clarity
        broadcast(health_and_map)  

        if action == '1':
            HP, DAM = attacks.sword(playerData.PLAYER_HP[defending_player])
            playerData.PLAYER_HP[defending_player] = HP

            # SEND B - send attack outcome 
            broadcast(f'> {CLIENTS[player_a]} uses sword! -{str(DAM)} dam')

        elif action == '2':
            HP, DAM = attacks.spell(playerData.PLAYER_HP[defending_player])
            playerData.PLAYER_HP[defending_player] = HP

            # SEND B - send attack outcome
            broadcast(f'> {CLIENTS[player_a]} uses spell! -{str(DAM)} dam')
        
        time.sleep(2)

        ## TODO the players actual attack and damage

        # confirmation that round has ended. Clients will recv this
        # message and continue the gameplay loop together to avoid
        # issues with the threads misaligning
        broadcast('conf')

        # continue to increment this var to decide which players turn it is
        playerData.PLAYER += 1

        # maintain lag so that client program can run its refresh code in gameplay()
        # MUST HAVE THIS PAUSE otherwise client will NOT get updates
        time.sleep(.2)


def game_start(client):

    # build numerically accessible list of client sockets for easy calling
    client_list = []
    for cli in CLIENTS:
        client_list.append(cli)

    # send client sockets in separate threads into game loop
    PL_THREAD = threading.Thread(target=gameloop, args=(client_list[0], client_list[1],))
    PL_THREAD.start()


# Accept clients, receive their usernames, 
# and when 2 have connected, start the game
def accept_clients():
    # keep track of connected clients until x == 2
    x = 0

    while True:

        print(str(len(CLIENTS))+' clients in lobby')
        SERVER.listen(2)

        client_socket, client_address = SERVER.accept()
        ADDRESSES[client_socket] = client_address
        x += 1
        
        print('Connected by ', client_address)
        client_socket.sendall('> Connected to server\n> Please enter username'.encode())
        
        client_name = client_socket.recv(BUFFER_SIZE).decode()
        CLIENTS[client_socket] = client_name

        client_socket.sendall(f'> You are now playing as {client_name}'.encode())

        if x == 2:
            print('[*] ENTERING GAME')
            for client in CLIENTS:
                client.sendall('start'.encode())
            time.sleep(1)

            game_start(client_socket)
            break


def main():
    accept_clients()

main()
