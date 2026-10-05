# Luís Carlos Delgado Torrecilha - 15472530
# Beatriz Fonseca Silva - 15653959
import RPi.GPIO as GPIO
import time

# Definição do pino físico do LED (padrão BOARD)
LED_PIN = 18

def executar_contagem(tempo_segundos):
    print("\nIniciando contagem:")
    
    # Laço de repetição para a contagem regressiva
    for tempo_restante in range(tempo_segundos, -1, -1):
        # Separação em minutos e segundos utilizando divmod
        minutos, segundos = divmod(tempo_restante, 60)
        
        # Formatação MM:SS e atualização na mesma linha 
        # O end='\r' volta o cursor e o flush=True força o terminal a atualizar a tela instantaneamente
        print('{:02d}:{:02d}'.format(minutos, segundos), end='\r', flush=True)
        
        # Aguarda 1 segundo apenas se ainda houver tempo restante
        if tempo_restante > 0:
            time.sleep(1)
            
    # Mensagem indicando o final da contagem
    print("\nContagem finalizada!")
    
    # Aciona e mantém o LED ligado após a contagem
    GPIO.output(LED_PIN, GPIO.HIGH)

def main():
    # Configuração da numeração física e do pino do LED
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    # Garante que o LED inicie apagado
    GPIO.output(LED_PIN, GPIO.LOW)
    
    try:
        # Laço para continuar pedindo o valor até que uma entrada válida seja fornecida
        while True:
            entrada = input("Digite o tempo da contagem regressiva (em segundos): ")
            
            try:
                # Type casting para validar se a entrada é um número inteiro
                tempo = int(entrada)
                
                # Validação para garantir que o número seja positivo
                if tempo < 0:
                    print("Erro: O número deve ser positivo. Tente novamente.")
                    continue
                    
                # Chama a função modularizada da contagem
                executar_contagem(tempo)
                
                # Sai do laço de repetição (while) após a execução correta
                break 
                
            except ValueError:
                # Manipulação de erro para valores inválidos (letras, símbolos) sem forçar a saída do script
                print("Erro: O valor digitado deve ser um número inteiro. Tente novamente.")
                
    except KeyboardInterrupt:
        # Tratamento de exceção para interrupção via teclado (CTRL+C)
        print("\nPrograma interrompido pelo usuário.")
        
    finally:
        # Cleanup do pino após o final ou interrupção do programa
        GPIO.cleanup()

if __name__ == '__main__':
    main()