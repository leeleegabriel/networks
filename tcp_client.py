# Lee Vanrell
# Group 6
# COMP-4320
# 9/20/18

import socket
import random
import datetime
import ipaddress

def main():
  TCP_ADDRESS = getIP()
  TCP_PORT = getInput("Enter Server Port: ", 0, 65536)

  Opcode = getInput("Enter Opcode: ", 0, 6)
  Operand1 = getInput("Enter Operand1: ", -32768, 32767)
  if Opcode != 6:
    Operand2 = getInput("Enter Operand2: ", -32768, 32767)

  Request_id = random.randint(0, 255)


  if Opcode != 6:
    MESSAGE = getMessage(Request_id, Opcode, Operand1, Operand2)
  else:
    MESSAGE = getMessage(Request_id, Opcode, Operand1)

  printMessage(MESSAGE)
  sendMessage("".join(MESSAGE).encode(), TCP_ADDRESS, TCP_PORT)

def getIP():
  while True:
    TCP_ADDRESS = input("Enter Server IP: ")
    try:
      ipaddress.ip_address(TCP_ADDRESS)
      return TCP_ADDRESS
    except ValueError:
      print("Invalid IP")

def getInput(output, lower_bound, upper_bound):
  while True:
    try:
      u_input= int(input(output))
      if u_input >= lower_bound and u_input <= upper_bound:
        return u_input
    except:
      pass
    print("Invalid input")

def getMessage(Request_id, Opcode, Operand1, Operand2=""):
  Request_id = (Request_id).to_bytes(1, byteorder='big')
  Opcode =  (Operand1).to_bytes(1, byteorder='big')
  Operand1 =  (Operand1).to_bytes(2, byteorder='big')
  if Opcode != 6:
    Byte_count = (8).to_bytes(1, byteorder='big')
    Number_of_Operands = (2).to_bytes(1, byteorder='big')
    Operand2 = (Operand2).to_bytes(2, byteorder='big')
  else:
    Byte_count = (6).to_bytes(1, byteorder='big')
    Number_of_Operands = (1).to_bytes(1, byteorder='big')

  MESSAGE = []
  if Opcode != 6:
    MESSAGE += (Byte_count).hex()
    MESSAGE += (Request_id).hex()
    MESSAGE += (Opcode).hex()
    MESSAGE += (Number_of_Operands).hex()
    MESSAGE += (Operand1).hex()
    MESSAGE += (Operand2).hex()
  else: 
    MESSAGE += (Byte_count).hex()
    MESSAGE += (Request_id).hex()
    MESSAGE += (Opcode).hex()
    MESSAGE += (Number_of_Operands).hex()
    MESSAGE += (Operand1).hex()
  return MESSAGE

def printMessage(MESSAGE):
  x = 0
  print("Bytes:")
  while x in range(0, len(MESSAGE)):
    print("".join(MESSAGE[x:x+2]))
    x += 2

def sendMessage(MESSAGE, TCP_ADDRESS, TCP_PORT):  
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((TCP_ADDRESS, TCP_PORT))
  client.settimeout(10)
  try:

    print("Sending Data:")
    t1 = datetime.datetime.now()
    client.send(MESSAGE)
    
    response = client.recv(4096)
    t2 = datetime.datetime.now()

    t_delta = t2 - t1 
    print("Response received: %s" % Request_id)
    print(response)
    print("Round trip time: %s" % (t1 - t2).microseconds)
  except socket.timeout as e:
    print("Server timed out (10 seconds")

if __name__ == "__main__":
  try:
    while True:
      print("Starting UDP Client")
      main()
  except KeyboardInterrupt as k:
    print("\nKeyboardInterrupt detected quitting..")