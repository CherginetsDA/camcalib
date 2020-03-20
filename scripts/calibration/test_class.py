#!/usr/bin/env python
import argparse
import sys
sys.path.append('../..')
import include.calibration as cl

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('-n','--numb', nargs="?", type=int, const=100, default=50, help="Count of pictures")
parser.add_argument('-s','--side', nargs="?", type=float, const=0.0285,default=1, help="Size of square")
parser.add_argument('-c','--conf', action="store_true", help="Config name and path to  save params")
args = parser.parse_args()

def main():
    calib = cl(board_size = (6,9),pict = 150 ,side=args.side)
    calib.calibrate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
