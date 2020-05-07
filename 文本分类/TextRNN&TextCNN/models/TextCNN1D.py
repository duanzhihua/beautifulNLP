#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# __author__ = 'zd'
import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, Conv1D, Dropout, Flatten, MaxPool1D, concatenate
import numpy as np


class Config(object):
    def __init__(self, dataset, embedding):
        self.model_name = 'TextCNN1D'
        self.train_path = dataset + '/dataset/train.txt'
        self.dev_path = dataset + '/dataset/dev.txt'
        self.text_path = dataset + '/dataset/test.txt'
        self.class_list = [x.strip() for x in open(dataset + '/dataset/class.txt').readlines()]
        self.vocab_path = dataset + '/embedding/vocab.pkl'
        self.save_path = './results/' + self.model_name + '.h5'
        self.log_path = '../log/' + self.model_name

        self.embedding_matrix = np.load(dataset + '/embedding/' + embedding)['embeddings'].astype('float32') if embedding != 'random' else None

        self.dropout = 0.5
        self.require_improvement = 1000
        self.num_classes = len(self.class_list)
        self.n_vocab = 0    # 词表大小 在运行时赋值
        self.num_epochs = 20
        self.batch_size = 128
        self.max_len = 32
        self.learning_rate = 1e-3
        self.embed = self.embedding_matrix.shape[1] if self.embedding_matrix is not None else 300   # 字向量维度
        self.filter_sizes = (2, 3, 4)   # 卷积核尺寸
        self.num_filters = 256      # 卷积核数量 (channels数)


class MyModel(tf.keras.Model):
    def __init__(self, config):
        super(MyModel, self).__init__()
        self.config = config
        self.embedding = Embedding(
            input_dim=self.config.embedding_matrix.shape[0],
            output_dim=self.config.embedding_matrix.shape[1],
            input_length=self.config.max_len,
            weights=[self.config.embedding_matrix],
            trainable=False
        )
        self.convs = [Conv1D(self.config.num_filters, k,
                             padding='same', strides=1,
                             activation='relu') for k in self.config.filter_sizes]
        self.flatten = Flatten()
        self.dropout = Dropout(self.config.dropout)
        self.out_put = Dense(units=config.num_classes, activation='softmax')

    def conv_and_pool(self, x, conv):
        x = conv(x)
        x = MaxPool1D()(x)
        return x

    def build(self, input_shape):
        super(MyModel, self).build(input_shape)

    def call(self, x):
        x = self.embedding(x)
        x = concatenate([self.conv_and_pool(x, conv) for conv in self.convs], axis=-1)
        x = self.flatten(x)
        x = self.dropout(x)
        x = self.out_put(x)
        return x
