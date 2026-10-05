# Luís Carlos Delgado Torrecilha - 15472530
# Beatriz Fonseca Silva - 15653959
from gpiozero import PWMLED
from time import sleep

# Conecta o LED na porta GPIO 18 do Raspberry Pi.
# Usamos o PWMLED para conseguir controlar o brilho (intensidade) de forma suave,
# e não apenas ligar e desligar bruscamente.
led = PWMLED(18)

try:
    # Dá um toque no terminal para avisar que o script está rodando
    print("Programa PWM iniciado no GPIO 18. Pressione CTRL+C para encerrar.")
    
    while True:
        # Primeiro loop: aumenta o brilho gradualmente do zero até o máximo (100%)
        # De 5 em 5 passos para a transição ficar bem fluida
        for i in range(0, 101, 5):
            led.value = i / 100.0  # Converte a porcentagem para um valor entre 0.0 e 1.0
            sleep(0.05)            # Pausa curtinha para dar tempo de enxergar a mudança
            
        # Segundo loop: diminui o brilho aos poucos, voltando do 100% até apagar (0%)
        for i in range(100, -1, -5):
            led.value = i / 100.0
            sleep(0.05)
            
except KeyboardInterrupt:
    # Se você apertar CTRL+C, o programa cai aqui de forma limpa e avisa na tela
    print("\nPrograma interrompido pelo usuário.")
