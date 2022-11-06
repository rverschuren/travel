#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:33:29 2021

@author: mib
"""
import argparse
from pathlib import Path
from VeSeg.travel_v3 import travel

'''
consider the use of the function travel instead of travel_nora
'''

#example paths
pth = '../media/'
pth_in = pth + 'pat01'
pth_ext_msk = pth + 'thorax_pred.nii.gz'
pth_trachea = pth + 'trachea.nii.gz'
pth_vessel = pth + 'vessels.nii.gz'


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="image", help="lung image path", default = pth_in)
    parser.add_argument("-m", dest="mask", help="lung mask path", default = pth_ext_msk)
    parser.add_argument("-t", dest="trachea", help="trachea mask path", default = pth_trachea)
    parser.add_argument("-v", dest="vessels", help="vessel mask path", default = pth_vessel)
    args = parser.parse_args()
    
    print("test")
    travel(Path(args.image), Path(args.vessels))



if __name__ == "__main__":
    main()