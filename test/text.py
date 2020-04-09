#!/usr/bin/env python
import argparse


parser = argparse.ArgumentParser(prog="Test parser args")
# parser.add_argument("echo", help="It is first word", type=int,choices=[0,1,2], const = 2)
# parser.add_argument("ass", help="It is number",type=float, const = 3.0)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument("-t","--test",help="Test value", action="store", type = float, default = 2)
parser.add_argument("-s","--set" ,help="Set something new", nargs="?", default = "hello", type=str, dest="sets")
parser.add_argument("-v","--ver", help="Print something beautiful", action="count", default=0)
parser.add_argument("-c","--cer", help="Print something beautifuler", action="store_true")
args = parser.parse_args()

def main():
    print("Start script")
    # print(args.ass**args.echo)
    print("%-10s, %d"%(args.sets,10))
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
