import numpy as np
import cv2
def tensor_to_numpy_image(tensor, mean, std):
    # Convert tensor to numpy array
    np_img = tensor.numpy()
    # Rearrange channels from (C, H, W) to (H, W, C)
    np_img = np.transpose(np_img, (1, 2, 0))
    
    # Denormalize the image using mean and standard deviation
    np_img = (np_img * std) + mean
    
    # Clip the float values to [0, 1] and convert to uint8
    np_img = np.clip(np_img, 0, 1)
    np_img = (np_img * 255).astype(np.uint8)
    
    return np_img

def visualize_result(image_tensor, result,
                      ground_truth, target_path,
                        ouput_format='regression'):
    # Convert image to numpy array
    
    img_np = tensor_to_numpy_image(image_tensor,
                mean=[0.4623, 0.3856, 0.2822],
                std=[0.2527, 0.1889, 0.1334])
    img_width,img_height,_=img_np.shape
    # Draw ground truth points
    
    if ouput_format == 'regression':
        x, y = ground_truth
        x, y = int(x * img_width), int(y * img_height)
    elif ouput_format == 'heatmap':
        y, x = np.unravel_index(np.argmax(ground_truth), ground_truth.shape)
    else:
        raise ValueError('Invalid ouput_format. Choose "regression" or "heatmap".')
    img_np = cv2.circle(img_np, (int(x), int(y)), 3, (0, 255, 0), -1)
    img_np = cv2.putText(img_np, 'gt', (int(x) + 5, int(y) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # Draw predicted points
    if ouput_format == 'regression':
        x, y = result
        x, y = int(x * img_width), int(y * img_height)
    elif ouput_format == 'heatmap':
        y, x = np.unravel_index(np.argmax(result), result.shape)
    else:
        raise ValueError('Invalid ouput_format. Choose "regression" or "heatmap".')
    img_np = cv2.circle(img_np, (int(x), int(y)), 3, (0, 255, 255), -1)
    img_np = cv2.putText(img_np, 'predict', (int(x) + 5, int(y) + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

    # Save the visualization
    cv2.imwrite(target_path, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
