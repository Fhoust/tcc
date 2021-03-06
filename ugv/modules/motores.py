'''Modulo responsavel pelo controle dos motores'''


import time
import RPi.GPIO as io


io.setwarnings(False)

io.setmode(io.BOARD)
io.setup(38, io.OUT)
io.setup(37, io.OUT)
io.setup(36, io.OUT)
io.setup(35, io.OUT)
io.setup(12, io.IN)
io.setup(11, io.IN)
io.setup(15, io.IN)
io.setup(13, io.IN)
io.setup(16, io.IN)

pwmIn1 = io.PWM(38, 100)
pwmIn2 = io.PWM(37, 100)
pwmIn3 = io.PWM(36, 100)
pwmIn4 = io.PWM(35, 100)
pwmIn1.start(0)
pwmIn2.start(0)
pwmIn3.start(0)
pwmIn4.start(0)


def virar(direcao):
    '''Realiza um movimento constante

    Parametros:
    -- direcao: Uma string de acordo com o movimento desejado
    '''
    if direcao == "direita":
        pwmIn2.ChangeDutyCycle(100)
        pwmIn4.ChangeDutyCycle(100)
        time.sleep(1.3)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn1.ChangeDutyCycle(100)
        pwmIn4.ChangeDutyCycle(100)
        time.sleep(1)
        pwmIn1.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "direita fino":
        pwmIn2.ChangeDutyCycle(100)
        pwmIn4.ChangeDutyCycle(100)
        time.sleep(0.2)
        pwmIn1.ChangeDutyCycle(0)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn3.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "esquerda":
        pwmIn1.ChangeDutyCycle(100)
        pwmIn3.ChangeDutyCycle(100)
        time.sleep(1.3)
        pwmIn3.ChangeDutyCycle(0)
        pwmIn1.ChangeDutyCycle(100)
        pwmIn4.ChangeDutyCycle(100)
        time.sleep(1)
        pwmIn1.ChangeDutyCycle(0)
        pwmIn3.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "esquerda fino":
        pwmIn1.ChangeDutyCycle(100)
        pwmIn3.ChangeDutyCycle(100)
        time.sleep(0.1)
        pwmIn1.ChangeDutyCycle(0)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn3.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "frente":
        pwmIn1.ChangeDutyCycle(100)
        pwmIn4.ChangeDutyCycle(100)
        time.sleep(1)
        pwmIn1.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "chegou":
        pwmIn1.ChangeDutyCycle(0)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn3.ChangeDutyCycle(0)
        pwmIn4.ChangeDutyCycle(0)

    elif direcao == "nada":
        pwmIn2.ChangeDutyCycle(100)
        pwmIn3.ChangeDutyCycle(100)
        time.sleep(1)
        pwmIn2.ChangeDutyCycle(0)
        pwmIn3.ChangeDutyCycle(0)

    else:
        io.cleanup()


def lerlinhas():
    '''Le os sensores de IR e com base em seus estados aciona os
    motores, podendo corrigir eventuais erros de direcao'''
    error = 0

    while error != -999:
        seEE = io.input(12)
        seEe = io.input(11)
        seM = io.input(13)
        seDd = io.input(15)
        seDD = io.input(16)

        if seEE == 0 and seEe == 1 and seM == 1 and seDd == 1 and seDD == 1:
            error = -4
        elif seEE == 0 and seEe == 0 and seM == 1 and seDd == 1 and seDD == 1:
            error = -3
        elif seEE == 1 and seEe == 0 and seM == 1 and seDd == 1 and seDD == 1:
            error = -2
        elif seEE == 1 and seEe == 0 and seM == 0 and seDd == 1 and seDD == 1:
            error = -1
        elif seEE == 1 and seEe == 1 and seM == 0 and seDd == 1 and seDD == 1:
            error = 0
        elif seEE == 1 and seEe == 1 and seM == 0 and seDd == 0 and seDD == 1:
            error = 1
        elif seEE == 1 and seEe == 1 and seM == 1 and seDd == 0 and seDD == 1:
            error = 2
        elif seEE == 1 and seEe == 1 and seM == 1 and seDd == 0 and seDD == 0:
            error = 3
        elif seEE == 1 and seEe == 1 and seM == 1 and seDd == 1 and seDD == 0:
            error = 4
        elif seEE == 0 and seEe == 0 and seM == 0 and seDd == 0 and seDD == 0:
            error = -999
            pwmIn1.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn4.ChangeDutyCycle(0)

        if error == -4:
            pwmIn4.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(100)
            pwmIn1.ChangeDutyCycle(100)
        elif error == -3:
            pwmIn2.ChangeDutyCycle(0)
            pwmIn4.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(100)
            pwmIn3.ChangeDutyCycle(80)
        elif error == -2:
            pwmIn3.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(100)
            pwmIn4.ChangeDutyCycle(30)
        elif error == -1:
            pwmIn3.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(100)
            pwmIn4.ChangeDutyCycle(50)
        elif error == 0:
            pwmIn2.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(90)
            pwmIn4.ChangeDutyCycle(90)
        elif error == 1:
            pwmIn2.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(50)
            pwmIn4.ChangeDutyCycle(100)
        elif error == 2:
            pwmIn2.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn1.ChangeDutyCycle(30)
            pwmIn4.ChangeDutyCycle(100)
        elif error == 3:
            pwmIn1.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(80)
            pwmIn4.ChangeDutyCycle(100)
        elif error == 4:
            pwmIn1.ChangeDutyCycle(0)
            pwmIn3.ChangeDutyCycle(0)
            pwmIn2.ChangeDutyCycle(100)
            pwmIn4.ChangeDutyCycle(100)


def lerSensores():
    '''Funcao criada para testes dos sensores de IR'''
    while True:
        seEE = io.input(12)
        seEe = io.input(11)
        seM = io.input(13)
        seDd = io.input(15)
        seDD = io.input(16)
        print("%d - %d - %d - %d - %d" % (seEE, seEe, seM, seDd, seDD))
