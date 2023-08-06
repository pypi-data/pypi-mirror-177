import keyboard
from getpass import getpass

class raytux:
    def __init__():
        pass

    def block_key(key:str):
        try:
            keyboard.block_key(key)
        except:
            print(f"Could not find a key by the name of ( {key} )")

    def hide_input(message:str):
        msg = getpass(message)
        return msg