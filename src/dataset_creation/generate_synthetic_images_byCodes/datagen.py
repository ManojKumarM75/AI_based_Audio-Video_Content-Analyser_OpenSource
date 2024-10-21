import random
import cv2
import numpy as np
import os
import csv
from configurations import DEMO_CONFIG
from tqdm import tqdm

isSeed = DEMO_CONFIG['useSeed']
if isSeed:
    seed = DEMO_CONFIG['seed']
    random.random_seed(seed)
    np.random.random_seed(seed)

def apply_shift(block, shift_x, shift_y):
    """
    Shift the block by a specific amount in the x and y directions.
    """
    height, width = block.shape[:2]
    shifted_block = np.zeros_like(block)

    for y in range(height):
        for x in range(width):
            new_x = min(max(x + shift_x, 0), width - 1)
            new_y = min(max(y + shift_y, 0), height - 1)
            shifted_block[y, x] = block[new_y, new_x]

    return shifted_block

def create_artifacts_with_directional_copying(frame, block_size, max_shift_value, artifact_percentage, horizontal=True, start_from_top_or_left=True):
    """
    Create artifacts in a single direction by copying content from unmodified areas and applying shifts.
    """
    height, width, _ = frame.shape
    modified_frame = frame.copy()

    # Calculate number of blocks needed based on direction
    blocks_per_row = width // block_size if horizontal else height // block_size
    blocks_per_col = height // block_size if horizontal else width // block_size
    total_blocks = blocks_per_row * blocks_per_col

    # Calculate how many blocks correspond to the specified percentage
    artifact_blocks_count = int(artifact_percentage * total_blocks)

    block_count = 0
    for i in range(blocks_per_col):
        for j in range(blocks_per_row):
            if block_count >= artifact_blocks_count:
                return modified_frame  # Stop if we've reached the desired percentage
            
            # Calculate the top-left corner of the block
            if horizontal:
                y = i * block_size
                x = j * block_size
                if not start_from_top_or_left:
                    y = height - (i + 1) * block_size  # Start from bottom
                if y < 0 or y + block_size > height:
                    continue  # Avoid going out of bounds
            else:
                x = i * block_size
                y = j * block_size
                if not start_from_top_or_left:
                    x = width - (i + 1) * block_size  # Start from right
                if x < 0 or x + block_size > width:
                    continue  # Avoid going out of bounds

            # Define block region from the original frame
            if horizontal:
                # Copy from an unmodified area above or below
                copy_y = max(0, y - block_size) if start_from_top_or_left else min(height - block_size, y + block_size)
                copy_block = frame[copy_y:copy_y + block_size, x:x + block_size]
            else:
                # Copy from an unmodified area to the left or right
                copy_x = max(0, x - block_size) if start_from_top_or_left else min(width - block_size, x + block_size)
                copy_block = frame[y:y + block_size, copy_x:copy_x + block_size]

            # Apply random shifts
            shift_x = np.random.randint(-max_shift_value, max_shift_value + 1)
            shift_y = np.random.randint(-max_shift_value, max_shift_value + 1)

            # Shift the copied block
            shifted_block = apply_shift(copy_block, shift_x, shift_y)

            # Place the shifted block into the modified frame
            modified_frame[y:y + block_size, x:x + block_size] = shifted_block

            block_count += 1

    return modified_frame



def randomize_parameters(base_parameters):
    return {
        'block_size': random.randint(base_parameters['block_size_min'], base_parameters['block_size_max']),
        'max_shift_value': random.randint(base_parameters['max_shift_value_min'], base_parameters['max_shift_value_max']),
        'artifact_percentage': random.uniform(base_parameters['artifact_percentage_min'], base_parameters['artifact_percentage_max']),
        'horizontal': random.choice([True, False]),  # Randomly choose direction
        'start_from_top_or_left': random.choice([True, False])  # Randomly choose starting point
    }

def process_extracted_frames(frames_folder, output_folder, base_parameters, num_variations):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    csv_file_path = os.path.join(DEMO_CONFIG['data'], 'dataset.csv')
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['image_name', 'block_size', 'max_shift_value', 'artifact_percentage', 'horizontal', 'start_from_top_or_left'])

        # Get the list of image files
        image_files = [filename for filename in os.listdir(frames_folder) if filename.endswith('.jpg')]
        for filename in tqdm(image_files, desc="Processing images", unit="image"):
            frame = cv2.imread(os.path.join(frames_folder, filename))
            for _ in tqdm(range(num_variations), desc="Generating variations", leave=False):
                randomized_params = randomize_parameters(base_parameters)
                modified_frame = create_artifacts_with_directional_copying(
                    frame,
                    block_size=randomized_params['block_size'],
                    max_shift_value=randomized_params['max_shift_value'],
                    artifact_percentage=randomized_params['artifact_percentage'],
                    horizontal=randomized_params['horizontal'],
                    start_from_top_or_left=randomized_params['start_from_top_or_left']
                )
                modified_filename = f"{filename}"
                cv2.imwrite(os.path.join(output_folder, modified_filename), modified_frame)

                # Write the randomized parameters to the CSV file
                csv_writer.writerow([
                    modified_filename,
                    randomized_params['block_size'],
                    randomized_params['max_shift_value'],
                    randomized_params['artifact_percentage'],
                    randomized_params['horizontal'],
                    randomized_params['start_from_top_or_left']
                ])
