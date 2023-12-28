import threading
import sys
import time
import RPi.GPIO as GPIO


sys.path.append('./configuracoes') 

import uart, gpio, variaveis_globais, pid, lcd

encoder_terreo = 0 #973
encoder_1_andar = 0 #5063
encoder_2_andar = 0
encoder_3_andar = 0 #17153
encoder_atual = 0
botoes_elevador = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pidControl_value = 0
fila = []

def read_lcd(ser, matricula):
    try:
        lcd.lcd_init()
        while True:
            temperature = uart.get_ambient_temperature()
            uart.send_ambient_temperature(ser, temperature, matricula) 
            if variaveis_globais.estado_elevador == 1: 
                string = f"Subindo"
                lcd.lcdLoc(lcd.LINE2)
                lcd.typeln(string) 
            elif variaveis_globais.estado_elevador == 2:
                string = f"Descendo"
                lcd.lcdLoc(lcd.LINE2)
                lcd.typeln(string)
            elif variaveis_globais.estado_elevador == 0:
                string = f"Parado"
                lcd.lcdLoc(lcd.LINE2)
                lcd.typeln(string)

            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x08, lcd.LCD_CMD)

def cacth_encoder_value(ser, matricula):
    global encoder_atual
    while True:
        encoder_atual = uart.encoder(ser, matricula)
        # uart.send_motor_pwm_control(ser, matricula, pidControl_value)
        time.sleep(0.2)

def catch_pwm_control(ser, matricula):
    with variaveis_globais.serial_lock: 
        while True:
            uart.send_motor_pwm_control(ser, matricula, pidControl_value)
            time.sleep(0.2)

def read_button(ser, matricula):
    global botoes_elevador
    while True: 
        botoes_elevador = uart.read_button_registers(ser, matricula)
        time.sleep(0.05)

# Função para sempre atualizar o controle do PID
def update_pid_control(ser, matricula, encoder_atual):
    global pidControl_value
    pidControl_value = pid.pid_controle(encoder_atual) 
    gpio.intensidade_motor.ChangeDutyCycle(abs(pidControl_value))
    # if pidControl_value != 0:
    #     uart.send_motor_pwm_control(ser, matricula, pidControl_value)
    return pidControl_value

def elevador_gage():
    global encoder_terreo
    global encoder_1_andar
    global encoder_2_andar
    global encoder_3_andar

    while True:
        gpio.elevador_up()
        gpio.intensidade_motor.ChangeDutyCycle(5)
        if GPIO.event_detected(gpio.Sensor_Terreo):
            print("Sensor do térreo ativado")
            encoder_terreo = encoder_atual
            print(f"Encoder térreo: {encoder_terreo}")
        
        elif GPIO.event_detected(gpio.Sensor_1_andar):
            print("Sensor do 1º andar ativado")
            encoder_1_andar = encoder_atual
            print(f"Encoder 1 andar: {encoder_1_andar}")
            
        elif GPIO.event_detected(gpio.Sensor_2_andar):
            print(f"Sensor do 2º andar ativado")
            encoder_2_andar = encoder_atual
            print(f"Encoder 2 andar: {encoder_2_andar}")
                        
        elif GPIO.event_detected(gpio.Sensor_3_andar):
            print("Sensor do 3º andar ativado")
            encoder_3_andar = encoder_atual
            print(f"Encoder 3 andar: {encoder_3_andar}")
        if encoder_atual == 25500:
            break

