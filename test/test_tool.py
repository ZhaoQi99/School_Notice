'''
Created on Oct 10, 2018

@author: QiZhao
'''
from tool import *


def main():
    Mkdir('Log')
    Mkdir('Log')

    Mkfile('Log/' + 'Exception_log.log')

    Mkfile('Data/test.md', 1)
    Mkfile('Data/test.md', 0)

    Mkfile('Data/test2.md', 1)
    Mkfile('Data/test2.md', 1)

    Log_Write('test_str', 'test_str\n')
    test_list = [['test1_1', 'test1_2', 'test1_3'],
                 ['test2_1', 'test2_2', 'test2_3']]
    Log_Write('test_list', test_list)

    print(time_text())


if __name__ == '__main__':
    main()
