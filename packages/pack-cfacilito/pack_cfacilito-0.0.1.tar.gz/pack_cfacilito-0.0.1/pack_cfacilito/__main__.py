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

logging.basicConfig(level=logging.DEBUG) #que imprima mensajes de tipo DEBUG para abajo

if __name__ == '__main__':
    logging.debug('>>> Comienza ejecucion desde dentro de __main__.py\n')
    workshops = unreleased()
    logging.debug(unreleased.__doc__) #imprime el atributo de documentacion de la funcion
    print(workshops)
    logging.debug('\n>>> Finaliza ejecucion desde dentro de __main__.py')