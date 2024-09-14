from transformers import BlipProcessor, BlipForConditionalGeneration, GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image


class ImagePrompt:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.processor = None
        self.model = None
        self.inputs = None

    def _generate_model(self):
        # Load BLIP model and processor
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.inputs = self.processor(images=self.image, return_tensors="pt")

    def _generate_output(self):
        # Generate caption from BLIP model
        self._generate_model()
        output = self.model.generate(**self.inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption

    def generate_music_prompt(self):
        # Generate initial caption and refine it for music
        caption = self._generate_output()
        return caption

    def __str__(self):
        # Print refined music prompt when the object is printed
        return self.generate_music_prompt()


image_prompt = ImagePrompt("images/Hack_MIT_Crowd.jpg")
print(image_prompt)
