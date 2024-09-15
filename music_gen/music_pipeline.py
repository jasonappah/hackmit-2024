import torch
import librosa
import soundfile as sf

# Load the TorchScript model
model_path = 'music_gen/gen_model/musicnet.ts'
model = torch.jit.load(model_path)
model.eval()  # Set the model to evaluation mode

# Load your audio file with Librosa
audio_path = 'music_gen/mp3/Dancing Through the Night.mp3'
audio, sample_rate = librosa.load(audio_path, sr=None, mono=True)  # Load as mono audio

# Convert the audio to a PyTorch tensor
audio_tensor = torch.tensor(audio).unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions

# Normalize audio if required (optional based on model requirements)
audio_tensor = audio_tensor / torch.max(torch.abs(audio_tensor))

# Run the model on the audio
with torch.no_grad():
    output = model(audio_tensor)

# Convert the output tensor to a NumPy array
output_audio = output.squeeze(0).squeeze(0).numpy()  # Remove batch and channel dimensions

# Save the output audio
sf.write('output_audio.wav', output_audio, sample_rate)

print("Audio processed and saved as 'output_audio.wav'.")
