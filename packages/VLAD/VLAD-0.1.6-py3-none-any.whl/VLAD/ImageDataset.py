import torch
from types import SimpleNamespace
from pathlib import Path

from .utils import *
from .Descriptors import compute_SIFT

class ImageDataset(torch.utils.data.Dataset):
  """This class handle data loading - Pytorch style
  """
  default_conf = {
      'globs': ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG'],
      'grayscale': False,
      'interpolation': 'cv2_area'
  }
  def __init__(self, root, conf, paths = None):
    """This function read and save paths of a folder of images
    """
    self.conf = conf = SimpleNamespace(**{**self.default_conf, **conf})
    self.root = root
    paths = []
    for g in conf.globs:
      paths += list(Path(root).glob('**/'+g))
    if len(paths) == 0:
      raise ValueError(f'Could not find any image in root: {root}.')
    paths = sorted(list(set(paths)))
    self.names = [i.relative_to(root).as_posix() for i in paths]
  
  def __getitem__(self, idx):
    """This function is used to load specific item from ImageDataset.
    The load is performed only when specific idx is called -> saving RAM
    """
    name = self.names[idx]
    image = read_image(self.root/name)
    size = image.shape[:2][::-1]
    feature = compute_SIFT(image)
    data = {
        'image': image,
        'feature': feature
    }
    return data
  def __len__(self):
    return len(self.names)