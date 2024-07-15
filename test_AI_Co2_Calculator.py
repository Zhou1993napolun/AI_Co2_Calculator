# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:25:02 2024

@author: tt186
"""

import time
from AI_Co2_Calculator import *

def main():
    print("Program Start...")
    
    # 延时10秒
    time.sleep(50)
    
    print("The delay ends and the program continues...")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    
    test_mesure(start,end)