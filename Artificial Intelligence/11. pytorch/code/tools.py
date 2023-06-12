import torch
import os
import random, csv
from torch.utils.data import Dataset, DataLoader
from torch.nn import functional as fu
from torchvision import transforms, models
from torch import nn, optim
from PIL import Image
# 模型可调式参数
batch_size = 16
learning_rate = 0.001
epoch_nums = 20
model_type = 0
optim_type = 0


# 输入为：data/train, data/test
class MyDataset(Dataset):
    def __init__(self, root, resize):
        super(MyDataset, self).__init__()
        self.images_path, self.labels = [], []
        self.root = root
        self.resize = resize

        # 获取到每一个图片的路径
        for i, name in enumerate(sorted(os.listdir(os.path.join(root)))):
            cur_dir = os.path.join(root, name)
            if not os.path.isdir(cur_dir):
                continue

            temp = [os.path.join(root, name, imgdir) for imgdir in os.listdir(cur_dir)]
            self.images_path.extend(temp)
            self.labels.extend([i] * len(os.listdir(cur_dir)))
        assert len(self.images_path) == len(self.labels), 'unknown error'

    def __len__(self):
        return len(self.images_path)

    def __getitem__(self, idx):
        img, label = self.images_path[idx], self.labels[idx]

        tf = transforms.Compose([
            lambda x: Image.open(x).convert('RGB'),  # 根据路径获得彩图
            transforms.Resize((self.resize, self.resize)),  # 进行一些图像处理
            transforms.RandomRotation(0),
            transforms.CenterCrop(self.resize),
            transforms.ToTensor(),  # 将图片转为张量
            transforms.Normalize(mean=[0.485, 0.456, 0.406],  # 对应RGB通道
                                 std=[0.229, 0.224, 0.225])
        ])

        # 将图片，标签转为张量
        img = tf(img)
        label = torch.tensor(label)
        return img, label




class MyCNN(nn.Module):
    def __init__(self):
        super(MyCNN, self).__init__()
        self.stride = 2
        self.conv_unit = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=(5, 5), stride=(self.stride, self.stride)),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, kernel_size=(5, 5), stride=(self.stride, self.stride))
        )
        tmp = torch.randn(batch_size, 3, 224, 224)
        out = self.conv_unit(tmp)
        # out [batch_size, 16, 106/26, 106/26]
        print("out:", out.shape)
        assert True, "break"
        self.fc_input_dim = 16*106*106 if self.stride == 1 else 16*26*26
        self.fc_unit = nn.Sequential(
            nn.Linear(self.fc_input_dim, 1024),
            nn.ReLU(),
            nn.Linear(1024, 128),
            nn.ReLU(),
            nn.Linear(128, 5)
        )

    def forward(self, x):
        x = self.conv_unit(x)
        length = x.size(0)
        x = x.view(length, self.fc_input_dim)
        logits = self.fc_unit(x)
        return logits


# 搭建resnet18神经网络
class Resnet18(nn.Module):
    def __init__(self, classes=5):
        super(Resnet18, self).__init__()
        self.features = models.resnet18(pretrained=True)
        self.features.fc = nn.Linear(512, classes)

    def forward(self, x):
        x = self.features(x)
        return x



