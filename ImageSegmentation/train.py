from tqdm import tqdm
import torch

def train_epoch(data_loader, model, optimizer, loss_fn,device):
    """
    Function for a single epoch of training the model using the provided data loader, optimizer, and loss function.

    Args:
        data_loader: DataLoader providing batches of training data.
        model: The deep learning model to be trained.
        optimizer: The optimization algorithm (e.g., SGD, Adam) for updating model parameters.
        loss_fn: The loss function to compute the training loss.
        

    Returns:
        None

    Note:
        This function performs a single pass of training over the entire dataset.
        The model should be in training mode before calling this function.

    Instructions:
        Implement the training loop for the provided model and data loader.
        - Iterate over the batches of data from the data loader.
        - Move data and targets to the appropriate device (e.g., GPU).
        - Forward pass: Compute predictions using the model.
        - Compute the loss between predictions and targets using the provided loss function.
        - Backward pass: Zero the gradients, backpropagate the loss, and update model parameters using the optimizer.
        - Update the tqdm loop to display the loss for each batch.

      
    """
    loop = tqdm(data_loader)

    # START YOUR CODE HERE
    for (batch, (image, mask)) in enumerate(loop):
        # send the input to the device
        image = image.to(device)
        mask = mask.to(device)
        preds = model(image)

		# perform a forward pass and calculate the training loss
        loss = loss_fn(preds, mask)
        
		# first, zero out any previously accumulated gradients, then perform backpropagation, and then update model parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loop.set_postfix(loss=loss.item())
    # END YOUR CODE HERE
