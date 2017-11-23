

class Colorizer:

    foregrounds = {
        'red': '31',
        'green': '32',
        'yellow': '33',
        'light_purple': '34',
        'purple': '35',
        'cyan': '36',
        'light_grey': '37',
        'black': '38'
    }
    backgrounds = {
        'red': '40',
        'green': '41',
        'yellow': '42',
        'light_purple': '43',
        'purple': '44',
        'cyan': '45',
        'light_grey': '46',
        'black': '47',
        'transparent': '00',
    }
    
    # @classmethod
    # def Red(cls, prt): return "\033[91m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def Green(cls, prt): return "\033[92m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def Yellow(cls, prt): return "\033[93m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def LightPurple(cls, prt): return "\033[94m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def Purple(cls, prt): return "\033[95m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def Cyan(cls, prt): return "\033[96m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def LightGray(cls, prt): return "\033[97m {}\033[00m" .format(cls, prt)
    # @classmethod
    # def Black(cls, prt): return "\033[98m {}\033[00m" .format(cls, prt)

    @classmethod
    def Red(cls, prt): return "\033[31m {}\033[00m" .format(prt)
    @classmethod
    def Green(cls, prt): return "\033[32m {}\033[00m" .format(prt)
    @classmethod
    def Yellow(cls, prt): return "\033[33m {}\033[00m" .format(prt)
    @classmethod
    def LightPurple(cls, prt): return "\033[34m {}\033[00m" .format( prt)
    @classmethod
    def Purple(cls, prt): return "\033[35m {}\033[00m" .format(prt)
    @classmethod
    def Cyan(cls, prt): return "\033[36m {}\033[00m" .format(prt)
    @classmethod
    def LightGray(cls, prt): return "\033[37m {}\033[00m" .format(prt)
    @classmethod
    def Black(cls, prt): return "\033[38m {}\033[00m" .format(prt)
    
    @classmethod
    def custom(cls, prt, foreground='white', background='transparent'):
        if foreground in cls.foregrounds and background in cls.backgrounds:
            fg = cls.foregrounds[foreground]
            bg = cls.backgrounds[background]
            return "\033[%sm {}\033[%sm".format(fg, bg)
        return "\033[91m {}\033[00m" .format(prt)
