import torch
import torch.nn as nn
import torchvision.transforms.functional as TF

class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        """
        Initialize a double convolution block.

        Args:
            in_channels (int): Number of input channels.
            out_channels (int): Number of output channels.

        This class defines a block that consists of two sequential convolutional layers
        followed by batch normalization and ReLU activation. It is typically used as a
        building block within the UNet architecture.

        Forward Pass:
            - Input shape: (batch_size, in_channels, H, W)
            - Output shape: (batch_size, out_channels, H, W)

        Example:
            If you create a DoubleConv block with in_channels=64 and out_channels=128,
            the forward pass will take an input tensor of shape (batch_size, 64, H, W),
            apply two convolutional layers, and produce an output tensor of shape
            (batch_size, 128, H, W).
        """
        
        super(DoubleConv, self).__init__()
        
        ### START YOUR CODE HERE
        
        self.conv=torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.ReLU(inplace=True)
        )
    
        ### END YOUR CODE HERE
        
    def forward(self, x):
        """
        Forward pass through the double convolution block.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, in_channels, H, W).

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, out_channels, H, W).

        """
        return self.conv(x)

### Unet
class UNET(nn.Module):
    def __init__(
            self, in_channels=3, out_channels=1, features=[64, 128, 256, 512],
    ):
        """
        Initialize a U-Net architecture.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            features (list): List of integers representing the number of features at each U-Net level.

        This class defines a U-Net architecture for image segmentation tasks. It consists of an
        encoder (downsampling path), a bottleneck, and a decoder (upsampling path).


        Example:
        If you create a UNET with in_channels=3, out_channels=1, and features=[64, 128, 256, 512],
        the forward pass will take an input tensor of shape (batch_size, 3, H, W), process it
        through the U-Net architecture, and produce an output tensor of shape (batch_size, 1, H, W)
        for binary segmentation.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, in_channels, H, W).
            return_skipconnections (bool): Whether to return skip connections (default is False).

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, out_channels, H, W).
            list: List of skip connections if `return_skipconnections` is True.
        """
        super(UNET, self).__init__()
        self.ups = nn.ModuleList()
        self.downs = nn.ModuleList()
        

        ### START YOUR CODE HERE
        ### the components

        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)

        ##Decoder

        ##Encoder
        self.downs.append(DoubleConv(in_channels=in_channels, out_channels=features[0]))
        self.ups.append(torch.nn.ConvTranspose2d(in_channels=features[-1]*2, out_channels=features[-1], kernel_size=2, stride=2))
        self.ups.append(DoubleConv(in_channels=features[-1]*2, out_channels=features[-1]))
        for i in range(1, len(features)):
            self.downs.append(DoubleConv(in_channels=features[i-1], out_channels=features[i]))
            self.ups.append(torch.nn.ConvTranspose2d(in_channels=features[-1*(i+1)]*2, out_channels=features[-1*(i+1)], kernel_size=2, stride=2))
            self.ups.append(DoubleConv(in_channels=features[-1*(i+1)]*2, out_channels=features[-1*(i+1)]))
        self.bottleneck=DoubleConv(in_channels=features[-1], out_channels=features[-1]*2)
        self.final_conv=torch.nn.Conv2d(features[0], out_channels, kernel_size=1)

        ### END YOUR CODE HERE

    def forward(self, x, return_skipconnections=False):
        skip_connections=[]
        ### START YOUR CODE HERE
        for module in self.downs:
            x = module(x)
            skip_connections.append(x)
            x = self.pool(x)
        # Bottleneck
        x = self.bottleneck(x)
        c = -1 # skip connections index
        for i in range(0, len(self.ups)-1, 2):
            upconv = self.ups[i]
            doubleconv = self.ups[i+1]
            skip = skip_connections[c]

            x = upconv(x)

            # Resize x so it can be concatenated to skip_connections
            if x.shape != skip.shape:
                x = TF.resize(x, size=skip.shape[2:])
            x_combined = torch.concatenate((skip, x), axis=1)

            x = doubleconv(x_combined)

            c -= 1
        x = self.final_conv(x)
        ### END YOUR CODE HERE
        if return_skipconnections:
            return x, skip_connections
        return x

