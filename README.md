# RaspberryPi_Weather_Station
This project entails interfacing a Raspberry Pi 4 development board with a DHT11 sensor module and a 16x2 LCD Display for real-time temperature and humidity measurement. The recordings are then transmitted to the Thingspeak cloud platform for visualization and analysis.
The main components implemented in the project include:
- Raspberry Pi 4
- DHT11 sensor module
- 16x2 LCD Display
- Potentiometer > for adjusting the contrast on the LCD Display
- Thingspeak dashboard -> For receiving, analyzing and visualizing real-time temperature and humidity readings.
  
The [Thingspeak](https://thingspeak.com/) platform is an IoT platform that receives data from IoT devices for analysis, visualization, and to also send alerts. 

In order to connect an IoT device to the Thingspeak platform, a channel is created on Thingspeak, from which an API is generated that is included in the code to link the device to the dashboard:


Once the dashboard starts receiving data, plots can be developed to visualize the data for the parameters, which in this case are temperature and humidity:

