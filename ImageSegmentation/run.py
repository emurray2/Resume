import albumentations as A
from dataset import SegDataset
from torch.utils.data import DataLoader
from albumentations.pytorch import ToTensorV2
from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torchvision.transforms.functional as TF
from tqdm import tqdm
from utils import *
from train import train_epoch
import torch.optim as optim

def train_unet(model,device):
    """
    Main training and evaluation function for a binary segmentation model.

    This function performs the following steps:
    1. Define an appropirate loss function for the problem(https://pytorch.org/docs/stable/nn.html#loss-functions) and
        optimizer (https://pytorch.org/docs/stable/optim.html).
    2. Iterate through training epochs:
        - Train the model on the training data using the defined loss function and optimizer.
        - Save the model checkpoint, including the model's state_dict and optimizer's state_dict.
        - Evaluate the model's accuracy, Dice Score, and Jaccard Index on the validation data.
        - Record accuracy, Dice Score, and Jaccard Index for each epoch in a global array(This will be used by you to plot the graphs later).
        - Save prediction examples to a specified folder.

    Args:
        None

    Returns:
        (Tuple[list, list, list]: A tuple containing lists of  for accuracy, Dice Score, and Jaccard Index for each epoch.

    Note:
        - This function assumes the existence of the following variables/constants:
            - model: The binary segmentation model to be trained and evaluated.
            - LEARNING_RATE: The learning rate used for the optimizer.
            - NUM_EPOCHS: The number of training epochs.
            - train_loader: DataLoader for training data.
            - val_loader: DataLoader for validation data.
            - device: The device (e.g., "cuda" or "cpu") on which the model is trained and evaluated.
        - You should provide appropriate values for these variables/constants before calling this function.

    """
    ####################################HYPERPARAMETERS#################################
    learning_rate = 1e-4
    num_epochs = 29
    img_height=img_width=512
    batch_size=2
    train_dir="Data/train" #Enter the path to your train data
    test_dir="Data/test"  #Enter the path to your test data
    save_path="Data/saves" #Enter path to save model ouputs
    ####################################################################################

    ###################################DATA AUGMENTATIONS###############################
    train_transform, val_transform=get_transforms(img_height, img_width)
    ###################################################################################

    ###################################DATALOADERS#####################################
    train_ds = SegDataset(
            dir=train_dir,
            transform=train_transform,
        )

    val_ds = SegDataset(
            dir = test_dir,
            transform=val_transform,
        )

    train_loader = DataLoader(
            train_ds,
            batch_size=batch_size,
            num_workers=1,
            shuffle=True,
        )


    val_loader = DataLoader(
            val_ds,
            batch_size=batch_size,
            num_workers=1,
            shuffle=False,
        )
    ###################################################################################
    #######################MAIN TRAINING LOOP#########################################

    '''
    Main training and evaluation loop for a binary segmentation model.

        In this part perform the following steps:
        1. Define an apporpirate loss function for the problem(https://pytorch.org/docs/stable/nn.html#loss-functions) and
        optimizer (https://pytorch.org/docs/stable/optim.html).
        2. Iterate through training epochs:
            - Train the model on the training data using the defined loss function and optimizer.
            - Save the model checkpoint, including the model's state_dict and optimizer's state_dict.
            - Evaluate the model's accuracy, Dice Score, and Jaccard Index on the validation data.
            - Record accuracy, Dice Score, and Jaccard Index for each epoch in a global array(This will be used by you to plot the graphs later).
            - Save prediction examples to a specified folder.
        
    '''
    ##START YOU CODE HERE
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    accuracy_list = []
    dice_list = []
    jaccard_list = []
    for i in range(num_epochs):
        train_epoch(train_loader, model, optimizer, loss_fn,device)
        checkpoint = {"model": model.state_dict(), "optimizer": optimizer.state_dict()}
        save_checkpoint(checkpoint)
        metrics = check_accuracy(val_loader, model, device)
        accuracy_list.append(metrics[0])
        dice_list.append(metrics[1])
        jaccard_list.append(metrics[2])
        save_predictions_as_imgs(val_loader, model, save_path, device)
    return (accuracy_list, dice_list, jaccard_list)
    ###END CODE HERE