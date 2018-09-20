import socket
import sys
import struct

def main(TCP_PORT):
  checkSocket(TCP_PORT)

  TCP_IP = "127.0.0.1"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)
  print("Listening on Port: %s" % TCP_PORT)

  conn, addr = s.accept()
  while True:
    data = conn.recv(4096)
    if not data: break
    print ("received data: %s" % data)
    response = parseData(b''.join(data))
    conn.send(response)
  conn.close()


def checkSocket(PORT):
  if PORT < 0 or PORT > 65535:
    print("Invalid Port")
    print("USAGE: python3 udp_client.py [IP Address] [Port]")
    sys.exit(0)

def parseData(data):
  if (total_message_length != len(data)):
    return struct.pack('!bbbi', ord(chr(7)), 0, ord(chr(127)), 0)

  (TML, Request_ID, Opcode, number_of_operands, Operand1, Operand2) = struct.unpack('!bbbbhh', data[:8])

  result = 0
  e = 0
  if Opcode == 0:
    result = Operand1 * Operand2
  elif Opcode == 1:
    result = Operand1 - Operand2
  elif Opcode == 2:  
    result = Operand1 | Operand2
  elif Opcode == 3:  
    result = Operand1 & Operand2
  elif Opcode == 4:  
    result = Operand1 >> Operand2
  elif Opcode == 5:  
    result = Operand1 << Operand2
  elif Opcode == 6:  
    result = ~Operand1
  else:
    e = 127

  return struct.pack('!bbbi', ord(chr(7)), Request_ID, ord(chr(e)), result)

if __name__ == "__main__":
  try:
    while True:
      print("Starting TCP Server")
      if len(sys.argv) == 2:
        main(int(sys.argv[1]))
      else:
        print("invalid command line arguments")
        break
  except KeyboardInterrupt as k:
    print("\nKeyboardInterrupt detected quitting..")