def control_elevator(ser, matricula):
    global fila
    elevador_gage()
    while True:
        if botoes_elevador[0] or botoes_elevador[7]:
            if not encoder_terreo in fila:
                fila.append(encoder_terreo)
                print(f"Fila: {fila}")
                print(f"Fila posição zero: {fila[0]}")
            if encoder_atual >= (encoder_terreo - 200) and  encoder_atual <= (encoder_terreo + 200):
                gpio.elevador_stoped()
                fila.remove(encoder_terreo)
                uart.send_button_registers(ser, 0x00, 0, matricula)
                uart.send_button_registers(ser, 0x07, 0, matricula)
                time.sleep(5)
                print(f"Fila vazia: {fila}")
            else:
                if encoder_atual < encoder_terreo:
                    gpio.elevador_up()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)
                elif encoder_atual > encoder_terreo:
                    gpio.elevador_down()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)

        if botoes_elevador[1] or botoes_elevador[2] or botoes_elevador[8]:
            if not encoder_1_andar in fila:
                fila.append(encoder_1_andar)
                print(f"Fila: {fila}")
                print(f"Fila posição zero: {fila[0]}")
            if encoder_atual >= (encoder_1_andar - 200) and  encoder_atual <= (encoder_1_andar + 200):
                gpio.elevador_stoped()
                fila.remove(encoder_1_andar)
                uart.send_button_registers(ser, 0x01, 0, matricula)
                uart.send_button_registers(ser, 0x02, 0, matricula)
                uart.send_button_registers(ser, 0x08, 0, matricula)
                time.sleep(5)
                print(f"Fila vazia: {fila}")
            else:
                if encoder_atual < encoder_1_andar:
                    gpio.elevador_up()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)
                elif encoder_atual > encoder_1_andar:
                    gpio.elevador_down()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)

        if botoes_elevador[3] or botoes_elevador[4] or botoes_elevador[9]:
            if not encoder_2_andar in fila:
                fila.append(encoder_2_andar)
                print(f"Fila: {fila}")
                print(f"Fila posição zero: {fila[0]}")
            if encoder_atual >= (encoder_2_andar - 200) and  encoder_atual <= (encoder_2_andar + 200):
                gpio.elevador_stoped()
                fila.remove(encoder_2_andar)
                uart.send_button_registers(ser, 0x03, 0, matricula)
                uart.send_button_registers(ser, 0x04, 0, matricula)
                uart.send_button_registers(ser, 0x09, 0, matricula)
                time.sleep(5)
                print(f"Fila vazia: {fila}")
            else:
                if encoder_atual < encoder_2_andar:
                    gpio.elevador_up()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)
                elif encoder_atual > encoder_2_andar:
                    gpio.elevador_down()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)

        if botoes_elevador[5] or botoes_elevador[10]:
            if not encoder_3_andar in fila:
                fila.append(encoder_3_andar)
                print(f"Fila: {fila}")
                print(f"Fila posição zero: {fila[0]}")
            if encoder_atual >= (encoder_3_andar - 200) and  encoder_atual <= (encoder_3_andar + 200):
                gpio.elevador_stoped()
                fila.remove(encoder_3_andar)
                uart.send_button_registers(ser, 0x05, 0, matricula)
                uart.send_button_registers(ser, 0x0A, 0, matricula)
                time.sleep(5)
                print(f"Fila vazia: {fila}")
            else:
                if encoder_atual < encoder_3_andar:
                    gpio.elevador_up()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)
                elif encoder_atual > encoder_3_andar:
                    gpio.elevador_down()
                    pid.pid_atualiza_referencia(fila[0])
                    update_pid_control(ser, matricula, encoder_atual)
                
        time.sleep(0.001)

def emergency_mode():
    while True:
        if botoes_elevador[6]:
            gpio.elevador_stoped()
        time.sleep(0.05)

    
def main():
    ser = uart.configure_serial()
    config = gpio.load_json('config.json')
    gpio.gpio_config(config)
    gpio.gpio_pins_config(config)
    matricula = "1308"
    
    thread1 = threading.Thread(target=read_lcd, args=(ser, matricula,)) 
    thread2 = threading.Thread(target=control_elevator, args=(ser, matricula,))
    thread3 = threading.Thread(target=emergency_mode, args=())
    therad4 = threading.Thread(target=cacth_encoder_value, args=(ser, matricula,))
    thread5 = threading.Thread(target=read_button, args=(ser, matricula,))

    therad4.start()
    thread1.start()
    thread2.start()
    thread3.start()
    
    thread5.start() 
    thread1.join()
    thread2.join()
    thread3.join()
    thread5.join() 
    therad4.join()

    gpio.elevador_free()
    ser.close()

if __name__ == "__main__":
    main()