import copy
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


emotion_list = ['anger', 'disgust', 'fear', 'joy', 'sad', 'surprise']


# 词语集频率归一化
def regulate(result):
    for row_index in range(len(result)):
        total = sum(result[row_index])
        for i in range(len(result[row_index])):
            result[row_index][i] /= total
    return result


# 拉普拉斯变换
def Lapras(matrix: list, sentence_length_list: list):
    for index, row in enumerate(matrix):
        # 得到每一行的最小公倍数
        word_num = sentence_length_list[index]
        extra = 0.35
        for i in range(len(row)):
            row[i] = (row[i] * word_num + extra) / (word_num + extra * len(matrix[0]))


class TrainData:
    sparse_matrix = None  # 稀疏矩阵简便存储
    emotion_data = None  # 存储每一行的情感概率分布
    train_data_length = None
    name_list = None  # 矩阵列标题

    # 传入稀疏矩阵的列标题，完整稀疏矩阵，对应的行情感列表
    # 关键是对于测试集相应数据的提取
    def __init__(self, name_list, sparse_matrix, emotion_listed, sentence_length_list):
        Lapras(sparse_matrix, sentence_length_list)
        self.name_list = name_list
        self.sparse_matrix = sparse_matrix
        self.pof_emo_init(emotion_listed)
        self.train_data_length = len(sparse_matrix)
        for i in self.emotion_data[:10]:
            # print(i)
            pass

    # 对于每一行
    def pof_emo_init(self, emotion_listed):
        self.emotion_data = []
        for cur_emo in emotion_listed:
            temp_dict = {}
            for emo in emotion_list:
                if emo == cur_emo:
                    temp_dict[emo] = 0.9
                else:
                    temp_dict[emo] = 0.02
            self.emotion_data.append(temp_dict)


# anger: 6.6%
# disgust: 2.6%
# fear: 16%
# joy: 36.2%
# sad: 20.2%
# surprise: 18.4%
def Predict(sentence: str, train_data: TrainData):
    global emotion_list
    word_list = sentence.split(' ')
    p_list = []
    # 对于每一种情感
    for emo in emotion_list:
        emo_prob = 0
        # 对训练集里面的每一行求和
        for row in range(train_data.train_data_length):
            prob_per_row = 1
            # 对句子里的每一个单词相对于此行的概率求积
            for word in word_list:
                if word in train_data.name_list:
                    index = list(train_data.name_list).index(word)
                    atom_prob = train_data.sparse_matrix[row][index]
                else:
                    # 对于不在训练集中的词，当其不存在，故置为1
                    atom_prob = 1
                if atom_prob:
                    prob_per_row *= atom_prob
            prob_per_row *= train_data.emotion_data[row][emo]
            emo_prob += prob_per_row
        p_list.append(emo_prob)
    # print(p_list)
    # end of initializing p_list
    answer = emotion_list[p_list.index(max(p_list))]
    return answer


# 对测试集数据的检验
if __name__ == '__main__':
    pass
















