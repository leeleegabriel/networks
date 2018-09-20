# Lee Vanrell
# Group 6
# COMP-4320
# 9/20/18

import sys
import socket
import random
import datetime
import ipaddress
import struct

def main(UDP_ADDRESS, UDP_PORT):
  checkSocket(UDP_ADDRESS, UDP_PORT)

  Opcode = getInput("Enter Opcode: ", 0, 6)
  Operand1 = getInput("Enter Operand1: ", -32768, 32767)
  if Opcode != 6:
    Operand2 = getInput("Enter Operand2: ", -32768, 32767)

  Request_id = random.randint(-128, 127)

  if Opcode != 6:
    MESSAGE = getMessage(Request_id, Opcode, Operand1, Operand2)
  else:
    MESSAGE = getMessage(Request_id, Opcode, Operand1)
  #sendMessage("".join(MESSAGE).encode(), UDP_ADDRESS, UDP_PORT)
  sendMessage(MESSAGE, UDP_ADDRESS, UDP_PORT, Request_id)

def checkSocket(ADDRESS, PORT):
  try:
    ipaddress.ip_address(ADDRESS)
  except ValueError:
    print("Invalid IP")
    print("USAGE: python3 udp_client.py [IP Address] [Port]")
    sys.exit(0)

  if PORT < 0 or PORT > 65535:
    print("Invalid Port")
    print("USAGE: python3 udp_client.py [IP Address] [Port]")
    sys.exit(0)


def getInput(output, lower_bound, upper_bound):
  while True:
    try:
      u_input= int(input(output))
      if u_input >= lower_bound and u_input <= upper_bound:
        return u_input
    except:
      pass
    print("Invalid input")

def getMessage(Request_id, Opcode, Operand1, Operand2=0):
  if Opcode == 6:
    Number_of_Operands = 1
  else:
    Number_of_Operands = 2

  MESSAGE = struct.pack('!bbbbhh', 8, int(Request_id), int(Opcode), Number_of_Operands, Operand1, Operand2)
  for x in range(0, 8):
    print(hex((MESSAGE[x])))
  return MESSAGE

# def printMessage(Output):
#   x = 0
#   print("Bytes:")
#   while x in range(0, len(Output)):
#     print("".join(Output[x:x+2]))
#     x += 2

def sendMessage(MESSAGE, UDP_ADDRESS, UDP_PORT, Request_id):  
  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
  client.settimeout(10)
  #client.bind(("127.0.0.1", UDP_PORT))
  try:

    print("Sending Data:")
    t1 = datetime.datetime.now()
    client.sendto(MESSAGE, (UDP_ADDRESS, UDP_PORT))
    
    data, addr = client.recvfrom(4096)
    t2 = datetime.datetime.now()

    t_delta = t2 - t1 

    print("Response received: %s" % Request_id)
    print(data)
    print("Round trip time: %s" % (t1 - t2).microseconds)
  except socket.timeout as e:
    print("Server timed out (10 seconds)")

if __name__ == "__main__":
  try:
    while True:
      print("Starting UDP Client")
      if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
      else:
        print("invalid command line arguments")
        break
  except KeyboardInterrupt as k:
    print("\nKeyboardInterrupt detected quitting..")