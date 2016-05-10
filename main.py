#!/usr/bin/env python

from __future__ import print_function

class C:
    RESET   = '\033[0m'
    WHITE   = '\033[1m'
    RED     = '\033[0;31m'
    GREEN   = '\033[0;32m'
    YELLOW  = '\033[0;33m'
    BLUE    = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN    = '\033[0;36m'
    GRAY        = '\033[1;30m'
    BOLD_RED    = '\033[1;31m'
    BOLD_GREEN  = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'

    @staticmethod
    def wrap(color, msg):
        return (color + msg + C.RESET)

class Log:
    @staticmethod
    def info(msg, **kwargs):
        print(msg, **kwargs)
    
    @staticmethod
    def success(msg, **kwargs):
        print(C.wrap(C.BOLD_GREEN, msg), **kwargs)

    @staticmethod
    def error(msg, **kwargs):
        print(C.wrap(C.BOLD_RED, msg), **kwargs)

class Base:
    TITLE = 'base test'
    
    def run(self):
        Log.info('{}... '.format(self.TITLE), end='')
        
        result = self.test()

        if result:
            Log.success('[OK]')
        else:
            Log.error('[Failed]')
            self.print_remedy()

    def test(self):
        raise Exception('must be implemented')
    
    def print_remedy(self):
        raise Exception('must be implemented')

class DefaultAccount(Base):
    TITLE = 'Checking Default Accounts'

    def test(self):
        accounts = ['lp', 'uucp', 'nuucp', 'guest', 'test']

        import pwd

        self.result = []

        for name in accounts:
            if name in [entry.pw_name for entry in pwd.getpwall()]:
                self.result.append(name)

        return not len(self.result) > 0

    def print_remedy(self):
        for name in self.result:
            print('sudo userdel {}'.format(name))

tests = [
        DefaultAccount()
]

def main():
    Log.info('# regular security check for Linux servers')
    Log.info('')

    for index, test in enumerate(tests):
        Log.info('# {}. '.format(index + 1), end='')
        test.run()

if __name__ == '__main__':
    main()
