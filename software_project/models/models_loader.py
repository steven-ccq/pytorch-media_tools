import torch
from models.siamese_net import SiameseNetwork
from models.neural_trans_tools import neural_trans_cnn

# net = SiameseNetwork()
# net.load_state_dict(torch.load('models/net_params1.pkl'))
# neural_trans_cnn.load_state_dict(torch.load('models/vgg19_pretrainedmodel.pth'))

class Classify_model():
    def __init__(self):
        self.state = False
        self.model = SiameseNetwork()

    def load_model(self):
        if not self.state:
            self.model.load_state_dict(torch.load('models/net_params1.pkl'))
            self.state = True

class Neural_trans_model():
    def __init__(self):
        self.state = False
        self.model = neural_trans_cnn

    def load_model(self):
        if not self.state:
            self.model.load_state_dict(torch.load('models/vgg19_pretrainedmodel.pth'))
            self.state = True

classify_model = Classify_model()
neural_trans_model= Neural_trans_model()