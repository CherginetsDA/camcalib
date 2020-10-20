#!/usr/bin/env python3
import argparse
import sys
sys.path.append('../..')
import include.calibration as cl
CONFIG_FILE_PATH = '../../config/cam_param.json'


parser = argparse.ArgumentParser(prog="Calibration via class include/calibration")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('-n','--numb', nargs="?", type=int, const=100, default=50, help="Count of pictures")
parser.add_argument('-s','--side', nargs="?", type=float, const=0.0285,default=1, help="Size of square")
parser.add_argument('-c','--conf', nargs="?", type=str,const = CONFIG_FILE_PATH, default=CONFIG_FILE_PATH, help="Config name and path to  save params")
args = parser.parse_args()

def main():
    checkerboard = (6,9)
    calib = cl(board_size = checkerboard,pict = args.numb ,side=args.side, conf = args.conf)
    calib.calibrate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
