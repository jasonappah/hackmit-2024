from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

# Load the processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image (change the URL to an image path if you're using a local image)
image_path = "images/Laptop.JPG"  # Replace with your image URL or path
image = Image.open(image_path)

# Preprocess the image and prepare for captioning
inputs = processor(images=image, return_tensors="pt")

# Generate a caption
output = model.generate(**inputs)

# Decode and print the caption
caption = processor.decode(output[0], skip_special_tokens=True)
print("Generated Caption:", caption)
