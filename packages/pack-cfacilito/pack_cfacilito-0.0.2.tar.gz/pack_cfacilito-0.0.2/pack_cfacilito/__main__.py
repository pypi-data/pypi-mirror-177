#este archivo se utiliza para que se puede ejecutar el paquete utilizando unicamente el nombre
# python -m pack_cfacilito
# -m ejecuta por nombre de paquete

from pack_cfacilito import unreleased
import logging

"""
INFO -> 10
DEBUG -> 20
WARNING -> 30 - A partir de aqui para abajo por default
ERROR -> 40 
CRITICAL -> 50
"""

logging.basicConfig(level=logging.INFO) #que imprima mensajes de tipo INFO para abajo

def main():
    logging.info(unreleased())

if __name__ == '__main__':
    logging.debug('>>> Comienza ejecucion desde dentro de __main__.py\n')

    main()
  
    logging.debug('\n>>> Finaliza ejecucion desde dentro de __main__.py')