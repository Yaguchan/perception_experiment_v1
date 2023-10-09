import os
import numpy as np
import soundfile as sf


# Set parameters
sample_rate = 48000
wav_len = 1
fadein = 0.01
fadeout = 0.01

OUTDIR = ''
NAME = 'wav'
A = 400
B = 500


def generate_sine_wave(frequency, duration, fade_in, fade_out, sample_rate):
    total_samples = int(sample_rate * duration)
    fade_in_samples = int(sample_rate * fade_in)
    fade_out_samples = int(sample_rate * fade_out)

    t = np.linspace(0, duration, total_samples, endpoint=False)
    fade_in_curve = np.linspace(0.0, 1.0, fade_in_samples, endpoint=False)
    fade_out_curve = np.linspace(1.0, 0.0, fade_out_samples, endpoint=False)

    # Generate sine wave
    wave = np.sin(2 * np.pi * frequency * t)

    # Apply fade-in and fade-out curves
    wave[:fade_in_samples] *= fade_in_curve
    wave[-fade_out_samples:] *= fade_out_curve

    return wave


def generate_silence(duration, sample_rate):
    total_samples = int(sample_rate * duration)
    return np.zeros(total_samples)


def make_and_save_wav(first, last, save_path):
    # Generate waves
    wave_1 = generate_silence(0.5, sample_rate)
    wave_2 = generate_sine_wave(A, wav_len, fadein, fadeout, sample_rate)
    wave_3 = generate_silence(first*0.001, sample_rate)
    wave_4 = generate_sine_wave(B, wav_len, fadein, fadeout, sample_rate)
    wave_5 = generate_silence(first*0.001, sample_rate)
    wave_6 = generate_sine_wave(A, wav_len, fadein, fadeout, sample_rate)
    wave_7 = generate_silence(first*0.001, sample_rate)
    wave_8 = generate_sine_wave(B, wav_len, fadein, fadeout, sample_rate)
    wave_9 = generate_silence(last*0.001, sample_rate)
    wave_10 = generate_sine_wave(A, wav_len, fadein, fadeout, sample_rate)
    wave_11 = generate_silence(0.5, sample_rate)
    # Concatenate waves
    final_wave = np.concatenate((wave_1, wave_2, wave_3, wave_4, wave_5, wave_6, wave_7, wave_8, wave_9, wave_10, wave_11))
    # Save to WAV file
    sf.write(save_path, final_wave, sample_rate, subtype="PCM_16")


def main():
    
    dir_path = os.path.join(OUTDIR, NAME)
    
    os.makedirs(dir_path, exist_ok=True)
    
    first = [100, 200, 400, 800, 1600]
    second = [[50, 59, 71, 84, 119, 141, 168, 200], [113, 130, 150, 173, 231, 266, 307, 354], [261, 291, 323, 360, 445, 495, 550, 612], \
              [615, 657, 702, 749, 854, 912, 974, 1040], [1231, 1314, 1403, 1498, 1708, 1824, 1948, 2080]]
    
    for i in range(len(first)):
        for s in second[i]:
            wav_path = os.path.join(dir_path, f'{first[i]}_{s}.wav')
            make_and_save_wav(first[i], s, wav_path)
    

if __name__ == '__main__':
    main()
