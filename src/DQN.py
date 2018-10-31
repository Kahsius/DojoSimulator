import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.norm = nn.BatchNorm1d(105) 
        self.lin1 = nn.Linear(105, 100)
        self.lin2 = nn.Linear(100, 50)
        self.anar = nn.Linear(50, 6)
        self.sulimo = nn.Linear(50, 6)
        self.ulmo = nn.Linear(50, 6)
        self.wilwar = nn.Linear(50, 6)
        self.sm = nn.Softmax()

    def forward(self, x):
        x = self.norm(x)
        x = F.relu(self.lin1(x))
        x = F.relu(self.lin2(x))
        anar = self.sm(self.anar(x))
        sulimo = self.sm(self.sulimo(x))
        ulmo = self.sm(self.ulmo(x))
        wilwar = self.sm(self.wilwar(x))
        return(torch.cat((anar, sulimo, ulmo, wilwar), 1))

