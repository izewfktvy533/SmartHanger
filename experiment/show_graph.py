#!/usr/bin/env pytho3
from matplotlib import pyplot as plt
import numpy as np
import ast
import json
import os

PATH = "./data/"
ADDR1 = '0x13a20040b87934'
ADDR2 = '0x13a2004099421a'



for file in sorted(os.listdir(PATH)):
    print(file)

    center_hum_addr1_lst = []
    left_hum_addr1_lst = []
    right_hum_addr1_lst = []

    center_tem_addr1_lst = []
    left_tem_addr1_lst = []
    right_tem_addr1_lst = []



    with open(PATH + file, 'r', encoding='utf-8') as f:
        datum_lst = f.readlines()

        for data_str in datum_lst:
            try:
                data_dit = ast.literal_eval(data_str)
                
                if data_dit['address'] == ADDR2:
                    center_hum_addr1_lst.append(data_dit['center_hum'])
                    left_hum_addr1_lst.append(data_dit['left_hum'])
                    right_hum_addr1_lst.append(data_dit['right_hum'])
                    center_tem_addr1_lst.append(data_dit['center_tem'])
                    left_tem_addr1_lst.append(data_dit['left_tem'])
                    right_tem_addr1_lst.append(data_dit['right_tem'])

            except:
                None

    left_diff_hum_addr1_lst  = list(np.array(left_hum_addr1_lst)   - np.array(center_hum_addr1_lst))
    right_diff_hum_addr1_lst = list(np.array(right_hum_addr1_lst)  - np.array(center_hum_addr1_lst))
    left_diff_tem_addr1_lst  = list(np.array(center_tem_addr1_lst) - np.array(left_tem_addr1_lst))
    right_diff_tem_addr1_lst = list(np.array(center_tem_addr1_lst) - np.array(right_tem_addr1_lst))
    

    plt.plot(range(len(left_diff_hum_addr1_lst)), left_diff_hum_addr1_lst, color='blue', linestyle='solid', linewidth=1, label="left")
    plt.title("left hum", fontsize=14)
    plt.show()
        
    plt.plot(range(len(right_diff_hum_addr1_lst)), right_diff_hum_addr1_lst, color='blue', linestyle='solid', linewidth=1, label="right")
    plt.title("right hum", fontsize=14)
    plt.show()
    
    plt.plot(range(len(left_diff_tem_addr1_lst)), left_diff_tem_addr1_lst, color='red', linestyle='solid', linewidth=1, label="left")
    plt.title("left tem", fontsize=14)
    plt.show()
        
    plt.plot(range(len(right_diff_tem_addr1_lst)), right_diff_tem_addr1_lst, color='red', linestyle='solid', linewidth=1, label="right")
    plt.title("right tem", fontsize=14)
    plt.show()
    


#plt.savefig(u".png", dpi=300)
#plt.legend()
#plt.title("", fontsize=14)
#plt.xlabel("", fontsize=12)
#plt.ylabel("", fontsize=12)
#plt.xlim()
#plt.ylim()
