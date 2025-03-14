from pyspark.sql import SparkSession
from pyspark.ml.image import ImageSchema
from pyspark.sql.functions import lit
from pyspark import SparkConf, SparkContext
# Create a Spark session
spark = SparkSession.builder \
    .appName("Image Classification") \
    .config("spark.driver.memory", "5g") \
    .config("spark.executor.memory", "5g") \
    .getOrCreate()




# Load images from a directory
#image_df = spark.read.format("image").load("/home/noob/Desktop/code/trainModel/")#dataset4/extracted_frames")

#trying different method
image_df_0 = spark.read.format("image").load("/home/noob/Desktop/code/trainModel/dataset*/extracted_frames/").limit(100)
image_df_0 = image_df_0.withColumn("label", lit(0))
#image_df_0 = image_df_0.limit(1000)

image_df_1 = spark.read.format("image").load("/home/noob/Desktop/code/trainModel/dataset*/modified_frames/").limit(100)
image_df_1 = image_df_1.withColumn("label", lit(1))
#image_df_1 = image_df_1.limit(1000)


image_df = image_df_0.union(image_df_1)

# add labels in the image_df dataframe, hopefully as a column.

# Show the DataFrame schema
image_df.printSchema()

#image_df.show(truncate=False)
image_count = image_df.count()
print(f"Number of images loaded: {image_count}")
print({image_df.select("label").distinct().show()})

import torch
import torchvision.transforms as transforms
from torchvision import models
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType

# Load the pre-trained Inception V3 model
model = models.inception_v3(pretrained=True)

#model.eval()  # Set the model to evaluation mode

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((126, 224)),  # Resize to (height, width)
    transforms.RandomHorizontalFlip(),
    transforms.RandomApply([
        transforms.RandomRotation(degrees=(90, 90))  # Rotate 90 degrees clockwise
    ], p=0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.3983, 0.3922, 0.3554], std=[0.1866, 0.1815, 0.1775])
])

# Define a UDF to extract features

count = 0
def extract_features(image_data):
    # Convert the image data to a PIL image
    count += 1
    image = ImageSchema.toPILImage(image_data)
    # Apply the transformations
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Perform inference
    with torch.no_grad():
        features = model(image)
    
    # Return the features as a list
    return features.flatten().tolist()
# Register the UDF
extract_features_udf = udf(extract_features, ArrayType(FloatType())) 
#print(count)
# Apply the UDF to extract features
feature_df = image_df.withColumn("features", extract_features_udf(image_df["image"]))
#feature_df.printSchema()

#STUCK HERE

labels = feature_df.select("label").rdd.flatMap(lambda x: x).take(100)  # Replace 'label_column' with your actual label column name
features = feature_df.select("features").rdd.flatMap(lambda x: x).take(100)#.collect().tak

# # Convert to tensors (if using PyTorch)
# features_tensor = torch.tensor(features)
# labels_tensor = torch.tensor(labels)


