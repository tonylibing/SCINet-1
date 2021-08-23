#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 18:32:30 2021

@author: amadeu
"""


######## data preprocessing #####
import torch
from collections import Counter
import numpy as np
from numpy import array
from torch.utils.data import Dataset,DataLoader

from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from sklearn.model_selection import train_test_split

import math

# data_file = 'data/traffic.txt'
# seq_size, batch_size, K = 15, 2, 2

        
def data_preprocessing(data_file, seq_size, batch_size, K):
    
    def open_data(data_file):
        with open(data_file, 'r') as f:
            text = f.read()
            
        text = text.split("\n") # there are 862 timesteps after each \n 
        # so we have 17544 elements, and each of these elements have 862 time steps
        text = text[:-1]
        
        all_samples = []
        for sample in text: # each samples consists of 862 time steps
            sample = sample.split(",")
            sample = np.array(sample)
            sample = sample.astype(float)

            all_samples.append(sample)
            
        
        return all_samples


    def create_sequences(all_samples, seq_size, K): 
        x = list()
        y = list()
        
        #data_len = len(all_samples)
        #train_len = math.floor(0.6*data_len)
        #valid_len = math.floor(0.2*data_len)
        #test_len = math.floor(0.2*data_len)
        
        for sample in all_samples: # change here
            
            for i in range(len(sample)):
                
                # i=0
                # seq_size=10
                idx = i + seq_size #sequence end
                
                if (idx+K) > len(sample)-1: 
                    break
                
                # add K positions to label to predict the K next timesteps
                feat_seq, target_seq = sample[i:idx], sample[idx:(idx+K)] # target labels for CNN
                x.append(feat_seq)
                y.append(target_seq)
                    
            
        return array(x), array(y)



    class get_data(Dataset):
        def __init__(self,feature,target):
            self.feature = feature
            self.target = target
        def __len__(self):
            return len(self.feature)
        def __getitem__(self,idx):
            item = self.feature[idx]
            label = self.target[idx]
            return item,label
    
    all_samples = open_data(data_file)#/home/scheppacha/data/trainset.txt')
    
    x, y = create_sequences(all_samples, seq_size, K)
    
    rest_feat, test_feat, rest_targ, test_targ = train_test_split(
            x, y, test_size=0.1) # 10%
    
    train_feat, valid_feat, train_targ, valid_targ = train_test_split(
            rest_feat, rest_targ, test_size=0.222) # 10% in paper
    
    train = get_data(train_feat, train_targ)# 
    valid = get_data(valid_feat, valid_targ)
    test = get_data(test_feat, test_targ)

    
    train_loader = torch.utils.data.DataLoader(train, batch_size, shuffle=True)#  shuffle ensures random choices of the sequences
    valid_loader = torch.utils.data.DataLoader(valid, batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test, batch_size, shuffle=False)

  
    return train_loader, valid_loader, test_loader