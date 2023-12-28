import threading


botao_terreo_sobe = 0
botao_primeiro_andar_desce = 1
botao_primeiro_andar_sobe = 2
botao_segundo_andar_desce = 3
botao_segundo_andar_sobe = 4
botao_terceiro_andar_desce = 5
botao_emergencia = 6
botao_terreo = 7
botao_primeiro_andar = 8
botao_segundo_andar = 9
botao_terceiro_andar = 10

# Criar um objeto de trava
serial_lock = threading.Lock()
estado_elevador = 0 