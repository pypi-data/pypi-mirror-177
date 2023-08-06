from torch import nn


#
# Classification Model
#
class CNNClassifier(nn.Module):

    def __init__(self):
        super().__init__()
        conv_layers = []
        kernel_size_conv = (5, 5)
        stride_conv = (1, 1)
        padding_conv = (2, 2)

        kernel_size_pool = (2, 2)
        stride_pool = (2, 2)

        # 1 Convolution Block with Relu.
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(5, 5), stride=(1, 3), padding=(2, 3))
        self.relu1 = nn.ReLU()
        self.mp1 = nn.MaxPool2d(kernel_size=kernel_size_pool, stride=stride_pool)
        self.bn1 = nn.BatchNorm2d(16)
        self.dp1 = nn.Dropout(0.2)
        nn.init.xavier_uniform_(self.conv1.weight)
        self.conv1.bias.data.zero_()
        conv_layers += [self.conv1, self.relu1, self.mp1, self.dp1, self.bn1]

        # 2 Convolution Block
        self.conv2 = nn.Conv2d(16, 32, kernel_size=kernel_size_conv, stride=stride_conv, padding=padding_conv)
        self.relu2 = nn.ReLU()
        self.mp2 = nn.MaxPool2d(kernel_size=kernel_size_pool, stride=stride_pool)
        self.bn2 = nn.BatchNorm2d(32)
        nn.init.xavier_uniform_(self.conv2.weight)
        self.conv2.bias.data.zero_()
        conv_layers += [self.conv2, self.relu2, self.mp2, self.bn2]

        # 3 Convolution Block
        self.conv3 = nn.Conv2d(32, 64, kernel_size=kernel_size_conv, stride=stride_conv, padding=padding_conv)
        self.relu3 = nn.ReLU()
        self.mp3 = nn.MaxPool2d(kernel_size=kernel_size_pool, stride=stride_pool)
        self.bn3 = nn.BatchNorm2d(64)
        nn.init.xavier_uniform_(self.conv3.weight)
        self.conv3.bias.data.zero_()
        conv_layers += [self.conv3, self.relu3, self.mp3, self.bn3]

        # 4 Convolution Block
        self.conv4 = nn.Conv2d(64, 128, kernel_size=kernel_size_conv, stride=stride_conv, padding=padding_conv)
        self.relu4 = nn.ReLU()
        self.mp4 = nn.AvgPool2d(kernel_size=kernel_size_pool, stride=stride_pool)
        self.bn4 = nn.BatchNorm2d(128)
        nn.init.xavier_uniform_(self.conv4.weight)
        self.conv4.bias.data.zero_()
        conv_layers += [self.conv4, self.relu4, self.mp4, self.bn4]

        # 5 Convolution Block
        self.conv5 = nn.Conv2d(128, 128, kernel_size=kernel_size_conv, stride=stride_conv, padding=padding_conv)
        self.relu5 = nn.ReLU()
        self.mp5 = nn.MaxPool2d(kernel_size=kernel_size_pool, stride=stride_pool)
        self.bn5 = nn.BatchNorm2d(128)
        nn.init.xavier_uniform_(self.conv5.weight)
        self.conv5.bias.data.zero_()
        conv_layers += [self.conv5, self.relu5, self.mp5, self.bn5]

        self.convs = nn.Sequential(*conv_layers)

        # Linear Layers
        self.lin1 = nn.Linear(in_features=512, out_features=128)
        self.lin2 = nn.Linear(in_features=128, out_features=2)

        # Dropout Layers
        self.dp2 = nn.Dropout(0.4)
        self.dp3 = nn.Dropout(0.4)

        # Softmax Layer
        self.sm = nn.Softmax(dim=1)

    #
    # Forward pass
    #
    def forward(self, x):
        # Convs Layers
        x = self.convs(x)

        x = x.view((x.shape[0], 512))

        # Linear Layer 1
        x = self.lin1(x)
        x = self.dp2(x)

        # Linear Layer 2
        x = self.lin2(x)
        x = self.dp3(x)

        # Softmax Layer
        x = self.sm(x)
        return x
