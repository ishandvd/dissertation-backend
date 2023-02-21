import sys
sys.path.append("./models/NMF")
from nmf_main import NmfDrum
from xml_interface import training_files_and_mix


# NmfDrum(["Mix_2.wav", "Hihat_train.wav", "Kick_train.wav", "Snare_Train.wav"], use_custom_training=False)

NmfDrum(["john_bonham_all_my_love.wav"], use_custom_training=False)