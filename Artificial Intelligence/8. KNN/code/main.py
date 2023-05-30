import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import math


p = -1


# 计算两向量之间的距离
def GetDistance(vec1, vec2):
    global p
    distance = 0.0
    dist_vec = vec1 - vec2
    # p-范数
    if p > 0:
        for i in range(len(dist_vec)):
            distance += math.fabs(dist_vec[i]) ** p
        distance = distance ** (1 / p)
    # 无穷范数
    elif p < 0:
        for i in range(len(dist_vec)):
            distance = math.fabs(dist_vec[i]) if math.fabs(dist_vec[i]) > distance else distance
    # 余弦表示法，模采取2-范数
    else:
        numerator = 0
        len1, len2 = 0, 0
        for i in range(len(vec1)):
            numerator += vec1[i] * vec2[i]
            len1 += vec1[i] ** 2
            len2 += vec2[i] ** 2
        distance = - (numerator / math.sqrt(len1 * len2))
        # print(distance)
    return distance


# 数据初始化
def DataInit():
    file_test = open('Classification/test.txt', 'r').read().split('\n')[1:-1]
    data = []
    for item in file_test:
        temp = item.split(' ')
        data.append([temp[2], ' '.join(temp[3:])])
    return data


class KNN:
    accuracy = 0.0

    def __init__(self, data):
        # 将训练集测试集句子放在一起提取特征，避免出现测试集单词训练集中不存在的情况
        # 此举便于向量匹配
        self.N = round((len(data)) * 0.8)
        self.k = round(math.sqrt(self.N)) + 4

        self.data = data
        cv = CountVectorizer()
        cv_fit = cv.fit_transform(np.array(self.data)[:, 1])
        self.train_emotion = np.array(self.data[:self.N])[:, 0]
        self.test_emotion = np.array(self.data[self.N:])[:, 0]
        self.name_list = cv.get_feature_names_out()
        self.matrix = cv_fit.toarray()

        print('N = ', self.N, '  ', 'k = ', self.k)
        print('p = ', p)

    def Solution(self):
        denominator, numerator = len(self.data) - self.N, 0
        cnt = 0
        for i in range(denominator):
            # emotion_predict = self.Predict(i)
            # 对于测试集里的每一个句子，进行情感预测
            emotion_predict = self.Predict(i)
            if emotion_predict == self.test_emotion[i]:
                numerator += 1
            cnt += 1
            print(emotion_predict, end=' ' if cnt % 20 != 0 else '\n')
        self.accuracy = round(numerator / denominator, 5)
        print('\n', self.accuracy)

    def Predict(self, sentence_index):
        emo_dict = {'anger': 0, 'disgust': 0, 'fear': 0, 'surprise': 0, 'sad': 0, 'joy': 0}
        # 获得待预测句子的one-hot向量
        vec = self.matrix[sentence_index + self.N]
        container = []
        for index, train_vec in enumerate(self.matrix[:self.N]):
            temp = [index, GetDistance(vec, train_vec), self.train_emotion[index]]
            container.append(temp)
        # 进行排序并保留前k个样本
        container.sort(key=lambda x: x[1])
        # print(container[:self.k])
        for item in container[:self.k]:
            emo_dict[item[2]] += 1
        return list(emo_dict.keys())[list(emo_dict.values()).index(max(list(emo_dict.values())))]


if __name__ == '__main__':
    Data = DataInit()
    solution = KNN(Data)
    solution.Solution()

