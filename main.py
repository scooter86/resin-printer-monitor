from machine import I2C, SPI, Pin
import time
import CCS811
import si7021
import sh1106

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq =10000)
spi = SPI(1, baudrate=1000000)

temp_sensor = si7021.Si7021(i2c)
CCS811_ADDR = const(0x5A) 
aq_sensor = CCS811.CCS811(i2c, addr=CCS811_ADDR)
display = sh1106.SH1106_SPI(128, 64, spi, Pin(5), Pin(2), Pin(4))
relay_pin = Pin(15, Pin.OUT)

while True:
    checkData = aq_sensor.data_available()
    t = temp_sensor.temperature
    rh = temp_sensor.relative_humidity
    if checkData:
        aq_sensor.put_envdata(humidity=rh,temp=t)   # Compensate Temp/Humidity Error
        aq_sensor.readSensorData()
        co2 = aq_sensor.eCO2
        voc = aq_sensor.tVOC
        print("Temperature is {}".format(t))
        print("Humidity is {}".format(rh))
        print('CO2 level: {}{} '.format(str(co2), ' ppm  '), end='')
        print('tVOC level: {}{}'.format(str(voc), ' ppb '))
        if t<= 26:
            relay_pin.value(1)
            display.reset()
            display.sleep(False)
            display.fill(0)
            display.text('Temp {} C'.format(str(t)), 0, 0, 1)
            display.text('Humid {}%'.format(str(rh)), 0, 8, 1)
            display.text('CO2 {} ppm'.format(str(co2)), 0, 16, 1)
            display.text('tVOC {} ppb'.format(str(voc)), 0, 24, 1)
            display.text('Heating', 0, 32, 1)
            display.show()
            time.sleep(60)
        elif t>= 29:
            relay_pin.value(0)
            display.reset()
            display.sleep(False)
            display.fill(0)
            display.text('Temp {} C'.format(str(t)), 0, 0, 1)
            display.text('Humid {}%'.format(str(rh)), 0, 8, 1)
            display.text('CO2 {} ppm'.format(str(co2)), 0, 16, 1)
            display.text('tVOC {} ppb'.format(str(voc)), 0, 24, 1)
            display.text('Check Temp', 0, 32, 1)
            display.show()
            time.sleep(60)
        else:
            display.reset()
            display.sleep(False)
            display.fill(0)
            display.text('Temp {} C'.format(str(t)), 0, 0, 1)
            display.text('Humid {}%'.format(str(rh)), 0, 8, 1)
            display.text('CO2 {} ppm'.format(str(co2)), 0, 16, 1)
            display.text('tVOC {} ppb'.format(str(voc)), 0, 24, 1)
            display.text('Normal', 0, 32, 1)
            display.show()
            time.sleep(30)
    else:
        display.reset()
        display.sleep(False)
        display.fill(0)
        display.text('Sensor Error', 0, 0, 1)
        display.show()
        time.sleep(20)