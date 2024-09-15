import torch
import librosa
import numpy as np
import soundfile as sf
from scipy.signal import lfilter

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
        # Extract additional information
        self.tempo, self.beats = self.analyze_audio()
        self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        self.harmonic, self.percussive = librosa.effects.hpss(self.y)  # Harmonic-Percussive Source Separation


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
        Generate a kick sound with a more natural decay.

        :param duration: Duration of the kick sound in seconds.
        :param freq: Frequency of the kick sound.
        :return: Generated kick sound array.
        """
        t = np.linspace(0, duration, int(self.sr * duration), False)
        kick = 0.5 * np.sin(2 * np.pi * freq * t)
        kick *= np.exp(-t * 40)  # More realistic decay envelope
        return kick

    def generate_snare(self, duration=0.1):
        """
        Generate a snare sound with a natural decay and noise shaping.

        :param duration: Duration of the snare sound in seconds.
        :return: Generated snare sound array.
        """
        snare = 0.5 * np.random.randn(int(self.sr * duration))
        envelope = np.exp(-np.linspace(0, 1, int(self.sr * duration)) * 12)  # Fast decay
        filtered_snare = lfilter([1], [1, -0.95], snare)  # Simple noise shaping
        return filtered_snare * envelope

    def generate_hihat(self, duration=0.05):
        """
        Generate a hi-hat sound with a sharp, realistic decay.

        :param duration: Duration of the hi-hat sound in seconds.
        :return: Generated hi-hat sound array.
        """
        hihat = 0.3 * np.random.randn(int(self.sr * duration))
        envelope = np.exp(-np.linspace(0, 1, int(self.sr * duration)) * 50)  # Fast decay
        return hihat * envelope

    def generate_piano(self, note, duration=0.5):
        """
        Generate a simple piano sound with natural decay and subtle reverb effect.

        :param note: MIDI note number.
        :param duration: Duration of the piano note in seconds.
        :return: Generated piano note array.
        """
        freq = 440.0 * (2.0 ** ((note - 69) / 12.0))
        t = np.linspace(0, duration, int(self.sr * duration), False)
        piano_note = 0.4 * np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 4)  # Adjusted decay envelope
        reverb = np.convolve(piano_note * envelope, np.random.normal(0, 0.01, 500), mode='same')
        return piano_note * envelope + reverb * 0.1  # Add subtle reverb

    def add_drums(self, beats, beat_strengths):
        """
        Add drum sounds matching the rhythmic complexity of the music.

        :param beats: Array of beat frames.
        :param beat_strengths: Array of beat strengths from the ML model.
        :return: Drum mix array.
        """
        drums = np.zeros_like(self.y)
        extended_strengths = self.extend_beat_strengths(beat_strengths)
        onsets = librosa.onset.onset_detect(y=self.percussive, sr=self.sr, backtrack=True)
        
        # Map rhythmic components to reflect complexity in kick, snare, and hi-hat
        beat_positions = librosa.frames_to_time(beats, sr=self.sr)
        beat_intervals = np.diff(beat_positions)  # Calculate time intervals between beats

        for i, beat_time in enumerate(beat_positions[:-1]):
            # Determine the drum hit placement based on beat intervals and beat strengths
            interval = beat_intervals[i]
            kick_probability = extended_strengths[int(beat_time * self.sr)]  # Higher probability for stronger beats
            snare_probability = (1 - kick_probability) * 0.5  # Adjust snare based on weaker beats
            hihat_probability = extended_strengths[int(beat_time * self.sr)] * 0.3 + 0.7  # Hi-hats fill in around beats

            # Generate kick, snare, and hi-hat
            if kick_probability > 0.6:  # Add kicks on stronger beats
                kick = self.generate_kick(duration=interval) * kick_probability
                kick = self.adjust_dynamics(kick, extended_strengths[int(beat_time * self.sr):int(beat_time * self.sr) + len(kick)])
                if int(beat_time * self.sr) + len(kick) < len(drums):
                    drums[int(beat_time * self.sr):int(beat_time * self.sr) + len(kick)] += kick

            if snare_probability > 0.4:  # Add snares to complement kicks
                snare = self.generate_snare(duration=interval * 0.5) * snare_probability
                snare_time = int((beat_time + interval / 2) * self.sr)  # Place snares halfway through interval
                snare = self.adjust_dynamics(snare, extended_strengths[snare_time:snare_time + len(snare)])
                if snare_time + len(snare) < len(drums):
                    drums[snare_time:snare_time + len(snare)] += snare

            if hihat_probability > 0.5:  # Add hi-hats to fill gaps
                hihat = self.generate_hihat(duration=interval * 0.25) * hihat_probability
                hihat_time = int((beat_time + interval / 4) * self.sr)  # Place hi-hats slightly before snares
                hihat = self.adjust_dynamics(hihat, extended_strengths[hihat_time:hihat_time + len(hihat)])
                if hihat_time + len(hihat) < len(drums):
                    drums[hihat_time:hihat_time + len(hihat)] += hihat

            # Use onsets to add additional fills and accents
            if any(onset for onset in onsets if abs(onset / self.sr - beat_time) < interval / 2):
                # Add fills by doubling hits around onsets
                fill_kick = self.generate_kick(duration=0.1) * 0.8
                fill_snare = self.generate_snare(duration=0.1) * 0.7
                fill_time = int(beat_time * self.sr + interval * self.sr * 0.2)
                if fill_time + len(fill_kick) < len(drums):
                    drums[fill_time:fill_time + len(fill_kick)] += fill_kick
                if fill_time + len(fill_snare) < len(drums):
                    drums[fill_time:fill_time + len(fill_snare)] += fill_snare

        # Normalize drums to prevent clipping and maintain consistent levels
        drums = drums / np.max(np.abs(drums) + 1e-9)  # Avoid division by zero
        return drums





    def add_piano(self, beats, beat_strengths):
        """
        Add piano notes at beat locations with enhanced dynamics and musicality.

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
            
            # Cycle through the notes with random inversions and octave shifts for variation
            note = notes[(i // spacing) % len(notes)]
            if np.random.rand() > 0.5:  # 50% chance to play an octave higher or lower
                note += np.random.choice([-12, 12])  # Octave shift up or down

            piano_note = self.generate_piano(note)

            # Apply random variations to velocity for a more expressive feel
            variability_factor = np.random.uniform(0.8, 1.2)
            adjusted_piano = self.adjust_dynamics(
                piano_note * variability_factor, 
                extended_strengths[max(0, beat_time):max(0, beat_time + len(piano_note))]
            )

            # Slightly adjust timing to avoid robotic feel
            timing_offset = int(self.sr * np.random.uniform(-0.05, 0.05))  # Small timing shift

            # Mix the adjusted piano into the piano track
            start_time = max(0, beat_time + timing_offset)
            end_time = start_time + len(adjusted_piano)
            if end_time < len(piano):
                piano[start_time:end_time] += adjusted_piano

        # Normalize piano to prevent clipping and maintain consistent volume levels
        piano = piano / np.max(np.abs(piano) + 1e-9)  # Avoid division by zero
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
