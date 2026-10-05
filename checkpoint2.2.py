# Beatriz Fonseca Silva- 15653959
# Luís Carlos Delgado Torrecilha - 15472530
# Importa as classes DistanceSensor e LED da biblioteca gpiozero
from gpiozero import DistanceSensor, LED
from signal import pause


# Configura os pinos do sensor de ultrassom HC-SR04
# echo=24 e trigger=23 
sensor = DistanceSensor(echo = 24, trigger = 23, max_distance=1, threshold_distance=0.2)


# Configura o pino GPIO conectado ao LED (exemplo: GPIO 18)
led = LED(18)


print("Sensor de distância iniciado. O LED acenderá quando um objeto se aproximar.")
print("Pressione CTRL+C para sair.")


# Atribui a função de ligar o LED quando o sensor detectar um objeto no alcance
sensor.when_in_range = led.on


# Atribui a função de desligar o LED quando o objeto sair do alcance do sensor
sensor.when_out_of_range = led.off


# A função pause() mantém o script em execução indefinidamente aguardando os eventos do sensor
pause()
