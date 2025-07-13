
import torch
from torch.utils.data import Dataset
import os
import cv2 as cv 
from PIL import Image
import numpy as np

class SegDataset(Dataset):
    def __init__(self, dir, transform=None):
        """
        Initialize the segmentation dataset.

        Args:
            dir (str): The path to the data directory containing both images and masks.
            transform (callable): A function/transform to apply to the data.
        """

        self.image_dir = os.path.join(dir, 'image')
        self.transform = transform
        self.images = os.listdir(self.image_dir)

    def __len__(self):
        """
        Return the size of the dataset.

        Returns:
            int: The number of samples in the dataset.
            
        """
        #### START YOUR CODE HERE
        return len(self.images)
        ### END YOUR CODE HERE
        

    def __getitem__(self, idx):
        """
        Retrieve and preprocess an image and its corresponding mask.
        Image: (3, 512, 512)
        Mask: (1, 512, 512)

        Args:
            index (int): Index of the sample to retrieve.

        Returns:
            tuple: A tuple containing the preprocessed image and its corresponding mask.
                - image (Tensor): The preprocessed image as a PyTorch tensor.
                - mask (Tensor): The preprocessed mask as a PyTorch tensor.
        """
        img_path = os.path.join(self.image_dir, self.images[idx])
        mask_path = os.path.join(img_path.replace("image", "mask"))

        #### START YOUR CODE HERE
        image = cv.imread(img_path)
        mask = cv.imread(mask_path, cv.IMREAD_GRAYSCALE)
        results = self.transform(image=image, mask=mask)
        image = results["image"]
        mask = results["mask"]
        mask = mask.unsqueeze(0)
        mask = torch.sigmoid(mask)
        mask = (mask > 0.5).float()
        ### END YOUR CODE HERE

        return image, mask
