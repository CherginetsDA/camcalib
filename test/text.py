#!/usr/bin/env python
import argparse
import os
import sys
import time

parser = argparse.ArgumentParser(prog="Test parser args")
# parser.add_argument("echo", help="It is first word", type=int,choices=[0,1,2], const = 2)
# parser.add_argument("ass", help="It is number",type=float, const = 3.0)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument("-t","--test",help="Test value", action="store", type = int, default = 2)
parser.add_argument("-s","--set" ,help="Set something new", nargs="?", default = "hello", type=str, dest="sets")
parser.add_argument("-v","--ver", help="Print something beautiful", action="count", default=0)
parser.add_argument("-c","--cer", help="Print something beautifuler", action="store_true")
args = parser.parse_args()

def main():
    print("Start")
    xx = 0
    for n in xrange(args.test):
        xx +=1
        sys.stdout.write("\b")
        sys.stdout.write('Hello %d\r' % xx)
        sys.stdout.flush()
        time.sleep(0.1)

        # os.system('clear')
    # print("Start script")
    # print(args.ass**args.echo)
    # print("%-10s, %d"%(args.sets,10))
    # if args.ver:
    #     print("You are smart")
    # if args.cer:
    #     print("You are did it")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    # except:
    #     print("Something is wrong")
