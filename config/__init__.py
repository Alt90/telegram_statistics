from .config import *
try:
    from .local import *
except ImportError:
    pass