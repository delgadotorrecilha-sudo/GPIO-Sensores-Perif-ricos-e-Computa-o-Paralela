import RPi.GPIO as GPIO
import threading
import time


# Configurações de Pinos 
LED_PIN = 18      # Pino conectado ao LED
BUTTON_PIN = 12   # Pino conectado ao Botão


# Variáveis Globais Compartilhadas 
# Frequência inicial do LED (1.0 segundo)
blink_interval = 1.0 
# Mutex para proteger o acesso à variável blink_interval
interval_lock = threading.Lock() 
# Flag para indicar quando o programa deve ser encerrado
countdown_finished = False


def countdown_task(duration):
    """
    Thread 1: Realiza a contagem regressiva de forma independente.
    Ao final da contagem, funciona como um callback imprimindo na tela e sinalizando o encerramento.
    """
    global countdown_finished
    print(f"Iniciando contagem regressiva de {duration} segundos...")
    
    # Simula a contagem do tempo sem travar o restante do programa
    time.sleep(duration)
    
    print("\n[Callback] Contagem regressiva finalizada!")
    countdown_finished = True


def led_blink_task():
    """
    Thread 2: Controla o piscar do LED utilizando a frequência definida.
    O Mutex é utilizado para ler a variável global com segurança.
    """
    print("Tarefa de Blink LED iniciada.")
    while not countdown_finished:
        # Adquire o Mutex para ler o valor de intervalo sem risco de condição de corrida
        with interval_lock:
            current_interval = blink_interval
        
        # Liga e desliga o LED com base no intervalo atual
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(current_interval / 2)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(current_interval / 2)
        
    print("Encerrando a tarefa do LED.")


def change_frequency_callback(channel):
    """
    Callback de Interrupção: Chamado sempre que o botão for pressionado.
    """
    global blink_interval
    
    # Adquire o Mutex para alterar o valor da variável de forma segura
    with interval_lock:
        # Alterna entre 1.0s (lento) e 0.2s (rápido)
        if blink_interval == 1.0:
            blink_interval = 0.2
            print("\n[Botão] Frequência do LED alterada: RÁPIDA")
        else:
            blink_interval = 1.0
            print("\n[Botão] Frequência do LED alterada: LENTA")


def main():
    # Configura a numeração dos pinos
    GPIO.setmode(GPIO.BCM)
    
    # Configuração dos pinos de entrada e saída
    GPIO.setup(LED_PIN, GPIO.OUT)
    # Configura o botão com resistor de Pull-Up interno
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # Configura a detecção de borda de descida para o botão
    # O parâmetro bouncetime (300ms) evita falsas leituras
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=change_frequency_callback, bouncetime=300)


    # Cria as threads apontando para as funções correspondentes
    t_countdown = threading.Thread(target=countdown_task, args=(15,)) # Conta 15 segundos
    t_led = threading.Thread(target=led_blink_task)


    try:
        # Inicia a execução concorrente das threads
        t_countdown.start()
        t_led.start()


        # O main thread aguarda as outras threads finalizarem (join)
        t_countdown.join()
        t_led.join()


    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário (CTRL+C).")
        
    finally:
        # Limpa as configurações da GPIO e evita curtos-circuitos
        GPIO.cleanup()
        print("Programa finalizado.")


if __name__ == "__main__":
    main()
