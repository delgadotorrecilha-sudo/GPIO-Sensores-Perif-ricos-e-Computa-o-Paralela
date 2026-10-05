# Luís Carlos Delgado Torrecilha - 15472530
# Beatriz Fonseca Silva - 15653959
import RPi.GPIO as GPIO  # Puxa a biblioteca para controlar as portas (pinos) da Raspberry Pi
import time              # Puxa a biblioteca de tempo para fazer pausas/esperas

# Define quais pinos físicos da placa serão usados
LED_PIN = 18             # Pino onde o LED está conectado
BIN_PIN = 16             # Pino onde o botão está conectado

# Função chamada automaticamente toda vez que o botão muda de estado (aperta ou solta)
def evento_botao(canal):
    # Se o botão foi apertado (tensão foi para zero/LOW por causa do pull-up)
    if GPIO.input(BIN_PIN) == GPIO.LOW:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Liga o LED
    else:
        GPIO.output(LED_PIN, GPIO.LOW)   # Se soltou o botão, desliga o LED

def main():
    GPIO.setmode(GPIO.BOARD)  # Usa a numeração física dos pinos da placa (1 a 40)
    
    GPIO.setup(LED_PIN, GPIO.OUT)  # Configura o pino do LED como SAÍDA (manda energia)
    
    # Configura o pino do botão como ENTRADA com resistor interno (mantém o pino em 3.3V até ser apertado)
    GPIO.setup(BIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Avisa a placa para vigiar o botão: se mudar de estado (apertar ou soltar), chama a função 'evento_botao'
    # bouncetime=50 evita leituras falsas causadas pelo tremor mecânico do botão
    GPIO.add_event_detect(BIN_PIN, GPIO.BOTH, callback=evento_botao, bouncetime=50)
    
    try:
        print("Sistema iniciado. Pressione o botão para acender o LED (CTRL+C para sair).")
        # Mantém o programa rodando parado em segundo plano para não fechar sozinho
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Se o usuário apertar CTRL+C no teclado, avisa e encerra sem dar erro
        print("\nPrograma interrompido pelo usuário.")
                
    finally:
        # Limpa as configurações dos pinos para deixá-los seguros e prontos para outro uso
        GPIO.cleanup()
            
# Garante que a função principal só rode se o script for executado diretamente
if __name__ == '__main__':
    main()