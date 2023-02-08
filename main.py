from pars1 import lenta_parser
from ria import ria_parser

if __name__ == "__main__":
    a = lenta_parser()
    b = ria_parser()
    a.start()
    b.start()