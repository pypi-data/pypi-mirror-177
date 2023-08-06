import bleach,consolecmds,requests
CSI = '\033['
def code_to_chars(code):
    return f"{CSI}{code}m"
class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))

class AnsiFore(AnsiCodes):
    BLACK=30
    RED=31
    GREEN=32
    YELLOW=33
    BLUE=34
    MAGENTA=35
    CYAN=36
    WHITE=37
    RESET=39
    LIGHTBLACK_EX=90
    LIGHTRED_EX=91
    LIGHTGREEN_EX=92
    LIGHTYELLOW_EX=93
    LIGHTBLUE_EX=94
    LIGHTMAGENTA_EX=95
    LIGHTCYAN_EX=96
    LIGHTWHITE_EX=97
colours=AnsiFore()
