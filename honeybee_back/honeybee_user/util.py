import PIL
from torchvision import transforms


def load_image(file_name, size=224):
    image = PIL.Image.open(file_name).convert("RGB")
    image = transforms.Compose([
        transforms.CenterCrop(min(image.size[0], image.size[1])),
        transforms.Resize(size=size),
        transforms.ToTensor(),
    ])(image).unsqueeze(0)
    return image
