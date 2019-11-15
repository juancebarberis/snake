#Este módulo fue cedido por los profesores de mi cátedra de Algorítmos I.

'''
Utilidades para interactuar con la terminal en Windows y Unix
'''

def _unix_timed_getch(timeout):
    '''
    Espera hasta _timeout_ segundos una pulsación de tecla de la terminal.
    Si no se pulsó ninguna tecla devuelve el valor por defecto.
    '''
    import string, select, sys

    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    
    if ready:
        character = sys.stdin.read(1)
        if ord(character) == 3:
            raise KeyboardInterrupt
        elif ord(character) == 4:
            raise EOFError
        return character
    
    return ''

def _unix_timed_input(timeout):
    import termios, tty, sys, time

    # Limpiar buffer de stdin
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    
    fd = sys.stdin.fileno()

    old_settings = termios.tcgetattr(fd)
    # Desactivar eco y buffering de la terminal
    tty.setraw(sys.stdin.fileno())

    buffer = ''

    try:
        start_time = time.time()
        elapsed = 0
        while elapsed < timeout:
            buffer += _unix_timed_getch(timeout - elapsed)
            elapsed = time.time() - start_time
    finally:
        # Restaurar eco y buffering de la terminal
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return buffer

def _unix_clear_terminal():
    import os
    os.system('clear')

def _win_timed_input(timeout):
    import msvcrt, time, sys
    
    # Limpiar el buffer de stdin
    while msvcrt.kbhit():
        msvcrt.getch()
    
    buffer = ''
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if msvcrt.kbhit():
            buffer += msvcrt.getch().decode(sys.stdout.encoding)
        time.sleep(timeout / 10)

    return buffer

def _win_clear_terminal():
    import os
    os.system('cls')

def timed_input(timeout):
    '''
    Lee entrada del usuario durante _timeout_ segundos. Devuelve una cadena
    con todas las teclas que el usuario presionó durante ese tiempo.
    
    Si pasan _timeout_ segundos y no se presionó ninguna tecla, devuelve una
    cadena vacía.
    '''
    return _timed_input(timeout)

def clear_terminal():
    '''
    Borra todo el contenido de la terminal y restaura el cursor a la primera 
    posición.
    '''
    _clear_terminal()

try:
    # Detectar al cargar el módulo si estamos en Unix o Windows
    import msvcrt
    _timed_input = _win_timed_input
    _clear_terminal = _win_clear_terminal
except ImportError:
    _timed_input = _unix_timed_input
    _clear_terminal = _unix_clear_terminal