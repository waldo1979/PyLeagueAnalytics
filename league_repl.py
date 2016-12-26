from LolSci import LolAPI
from ptpython.repl import embed

if __name__ == '__main__':
    ls = LolAPI()
    embed(globals(), locals())