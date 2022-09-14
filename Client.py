import socket
import sys
import os.path
import select
def input_helper(args):
    """Validifies comand line inputs"""
    if len(args) != 4:
        sys.exit(f"Error: Incorect amount of inputs ({len(args)-1})")   
    try:
        form = str(args[1])
        ip = str(args[2])
        port = int(args[3])
    except ValueError:
        sys.exit("Error: Port value (input 3) must be an integer value") 
    if form != "date" and form != "time":
        sys.exit(f"First argument must be date or time,you inputted: {form}")    
    else:
        try:
            socket.getaddrinfo(ip, port)
        except:
            sys.exit("Invalid IP or host-name provided (Second Input)")     
    if port <= 1024 or port >= 64000:
        sys.exit("Port entered is invalid please enter a number between" \
                 "1024 and 64000 (Non-inclusive)")
            
    return form, ip, port  
    
def create_packet(form):
    """Creates a request packet to send to the server"""
    if form == "date":
        request_type = 0x0001
    else:
        request_type = 0x0002
    packet = bytearray(((0x497E<<32) + (0x0001<<16) + 
                        (request_type)).to_bytes(6, "big"))
    return packet

def connect_to_server(form, ip, port):
    """ Connects to server, sends request packet, waits 1 second 
    to recieve the response packet and then calls convert(packet, addr) 
    to print recieved information to command line."""
    try:
        #create socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        sys.exit("Error: Socket creation has failed")

    try:
        #connects to said socket
        client_sock.connect((ip, port))
    except:
        sys.exit(f"Error: Socket connection failed")
    #creates request packet
    packet = create_packet(form)
    client_sock.send(packet)
    reader, _, _ = select.select([client_sock], [], [], 1)
    #waits for response from server
    if reader:
        packet, addr = reader[0].recvfrom(64)
        convert(packet, addr)
    else:
        sys.exit("Error: TimeOut return packet not recieved in time")
        
def convert(packet, addr):
    """converts packet from byte array to a readable format"""
    magic = ((packet[0]<<8) + packet[1])
    p_type = ((packet[2]<<8) + packet[3])
    l_code = ((packet[4]<<8) + packet[5])
    year = ((packet[6]<<8) + packet[7])
    month = packet[8]
    day = packet[9]
    hour = packet[10]
    minute = packet[11]
    length = packet[12]
    if magic != 0x497E:
        sys.exit("Error: MagicNo Invalid")  
    elif p_type != 0x0002:
        sys.exit("Error: PacketType Invalid")   
    elif l_code not in [0x0001,0x0002,0x0003]:
        sys.exit("Error: Language code invalid")
    elif year >= 2100:
        sys.exit(f"Error: The year is not above 2,100 (Not {year})")
    elif month > 12 or month < 1:
        sys.exit("Error: Month server provided is invalid")
    elif day > 31 or day < 1:
        sys.exit("Error: Day server provided is invalid")
    elif hour > 23 or hour < 0:
        sys.exit("Error: Hour server provided is invalid")
    elif minute > 59 or minute < 0:
        sys.exit("Error: Minute server provided is invalid")
    elif len(packet) != (13+length):
        sys.exit("Error: Length in header does not match text size")
        
    t_rep = packet[13:].decode('utf-8')
    final_print = f"~~~~~~~~~~~~~~~~\nMagicNO: {magic}\nPacketType: {p_type}" \
        f"\nlanguage Code: {p_type}\nYear: {year}\nMonth: {month}\n" \
        f"Day: {day}\nHour: {hour}\nMinute: {minute}\nLength: {length}\n" \
        f"Textual representation: {t_rep}\n~~~~~~~~~~~~~~~~"
    sys.exit(final_print)
    
def main():
    form, ip, port = input_helper(sys.argv)
    connect_to_server(form, ip, port)
    
if __name__ == "__main__":
    main()
