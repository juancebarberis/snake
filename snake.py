from terminal import timed_input, clear_terminal
from random import randint

COLOR_VERDE = '\033[92m'
COLOR_ROJO = '\033[91m'
COLOR_NORMAL = '\033[0m'
SNAKE_MAX_LENGHT = 10       #Largo máximo que puede alcanzar snake.
TABLERO_SIZE = 20           #Tamaño del tablero (ancho y alto).
SPEED = 0.5                 #Tiempo permitido por movimiento.
SNAKE_SYMBOL = 'O'          #Símbolo que caracteriza a snake.
FRUTA_SYMBOL = '#'          #Símbolo que caracteriza a la fruta.

def main():
    fruta = generarFruta()
    movimiento = 'w'
    posCero  = TABLERO_SIZE // 2
    snake   = [(posCero, posCero)]

    while True:
        clear_terminal()

        snake, fruta = checkFruta(movimientoSnake(snake, movimiento), fruta)

        if not checkBordes(snake) or not checkAutoColision(snake):
            print('¡Game Over! :(')
            break
        if len(snake) == SNAKE_MAX_LENGHT:
            print('¡Ganaste! Alcanzaste la longitud máxima de snake.')
            break

        imprimirTablero(generarTablero(), snake, fruta)

        entrada = inputJugada(movimiento)
        if entrada == False:     
            print('Gracias por jugar.')
            break      
        if not entrada == None: 
            movimiento = entrada
    
def movimientoSnake(snake, movimiento):
    """Recibe <SNAKE> y un <MOVIMIENTO>. Agrega una nueva pieza en la
    dirección que recibe por <MOVIMIENTO>. Devuelve <SNAKE> con la nueva pieza."""

    if movimiento == "w": 
        snake.insert(0, (snake[0][0] - 1,snake[0][1]))
    if movimiento == "s":
        snake.insert(0, (snake[0][0] + 1,snake[0][1]))
    if movimiento == "a": 
        snake.insert(0, (snake[0][0],snake[0][1] - 1))
    if movimiento == "d": 
        snake.insert(0, (snake[0][0],snake[0][1] + 1))
    
    return snake

def checkFruta(snake, fruta):
    """Recibe <SNAKE> con la nueva pieza de movimientoSnake() y la posición de
    la <FRUTA>. Comprueba si la nueva pieza está en la misma posición de la fruta.
    Si las posiciones coinciden, genera una nueva fruta con generarFruta() y no
    elimina la última pieza de <SNAKE>. De lo contrario, elimina la última pieza de <SNAKE>.
    Devuelve <SNAKE> y <FRUTA>"""
    
    if snake[0] == fruta: 
        fruta = generarFruta()
    else: 
        snake.pop(-1)
        
    return snake, fruta

def checkBordes(snake):
    """Recibe <SNAKE>. Comprueba que la nueva posición no esté fuera de los límites
    del tablero. Devuelve <False> en caso de estar fuera de los límites."""

    if not (snake[0][0] == -1 or snake[0][1] == -1 or snake[0][0] == TABLERO_SIZE or snake[0][1] == TABLERO_SIZE): 
        return True

def checkAutoColision(snake):
    """Recibe <SNAKE>. Comprueba que la nueva posición no esté sobre otra parte del
    cuerpo de la serpiente. Devuelve <False> en caso de colisionar consigo misma."""
    cabezaSnake = snake[0]
    for i in range(2,len(snake)):
        if snake[i] == cabezaSnake: return False
    return True

def inputJugada(movimiento):
    """Recibe la variable de movimiento. Recibe, medianta input la
    jugada y comprueba que sea válida. Si no es válida, devuelve <NoneType>.
    Comprueba que lo ingresado no sea el opuesto del movimiento anterior."""
    
    entrada = timed_input(SPEED)

    if entrada.isspace():   #Para salir del juego, presiona <SPACE>
        return False  

    if entrada == 'w' and not movimiento == 's': 
        return entrada
    elif entrada == 'a' and not movimiento == 'd':
        return entrada
    elif entrada == 's' and not movimiento == 'w':
        return entrada
    elif entrada == 'd' and not movimiento == 'a':
        return entrada
    return movimiento

def generarTablero():
    """Genera el tablero base de juego a partir de <TABLERO_SIZE>."""
    tablero = []
    for fil in range(TABLERO_SIZE):
        tablero.append([])
        for col in range(TABLERO_SIZE):
            tablero[fil].append('.') 
    return tablero

def imprimirTablero(tablero, snake, fruta):
    """Recibe los componentes del juego (Tablero, Snake y Fruta) y los imprime en el
    orden y posiciones correspondientes."""

    #Agrega Snake al tablero
    for coord in snake:             
        tablero[coord[0]][coord[1]] = COLOR_VERDE + SNAKE_SYMBOL + COLOR_NORMAL

    #Agrega la fruta al tablero
    tablero[fruta[0]][fruta[1]] = COLOR_ROJO + FRUTA_SYMBOL + COLOR_NORMAL  

    #Impresión final del tablero
    for fila in range(TABLERO_SIZE): 
            lst = tablero[fila]
            tableroFinal= ""
            for dot in lst:
                tableroFinal += dot
            print(tableroFinal)

    #Impresión de información
    print(f"Tamaño:[{len(snake)}/{SNAKE_MAX_LENGHT}]")
    print(f"Mover:[w, a, s, d] | Salir:[Espacio/Enter]")

def generarFruta():
    """Genera dos coordenadas al azar en un rango hasta <TABLERO_SIZE>.
    Devuelve las coordenadas en una lista."""
    frutaCol = randint(0, TABLERO_SIZE - 1)
    frutaFil = randint(0, TABLERO_SIZE - 1)

    return (frutaCol, frutaFil)

main()      
