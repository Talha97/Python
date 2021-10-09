import threading
import serial
import time

serialConnection = serial.Serial()
serialConnection.baudrate = 14000 
serialConnection.port = 'COM7'
serialConnection.parity=serial.PARITY_NONE
serialConnection.stopbits=serial.STOPBITS_ONE
serialConnection.bytesize=serial.EIGHTBITS
serialConnection.timeout=0

stopWriteThread=False
stopReadThread=False

def writeSeriChannel():

    global serialConnection
    global stopWriteThread
    
    while True:
        serialConnection.write(b"Author: Talha Sevinc\r\n")
        time.sleep(1)
       
        if(stopWriteThread):
            break


def readSeriChannel():

    global serialConnection
    global stopReadThread
    
    receivedMessage="";
    messageInfo="Message Came: "
    while True:
     
     if(serialConnection.inWaiting() > 0):

         time.sleep(0.20)
         for message in serialConnection.read(100):
          receivedMessage+= chr(message)
       
         print(messageInfo+receivedMessage)
         receivedMessage=""
      
     if(stopReadThread):
        
         break
      
      


if __name__ == '__main__':
    
    serialConnection.open()
    
    thread1=threading.Thread(target=writeSeriChannel)
    thread2=threading.Thread(target=readSeriChannel)
    
    thread1.start()
    thread2.start()
    
    time.sleep(1)
    stopWriteThread=True
    
    while(True):
        
        sendMessage=input("Send Message:")
        
        if(sendMessage=="Quit" or sendMessage=="quit"):
            
           serialConnection.write("End Of program. I quited.".encode()) 
           
           stopWriteThread=True
           stopReadThread=True
           serialConnection.close()
           
           break
       
        else:
           serialConnection.write(sendMessage.encode())
        
     