from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


class ImagePrompt:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
    
    def _generate_model(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.inputs = self.processor(images=self.image, return_tensors="pt")

    def _generate_output(self):
        self._generate_model()
        output = self.model.generate(**self.inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption
    
    def __str__(self):
        return self._generate_output()


prompt = ImagePrompt("images/Laptop.JPG")
print(prompt)


