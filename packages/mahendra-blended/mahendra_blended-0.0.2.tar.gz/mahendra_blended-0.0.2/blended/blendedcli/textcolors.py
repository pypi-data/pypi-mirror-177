
from colorama import Fore as foreground, Back as background, Style, init 

init(autoreset=True)

class COLORS:
    # Different color codes
    BLUE =  foreground.BLUE
    CYAN  = foreground.LIGHTCYAN_EX or foreground.CYAN
    GREEN = foreground.LIGHTGREEN_EX or foreground.GREEN
    RED = foreground.LIGHTRED_EX or foreground.RED
    YELLOW = foreground.LIGHTYELLOW_EX or foreground.YELLOW
    WHITE = foreground.WHITE
    # Different color codes in SENTIMENTAL terms
    INFO = BLUE
    WARNING = YELLOW
    ERROR = RED
    #ENDC = WHITE
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    BOLDDIM = Style.BRIGHT + Style.DIM