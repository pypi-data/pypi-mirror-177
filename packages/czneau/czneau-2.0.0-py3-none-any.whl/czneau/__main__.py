from .czneau import (CCN, CzneauAnalyse)
import sys

def help():
    print('help()')
    pass

def main():
    args = sys.argv[1:]
    if len(args) == 0: # no args
        help()
        return
    for x in args:
        if x[0] != '-': # worng input

            help()
            return
        if x[1] != '-': # -
            for i in x[1:]:
                if i == 'h':
                    help()
                    return
                elif i == '':
                    pass
                else: # worng input
                    help()
                    return
        else: # --
            if x[2:].strip() == 'help':
                help()
                return
            elif x[2:].strip == '':
                pass
            else: # worng input
                help()
                return

if __name__ == '__main__':
    main()
