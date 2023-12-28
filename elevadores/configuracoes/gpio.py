import time
import RPi.GPIO as GPIO
import json

import sys

sys.path.append('..')

import variaveis_globais

DIR1 = 0   
DIR2 = 0
Sensor_Terreo = 0
Sensor_1_andar = 0
Sensor_2_andar = 0
Sensor_3_andar = 0
intensidade_motor = 0
encoder_terreo = 0
encoder_1_andar = 0
encoder_2_andar = 0
encoder_3_andar = 0

def load_json(nomeArquivo):
    with open(nomeArquivo, 'r') as arquivo_json:
        config = json.load(arquivo_json)
    return config

def gpio_config(config):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Configura os pinos GPIO com base nas informações do JSON
    pins_config(config)

def pins_config(config):
    for _, info in config.items():
        pino_bcm = info['BCM']
        modo = info['mode']

        if modo == 'OUT':
            GPIO.setup(pino_bcm, GPIO.OUT)
        elif modo == 'IN':
            GPIO.setup(pino_bcm, GPIO.IN)

def gpio_pins_config(config):
    global DIR1
    global DIR2
    global POTM
    global Sensor_Terreo
    global Sensor_1_andar
    global Sensor_2_andar
    global Sensor_3_andar
    global intensidade_motor

    DIR1 = config['DIR1']['BCM']
    DIR2 = config['DIR2']['BCM']
    POTM = config['POTM']['BCM']
    Sensor_Terreo = config['Sensor_Terreo']['BCM']
    Sensor_1_andar = config['Sensor_1_andar']['BCM']
    Sensor_2_andar = config['Sensor_2_andar']['BCM']
    Sensor_3_andar = config['Sensor_3_andar']['BCM']

    GPIO.setup(DIR1, GPIO.OUT)
    GPIO.setup(DIR2, GPIO.OUT)
    GPIO.setup(POTM, GPIO.OUT)
    GPIO.setup(Sensor_Terreo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Sensor_1_andar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Sensor_2_andar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Sensor_3_andar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(Sensor_Terreo, GPIO.RISING)
    GPIO.add_event_detect(Sensor_1_andar, GPIO.RISING)
    GPIO.add_event_detect(Sensor_2_andar, GPIO.RISING)
    GPIO.add_event_detect(Sensor_3_andar, GPIO.RISING)

    intensidade_motor = GPIO.PWM(POTM, 100) # Intensidade do motor vai até 100%
    intensidade_motor.start(0) # Inicia com 0% de intensidade
    intensidade_motor.ChangeDutyCycle(0) # Inicia com 0% de intensidade
  
def elevador_up():
    variaveis_globais.estado_elevador
    GPIO.output(DIR1, GPIO.HIGH)
    GPIO.output(DIR2, GPIO.LOW)
    variaveis_globais.estado_elevador = 1

def elevador_down():
    variaveis_globais.estado_elevador
    GPIO.output(DIR1, GPIO.LOW)
    GPIO.output(DIR2, GPIO.HIGH)
    variaveis_globais.estado_elevador = 2

def elevador_stoped():
    variaveis_globais.estado_elevador
    GPIO.output(DIR1, GPIO.HIGH)
    GPIO.output(DIR2, GPIO.HIGH)
    variaveis_globais.estado_elevador = 0

def elevador_free():
    GPIO.output(DIR1, GPIO.LOW)
    GPIO.output(DIR2, GPIO.LOW)