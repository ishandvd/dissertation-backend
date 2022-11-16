import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np



y, sr = librosa.load('ladder.wav', sr=None)


S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)


plt.figure()
S_dB = librosa.power_to_db(S, ref=np.max)
print(S_dB.shape)
# librosa.display.specshow(S_dB)
# plt.colorbar()
# plt.show()
# plt.savefig("ladder.png")