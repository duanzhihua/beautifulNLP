#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @license : Copyright(C), Your Company 
# @Author: Zhang Dong
# @Contact : 1010396971@qq.com
# @Date: 2020-08-26 9:26
# @Description: In User Settings Edit
# @Software : PyCharm
from collections import Counter
import numpy as np


class Vocab(object):
    PAD = 0
    SOS = 1
    EOS = 2
    UNK = 3

    def __init__(self):
        self.word2count = Counter()
        self.reversed = ['<PAD>', '<SOS>', '<EOS>', '<UNK>']
        self.index2word = self.reversed[:]
        self.word2index = {w: i for i, w in enumerate(self.reversed)}
        self.embeddings = None

    def add_words(self, words):
        for word in words:
            if word not in self.word2index:
                self.word2index[word] = len(self.index2word)
                self.index2word.append(word)
        self.word2count.update(words)

    def load_embeddings(self, file_path):
        num_embeddings = 0
        vocab_size = len(self.index2word)
        with open(file_path, 'rb') as f:
            for line in f:
                line = line.split()
                word = line[0].decode('utf-8')
                idx = self.word2index.get(word)
                if idx is not None:
                    vec = np.array(line[1:], dtype=np.float32)
                    if self.embeddings is None:
                        n_dims = len(vec)
                        self.embeddings = np.random.normal(
                            np.zeros((vocab_size, n_dims))).astype(np.float32)
                        self.embeddings[self.PAD] = np.zeros(n_dims)
                    self.embeddings[idx] = vec
                    num_embeddings += 1
        return num_embeddings

    def __getitem__(self, item):
        if type(item) is int:
            return self.index2word[item]
        return self.word2index.get(item, self.UNK)

    def __len__(self):
        return len(self.index2word)

    def size(self):
        return len(self.index2word)
