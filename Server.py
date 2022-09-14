import socket
import sys
import os.path
import select
import datetime
import time
"""Initialising saerver based on sys args"""
HOST = "127.0.0.1"
if len(sys.argv) != 4:
    sys.exit(f"Error: Incorect amount of ports ({len(sys.argv)-1})")
    
try:
    PORT1 = int(sys.argv[1])
    PORT2 = int(sys.argv[2])
    PORT3 = int(sys.argv[3])
    if PORT1 == PORT2 or PORT2 == PORT3 or PORT1 == PORT3:
        sys.exit("Error: All Inputs must be different")    
except ValueError:
    sys.exit("Error: All inputs must be an integer value")
    
ENGMONTHDICT = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 
             6:'June', 7:'July', 8:'August', 9:'September', 10:'October',
             11:'November', 12:'December'}
MAORIMONTHDICT = {1:'Kohitatea', 2:'Hui-tanguru ', 3:'Poutu-te-rangi', 
                  4:'Paenga-whawha ', 5:'Haratua', 6:'Pipiri ', 7:'Hongongoi',
                  8:'Here-turi-koka', 9:'Mahuru', 10:'Whiringa-a-nuku ', 
                  11:'Whiringa-a-rangi', 12:'Hakihea'}
GERMONTHDICT = {1:'Januar', 2:'Februar', 3:'Marz', 4:'April', 5:'Mai', 
                   6:'Juni', 7:'Juli', 8:'August', 9:'September', 10:'Oktober',
                   11:'November', 12:'Dezember'}
DATEDICT = {1:'Today’s date is', 2:'Ko te ra o tenei ra ko',
           3: 'Heute ist der'}
TIMEDICT = {1:'The current time is', 2:'Ko te wa o tenei wa',
           3: 'Die Uhrzeit ist'}

def server():
    """Initialises 3 sockets with a potential to be accessed
    assembles a response packet based on request and sends it back to the 
    clients socket"""
    eng_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mao_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ger_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_list = [eng_sock, mao_sock, ger_sock]
    
    try:
        eng_sock.bind((HOST, PORT1))
        mao_sock.bind((HOST, PORT2))
        ger_sock.bind((HOST, PORT3))
    except:
        sys.exit(f"Error: Socket binding failed" )
        
    while True:
        #waits for request packet
        readers, _, _ = select.select(server_list, [], [])
        for reader in readers:
            #determines language type of request packet.
            #then assembles a response packet and sends it back to the client.
            data, addr = reader.recvfrom(6)
            if reader == eng_sock:
                magic, p_type, r_type = read_packet(data)
                response_packet = assemble_return_packet(magic, p_type, r_type, 1)
                eng_sock.sendto(response_packet, addr)
            elif reader == mao_sock:
                magic, p_type, r_type = read_packet(data)
                response_packet = assemble_return_packet(magic, p_type, r_type, 2)
                mao_sock.sendto(response_packet, addr)
            elif reader == ger_sock:
                magic, p_type, r_type = read_packet(data)
                response_packet = assemble_return_packet(magic, p_type, r_type, 3)
                ger_sock.sendto(response_packet, addr)
                
def read_packet(packet):
    """Reads the request packet and assures it is in the right format 
    then returns individual parts of the byte array"""
    if len(packet) != 6:
        sys.exit("Error: This packet is not the right length." +
                         f"It is {len(data)} instead of 6 bytes long")  
        
    magic = ((packet[0]<<8) + packet[1])
    p_type = ((packet[2]<<8) + packet[3])
    r_type = ((packet[4]<<8) + packet[5])
    if magic != 0x497E:
        sys.exit("Error: MagicNo Invalid")   
    elif p_type != 0x0001:
        sys.exit("Error: PacketType Invalid")    
    elif r_type != 0x0001 and r_type != 0x0002:
        sys.exit("Error: RequestType Invalid")
            
    return magic, p_type, r_type

def assemble_return_packet(magic, p_type, r_type, language):
    """assembles response packet based on whether request packet 
    wants time or dateand what language they'd like it to be in."""
    date = datetime.datetime.today()
    if r_type == 0x0001:
        if language == 0x0001:
            msg = f"{DATEDICT[language]} {ENGMONTHDICT[date.month]} {date.day}, {date.year}"
        elif language == 0x0002:
            msg = f"{DATEDICT[language]} {MAORIMONTHDICT[date.month]} {date.day}, {date.year}"
        elif language == 0x0003:
            msg = f"{DATEDICT[language]} {date.day}. {GERMONTHDICT[date.month]} {date.year}"
            
    elif r_type == 0x0002:
        if language == 0x0001:
            msg = f"{TIMEDICT[language]} {date.hour}:{date.minute}"
        elif language == 0x0002:
            msg = f"{TIMEDICT[language]} {date.hour}:{date.minute}"
        elif language == 0x0003:
            msg = f"{TIMEDICT[language]} {date.hour}:{date.minute}"   
    
    byte_msg = msg.encode('utf-8')
    length = len(byte_msg)
    response_packet = bytearray(byte_msg)
    response_packet2 = bytearray((length +
                                 (date.minute<<8) + 
                                 (date.hour<<16) +
                                 (date.day<<24) +
                                 (date.month<<32) +
                                 (date.year<<40) +
                                 (language<<56) +
                                 (0x0002<<72) +
                                 (magic<<88)
                                 ).to_bytes(13, byteorder='big'))
    response_packet[0:0] = response_packet2
    return response_packet

if __name__ == "__main__":
    server()

main()