import serial
import struct
import time
import bmp280
import smbus2

import sys

sys.path.append('..')

import crc, variaveis_globais, lcd

# Configuração da porta serial
def configure_serial():
    ser = serial.Serial(port='/dev/serial0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    return ser

# Função pra solicitar o valor do encoder
def encoder(ser, matricula):  
    with variaveis_globais.serial_lock:  
        ser.flushInput()
        message = [0x01, 0x23, 0xC1] + [int(digit) for digit in matricula]
        crcRequest = crc.calcula_CRC(message)  # Calcula o CRC-16
        message = message + crcRequest
        ser.write(bytes(message))  
        # print(f"Mensagem enviada: {bytes(message)}")
        time.sleep(0.200)
        data = ser.read(9)
        # crcCalc = crc.calcula_CRC(data[0:7])
        # segundaParte = data[7:9]
        # if crcCalc == segundaParte:
        dados_byte_array = data[3:7]
        encoder_value =  int.from_bytes(dados_byte_array,"little")
        # print(f"Valor Encoder recebido: {encoder_value}")
        if encoder_value <= 25500:
            return encoder_value
        # else:
        #     print("Erro no CRC")
        #     encoder(ser, matricula)
        #     time.sleep(0.5)

# Função para enviar sinal de controle do Motor PWM
def send_motor_pwm_control(ser, matricula, pwm_value):
    with variaveis_globais.serial_lock:
         # ser.flushInput()
        pwm_value = abs(pwm_value)
        pwm_value_pack = struct.pack('<f', pwm_value)
        print(f"Valor do PWM: {pwm_value}")
        print(f"List do PWM: {list(pwm_value)}")
        message = [0x01, 0x16, 0xC2] + list(pwm_value_pack) + [int(digit) for digit in matricula]
        crcRequest = crc.calcula_CRC(message)  # Calcula o CRC-16
        message = message + crcRequest
        ser.write(bytes(message))

# Função da leitura da temperatura
def get_ambient_temperature():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    # Inicializar o sensor BMP280
    sensor = bmp280.BMP280(i2c_dev=bus, i2c_addr=address)

    # Realizar a leitura da temperatura
    temperature = sensor.get_temperature()

    return temperature

# Função para enviar a temperatura ambiente
def send_ambient_temperature(ser, temperature, matricula):
    with variaveis_globais.serial_lock:
        temperatura = struct.pack('<f', temperature)
        # print(f"Temperatura=: {list(temperatura)}")
        message =[0x01, 0x16, 0xD1] + list(temperatura) +  [int(digit) for digit in matricula]
        crcRequest = crc.calcula_CRC(message)  # Calcula o CRC-16
        message = message + crcRequest
        ser.write(bytes(message))

        # Exibindo a temperatura no LCD
        temperature_string = f"Temp: {temperature:.2f} C"  # Formatando a temperatura
        lcd.lcdLoc(lcd.LINE1)  # Posicionando o cursor no display 
        lcd.typeln(temperature_string)  # Exibindo a temperatura no display


# Função para ler os registradores dos botões
def read_button_registers(ser, matricula):
    with variaveis_globais.serial_lock:
        ser.flushInput()
        quantity = [11]
        message = [0x01, 0x03, 0x00] + quantity + [int(digit) for digit in matricula]
        crcRequest = crc.calcula_CRC(message)  # Calcula o CRC-16
        message = message + crcRequest
        ser.write(bytes(message))
        time.sleep(0.2)
        response = ser.read(16) 
        buttons = [byte for byte in response]
        ignore = buttons[2:-2]
        
        return ignore

# Função para atualizar o estado dos botões
def send_button_registers(ser, adress, state, matricula):
    with variaveis_globais.serial_lock:
        ser.flushInput()
        quantity = [1]
        arrayState = [state]
        message = [0x01, 0x06, adress] + quantity + arrayState + [int(digit) for digit in matricula]
        crcRequest = crc.calcula_CRC(message)  # Calcula o CRC-16
        message = message + crcRequest
        ser.write(bytes(message))
