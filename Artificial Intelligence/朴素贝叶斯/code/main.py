from tools import *


# 分别读取训练集以及测试集，进行文本提取
def data_init():
    file_train = open('Classification/train.txt', 'r')
    file_test = open('Classification/test.txt', 'r')
    file_train_txt = file_train.read().split('\n')[1:-1]
    file_test_txt = file_test.read().split('\n')[1:-1]

    # 分离训练集中的句子和情感，分别存储在
    train_text = []
    train_emotion = []
    sentence_length_list = []
    for _item in file_train_txt:
        _temp = _item.split(' ')
        train_text.append(' '.join(_temp[3:]))
        train_emotion.append(_temp[2])
        sentence_length_list.append(len(_temp) - 3)
    _tv = TfidfVectorizer(use_idf=False)
    _tv_fit = _tv.fit_transform(train_text)
    _ft_name = _tv.get_feature_names_out()

    # 获得训练集的完整稀疏矩阵
    sparse_matrix = regulate(_tv_fit.toarray())
    data = TrainData(_ft_name, sparse_matrix, train_emotion, sentence_length_list)
    return file_test_txt, data


if __name__ == '__main__':
    # 主函数开始
    test_text, train_data = data_init()

    denominator = len(test_text)
    # denominator = 100
    numerator = 0
    # 对于测试集的每一个数据，进行结果的比对
    cnt = 0
    for item in test_text[:]:
        temp = item.split(' ')
        emotion_predict = Predict(' '.join(temp[3:]), train_data)
        if emotion_predict == temp[2]:
            numerator += 1
        cnt += 1
        if cnt % 10 == 0:
            print(emotion_predict, end=' ' if cnt % 200 != 0 else '\n')
        # print(emotion_predict, end=' ' if cnt % 30 != 0 else '\n')
    print('\n\n正确率为：', 100 * round(numerator / denominator, 5), '%')


# 记录拉普拉斯变化赋予不同值的正确率变化，最终稳定在38.2
'''
0.1     0.2     0.3     0.325     0.33     0.34     0.345     0.35     0.375     0.4
37.5    37.6    37.8    38.0      38.1     38.1     38.2      38.2     37.8      37.7

'''