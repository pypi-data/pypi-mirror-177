import signal
import sys

def KeyboardInterruptHandler(signal, frame):
    print("\nProcess terminated due to keyboard interrupt.")
    sys.exit(0)

try:
    signal.signal(signal.SIGINT, KeyboardInterruptHandler) # For CTRL+C
    signal.signal(signal.SIGTSTP, KeyboardInterruptHandler) # For CTRL+Z
except Exception:
    """
    SIGTSTP might not be supported in windows and that is why is error handling
    """
    pass
