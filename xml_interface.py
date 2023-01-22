from xml.dom import minidom

filename = "C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/WaveDrum02_03#MIX.xml"



def drum_file(drum, t):
    drum_file_name = [x.firstChild.data for x in t
    if drum in x.firstChild.data]

    return drum_file_name[0] if len(drum_file_name) > 0 else ""

def onsets(drum, events_list):
    onsets = [float(event.getElementsByTagName("onsetSec")[0].firstChild.data) 
            for event in events_list if 
            event.getElementsByTagName("instrument")[0].firstChild.data == drum]

    return onsets

f = minidom.parse(filename)
mix = f.getElementsByTagName("audioFileName")[0]
print("Audio File Name: ", mix.firstChild.data)
training = f.getElementsByTagName("audioTrainingFileName")

(hh, sd, kd) = (drum_file("#HH#", training), 
                drum_file("#sD#", training), 
                drum_file("#KD#", training))

events = f.getElementsByTagName("event")

(hh_onsets, sd_onsets, kd_onsets) = (onsets("HH", events),
                                    onsets("SD", events),
                                    onsets("KD", events))

