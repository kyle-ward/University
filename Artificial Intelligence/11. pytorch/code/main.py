import matplotlib.pyplot as plt
from tools import *
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# 绘图变量
loss_train_xs, loss_train_ys = [], []
loss_test_xs, loss_test_ys = [], []
acc_train_xs, acc_train_ys = [], []
acc_test_xs, acc_test_ys = [], []


def main():
    # [batch, 3, len, wid]
    train_db = MyDataset('data\\train', 224)
    test_db = MyDataset('data\\test', 224)

    # assert False, 'break'
    train_loader = DataLoader(train_db, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_db, batch_size=batch_size, shuffle=False)
    ''' 测试输入输出维度的代码
    net = MyNet()
    tmp = torch.randn(32, 3, 224, 224)
    out = net(tmp)
    print('out:', out.shape)
    print('--------------------------------')
    '''

    # 令程序跑在GPU上，参数初始化
    assert torch.cuda.is_available(), 'cuda error'
    device = torch.device('cuda:0')
    # 选择模型并初始化
    if model_type:
        model = Resnet18().to(device)
    else:
        model = MyCNN().to(device)
    # 选择优化器并初始化
    criterion = nn.CrossEntropyLoss()
    if optim_type:
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    else:
        optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    # print(model)  # 打印模型参数

    # 开始训练
    for epoch in range(epoch_nums):
        train_average_loss, test_average_loss = 0.0, 0.0
        train_total_correct, test_total_correct = 0.0, 0.0
        train_total_num, test_total_num = 0.0, 0.0

        # train
        model.train()
        for batchidx, (x, label) in enumerate(train_loader):
            x, label = x.to(device), label.to(device)

            logits = model(x)
            pred = logits.argmax(dim=1)
            train_total_correct += torch.eq(pred, label).float().sum().item()
            train_total_num += x.size(0)
            # logits: [batch_size, 5], label: [batch_size]
            loss = criterion(logits, label)
            train_average_loss += loss.item()
            # 反向传播部分
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_acc = train_total_correct / train_total_num
        train_average_loss /= len(train_loader)
        print('epoch', epoch, ': train_loss ->', train_average_loss, end='\t\t')
        print('epoch', epoch, ': train_accuracy ->', train_acc)
        loss_train_xs.append(epoch), loss_train_ys.append(train_average_loss)
        acc_train_xs.append(epoch), acc_train_ys.append(train_acc)


        # test 无需 backprop
        model.eval()
        with torch.no_grad():
            for x, label in test_loader:
                x, label = x.to(device), label.to(device)
                logits = model(x)
                pred = logits.argmax(dim=1)
                test_total_correct += torch.eq(pred, label).float().sum().item()
                test_total_num += x.size(0)

                loss = criterion(logits, label)
                test_average_loss += loss.item()

            test_acc = test_total_correct / test_total_num
            test_average_loss /= len(test_loader)
            print('epoch', epoch, ': test_loss ->', test_average_loss, end='\t\t')
            print('epoch', epoch, ': test_accuracy ->', test_acc)
            loss_test_xs.append(epoch), loss_test_ys.append(test_average_loss)
            acc_test_xs.append(epoch), acc_test_ys.append(test_acc)
            print('-------------------------------------------------------------')






if __name__ == '__main__':
    main()
    # 绘图部分
    plt.title('loss function')
    plt.plot(loss_train_xs, loss_train_ys, label='train')
    plt.plot(loss_test_xs, loss_test_ys, label='test')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    plt.show()

    plt.title('accuracy function')
    plt.plot(acc_train_xs, acc_train_ys, label='train')
    plt.plot(acc_test_xs, acc_test_ys, label='test')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend()
    plt.show()

