

class Colorizer:
    @staticmethod
    def Red(prt): return "\033[91m {}\033[00m" .format(prt)
    @staticmethod
    def Green(prt): return "\033[92m {}\033[00m" .format(prt)
    @staticmethod
    def Yellow(prt): return "\033[93m {}\033[00m" .format(prt)
    @staticmethod
    def LightPurple(prt): return "\033[94m {}\033[00m" .format(prt)
    @staticmethod
    def Purple(prt): return "\033[95m {}\033[00m" .format(prt)
    @staticmethod
    def Cyan(prt): return "\033[96m {}\033[00m" .format(prt)
    @staticmethod
    def LightGray(prt): return "\033[97m {}\033[00m" .format(prt)
    @staticmethod
    def Black(prt): return "\033[98m {}\033[00m" .format(prt)