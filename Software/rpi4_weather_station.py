# Import the required libraries
import sys
import RPi.GPIO as GPIO
import os
import adafruit_dht
import urllib.request
import smbus
import time
import board
from ctypes import c_short

# Register Address
regCall  = 0xAA
regMean  = 0xF4
regMSB   = 0xF6
regLSB   = 0xF7
reghumid = 0x34
regTemp  = 0x2e
DEBUG = 1
sample = 2
deviceAdd = 0x77
humid = ""
temp = ""
I2cbus = smbus.SMBus(1)
key = "UNQ0JV1D7GNNUXBQ" # Write API key from ThingSpeak
GPIO.setmode(GPIO.BCM)

# Define GPIO to LCD Display mapping
LCD_RS = 18
LCD_EN = 23
LCD_D4 = 24
LCD_D5 = 16
LCD_D6 = 20
LCD_D7 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_EN, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

# def convert1(data, i): # signed 16-bit value
#     return c_short((data[i]<<8) + data[i + 1]).value

# def convert2(data, i): # unsigned 16-bit value
#     return (data[i]<<8) + data[i + 1]

# Define the DHT function
def readDHT():
    dht_device = adafruit_dht.DHT11(board.D22)
    temp = dht_device.temperature
    humid = dht_device.humidity
    return (str(int(humid)), str(int(temp)))

# initialize the LCD display
def lcd_init():
    lcdcmd(0x33)
    lcdcmd(0x32)
    lcdcmd(0x06)
    lcdcmd(0x0C)

# Define LCD Commands and data
def lcdcmd(ch): 

  GPIO.output(LCD_RS, 0)
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if ch&0x10==0x10:
    GPIO.output(LCD_D4, 1)
  if ch&0x20==0x20:
    GPIO.output(LCD_D5, 1)
  if ch&0x40==0x40:
    GPIO.output(LCD_D6, 1)
  if ch&0x80==0x80:
    GPIO.output(LCD_D7, 1)
  GPIO.output(LCD_EN, 1)
  time.sleep(0.0005)
  GPIO.output(LCD_EN, 0)

  # Low bits
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if ch&0x01==0x01:
    GPIO.output(LCD_D4, 1)
  if ch&0x02==0x02:
    GPIO.output(LCD_D5, 1)
  if ch&0x04==0x04:
    GPIO.output(LCD_D6, 1)
  if ch&0x08==0x08:
    GPIO.output(LCD_D7, 1)
  GPIO.output(LCD_EN, 1)
  time.sleep(0.0005)
  GPIO.output(LCD_EN, 0)

def lcddata(ch): 
  GPIO.output(LCD_RS, 1)
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if ch&0x10==0x10:
    GPIO.output(LCD_D4, 1)
  if ch&0x20==0x20:
    GPIO.output(LCD_D5, 1)
  if ch&0x40==0x40:
    GPIO.output(LCD_D6, 1)
  if ch&0x80==0x80:
    GPIO.output(LCD_D7, 1)
  GPIO.output(LCD_EN, 1)
  time.sleep(0.0005)
  GPIO.output(LCD_EN, 0)

  # Low bits
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if ch&0x01==0x01:
    GPIO.output(LCD_D4, 1)
  if ch&0x02==0x02:
    GPIO.output(LCD_D5, 1)
  if ch&0x04==0x04:
    GPIO.output(LCD_D6, 1)
  if ch&0x08==0x08:
    GPIO.output(LCD_D7, 1)
  GPIO.output(LCD_EN, 1)
  time.sleep(0.0005)
  GPIO.output(LCD_EN, 0)
  
# String function on LCD
def lcdstring(Str, line):
    lcdcmd(0x80 | line) # Set the cursor to the start of the line
    for char in Str:
        lcddata(ord(char))

# Home Page on LCD Display
lcd_init()
lcdcmd(0x01)
lcdstring("Raspberry Pi", 0x00)
lcdcmd(0xc0)
lcdstring("Weather Station", 0x40)
time.sleep(8) # 8 second delay


# main() function

def main():
    print ('System Ready...')
    URL = 'https://api.thingspeak.com/update?api_key=%s' % key # Thingspeak URL
    #print (URL)
    #print ("Wait....")
    while True:
            (humid, temp)= readDHT()

            # Print temp and humid on display
            lcdcmd(0x01) #clear the display
            lcdstring(f"Humid: {humid}%", 0x00)
            lcdstring(f"Temp: {temp}°C", 0x40)

            # Generate the final URL
            finalURL = f"{URL}&field1={humid}&field2={temp}"
            print(finalURL)
            s=urllib.request.urlopen(finalURL)
            print (f"Sent: Humidity = {humid}%, Temperature = {temp}°C") # Data sent to Thingspeak platform
            s.close()
            time.sleep(10) # Send new data after every 10 seconds

if __name__ == "__main__":
    main()
