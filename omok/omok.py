from multiprocessing import Process, cpu_count

from omok.display import *
from omok.adversarial import *

# Main Process (display, event control ...): 1
# Adversarial Search Engine: others
NumCPU = cpu_count()

class system:
    def __init__(self) -> None:
        self.display = display()
        pass