from .transfer_net import TransferNet
from .util import load_image
import torch
from torchvision.utils import save_image
import os
from glob import glob
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","honeybee_back.settings")
django.setup()

class Transfer:
    def __init__(self, style, module_dir='.'):
        self.style = style
        self.num_residual = 5
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.transfer_net = TransferNet(self.num_residual)
        self.checkpoint_dir = os.path.join(module_dir, "honeybee_user/parameter")
        self.style_path = os.path.join(self.checkpoint_dir, self.style)
        self.style_list = os.listdir(self.checkpoint_dir)
        self.build_model()

    def transform_image(self, src_image_path, des_image_path):
        image = load_image(src_image_path).to(self.device)
        transformed_image = self.transfer_net(image)
        save_image(transformed_image, os.path.join(des_image_path), normalize=False)

    def get_style_name(self):
        return self.style_list

    def change_style(self, style):
        if style not in self.style_list:
            return False
        self.style = style
        return True

    def __len__(self):
        return len(self.style_list)

    def __str__(self):
        out = ""
        for style in self.style_list:
            out += str(style)+","
        return out

    def build_model(self):
        self.transfer_net.to(self.device)
        self.load_model()

    def load_model(self):
        print(f"[*] Load model from {self.style_path}")
        if not os.path.exists(self.style_path):
            os.makedirs(self.style_path)

        if not os.listdir(self.style_path):
            raise Exception(f"[!] No parameter in {self.style_path}")

        parameter_path = glob(os.path.join(self.style_path, f'TransferNet_*.pth'))[-1]
        self.transfer_net.load_state_dict(torch.load(parameter_path,map_location='cpu'))
