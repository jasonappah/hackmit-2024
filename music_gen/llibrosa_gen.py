import torch
import librosa
import numpy as np
import soundfile as sf

class MusicEnhancer:
    def __init__(self, audio_path, model_path):
        """
        Initialize the MusicEnhancer class.

        :param audio_path: Path to the audio file without drums.
        :param model_path: Path to the pre-trained ML model.
        """
        self.audio_path = audio_path
        self.model_path = model_path
        self.y, self.sr = librosa.load(audio_path, sr=None)
        self.model = self.load_model()

    def load_model(self):
        """
        Load the pre-trained model.

        :return: Loaded PyTorch model.
        """
        model = torch.jit.load(self.model_path)
        model.eval()
        return model

    def analyze_audio(self):
        """
        Analyze the audio to detect tempo and beats.

        :return: Detected tempo and beat frames.
        """
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        print(f"Detected tempo: {tempo} BPM")
        return tempo, beats

    def extract_rhythmic_features(self):
        """
        Apply the ML model to extract rhythmic features from the audio.

        :return: Array of beat strengths.
        """
        audio_tensor = torch.tensor(self.y, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            beat_strengths = self.model(audio_tensor).squeeze(0).squeeze(0).numpy()

        # Ensure beat_strengths covers the entire track by padding if necessary
        if len(beat_strengths) < len(self.y):
            beat_strengths = np.pad(beat_strengths, (0, len(self.y) - len(beat_strengths)), 'constant')
        
        return beat_strengths

    def extend_beat_strengths(self, beat_strengths):
        """
        Extend beat strengths to cover the entire audio track length.

        :param beat_strengths: Original beat strengths array.
        :return: Extended beat strengths array matching the length of the audio.
        """
        extended_strengths = np.interp(np.arange(len(self.y)), 
                                       np.linspace(0, len(self.y), len(beat_strengths)), 
                                       beat_strengths)
        return extended_strengths

    def adjust_dynamics(self, signal, strengths):
        """
        Scale the signal by the beat strengths.

        :param signal: The audio signal (e.g., drums, piano).
        :param strengths: Beat strengths array.
        :return: Adjusted signal.
        """
        strengths_interp = np.interp(np.arange(len(signal)), np.linspace(0, len(signal), len(strengths)), strengths)
        return signal * strengths_interp

    def generate_kick(self, duration=0.1, freq=50):
        """
        Generate a kick sound.

        :param duration: Duration of the kick sound in seconds.
        :param freq: Frequency of the kick sound.
        :return: Generated kick sound array.
        """
        t = np.linspace(0, duration, int(self.sr * duration), False)
        kick = 0.5 * np.sin(2 * np.pi * freq * t)
        kick *= np.exp(-t * 30)  # Decay envelope
        return kick

    def generate_snare(self, duration=0.1):
        """
        Generate a snare sound.

        :param duration: Duration of the snare sound in seconds.
        :return: Generated snare sound array.
        """
        snare = 0.5 * np.random.randn(int(self.sr * duration))
        envelope = np.exp(-np.linspace(0, 1, int(self.sr * duration)) * 10)  # Fast decay
        return snare * envelope

    def generate_hihat(self, duration=0.05):
        """
        Generate a hi-hat sound.

        :param duration: Duration of the hi-hat sound in seconds.
        :return: Generated hi-hat sound array.
        """
        hihat = 0.3 * np.random.randn(int(self.sr * duration))
        envelope = np.exp(-np.linspace(0, 1, int(self.sr * duration)) * 30)  # Fast decay
        return hihat * envelope

    def generate_piano(self, note, duration=0.5):
        """
        Generate a simple piano sound using sine waves for a specified note.

        :param note: MIDI note number.
        :param duration: Duration of the piano note in seconds.
        :return: Generated piano note array.
        """
        freq = 440.0 * (2.0 ** ((note - 69) / 12.0))
        t = np.linspace(0, duration, int(self.sr * duration), False)
        piano_note = 0.4 * np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 3)  # Decay envelope to make it sound like a piano
        return piano_note * envelope

    def add_drums(self, beats, beat_strengths):
        """
        Add drum sounds at beat locations and ensure continuous presence.

        :param beats: Array of beat frames.
        :param beat_strengths: Array of beat strengths from the ML model.
        :return: Drum mix array.
        """
        drums = np.zeros_like(self.y)
        extended_strengths = self.extend_beat_strengths(beat_strengths)
        
        # Determine spacing of drum hits to ensure consistent presence
        spacing = int(self.sr * 0.5)  # Place a drum hit every 0.5 seconds

        for i in range(0, len(self.y), spacing):
            beat_time = i
            kick = self.generate_kick()
            snare = self.generate_snare()
            hihat = self.generate_hihat()

            adjusted_kick = self.adjust_dynamics(kick, extended_strengths[max(0, beat_time):max(0, beat_time + len(kick))])
            adjusted_snare = self.adjust_dynamics(snare, extended_strengths[max(0, beat_time):max(0, beat_time + len(snare))])
            adjusted_hihat = self.adjust_dynamics(hihat, extended_strengths[max(0, beat_time):max(0, beat_time + len(hihat))])

            # Mix the adjusted drums into the drum track
            if beat_time + len(adjusted_kick) < len(drums):
                drums[beat_time:beat_time + len(adjusted_kick)] += adjusted_kick
            if beat_time % 4 == 0 and beat_time + len(adjusted_snare) < len(drums):
                drums[beat_time:beat_time + len(adjusted_snare)] += adjusted_snare
            if beat_time + len(adjusted_hihat) < len(drums):
                drums[beat_time:beat_time + len(adjusted_hihat)] += adjusted_hihat

        # Normalize drums to prevent clipping
        drums = drums / np.max(np.abs(drums))
        return drums

    def add_piano(self, beats, beat_strengths):
        """
        Add piano notes at beat locations and ensure continuous presence.

        :param beats: Array of beat frames.
        :param beat_strengths: Array of beat strengths from the ML model.
        :return: Piano mix array.
        """
        piano = np.zeros_like(self.y)
        notes = [60, 64, 67]  # C Major chord: C, E, G
        extended_strengths = self.extend_beat_strengths(beat_strengths)
        
        # Determine spacing of piano hits to ensure consistent presence
        spacing = int(self.sr * 1)  # Place a piano hit every 1 second

        for i in range(0, len(self.y), spacing):
            beat_time = i
            note = notes[(i // spacing) % len(notes)]  # Cycle through the notes
            piano_note = self.generate_piano(note)

            adjusted_piano = self.adjust_dynamics(piano_note, extended_strengths[max(0, beat_time):max(0, beat_time + len(piano_note))])

            # Mix the adjusted piano into the piano track
            if beat_time + len(adjusted_piano) < len(piano):
                piano[beat_time:beat_time + len(adjusted_piano)] += adjusted_piano

        # Normalize piano to prevent clipping
        piano = piano / np.max(np.abs(piano))
        return piano

    def normalize(self, signal):
        """
        Normalize the audio signal to prevent clipping.

        :param signal: Audio signal to be normalized.
        :return: Normalized audio signal.
        """
        max_val = np.max(np.abs(signal))
        return signal / max_val if max_val > 0 else signal

    def save_output(self, output_audio, output_path='output_with_drums_and_piano.wav'):
        """
        Save the output audio file.

        :param output_audio: The mixed audio array with drums and piano.
        :param output_path: Path to save the output file.
        """
        sf.write(output_path, output_audio, self.sr)
        print(f"Drums and piano added and saved to {output_path}")

    def process(self):
        """
        Main process to analyze audio, generate drums and piano, and mix them.
        """
        tempo, beats = self.analyze_audio()
        beat_strengths = self.extract_rhythmic_features()
        drums = self.add_drums(beats, beat_strengths)
        piano = self.add_piano(beats, beat_strengths)

        # Normalize and adjust dynamics for a balanced mix
        drums = self.normalize(drums)
        piano = self.normalize(piano)
        
        # Combine the original audio with drums and piano
        output_audio = self.y + drums + piano
        output_audio = self.normalize(output_audio)  # Final normalization to prevent clipping
        
        self.save_output(output_audio)

# Create an instance of MusicEnhancer
audio_path = 'separated_files/htdemucs/Dancing Through the Night/no_drums.wav'
model_path = 'music_gen/gen_model/musicnet.ts'  # Replace with the actual model path

music_enhancer = MusicEnhancer(audio_path, model_path)
music_enhancer.process()
