from LolSci import LolSession
from ptpython.repl import embed

if __name__ == '__main__':
    ls = LolSession()
    embed(globals(), locals())