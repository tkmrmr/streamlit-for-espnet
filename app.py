import streamlit as st
import soundfile as sf
from espnet2.bin.tts_inference import Text2Speech
from num import *

def main():
    st.markdown("<h1 style='text-align: center;'>Speech Synthesis (Yumi)</h1>", unsafe_allow_html=True)
    # screen_name = st.text_input("Input your name")
    # if screen_name:
    txt = st.text_input('Input the words you want her to say')
    speed = st.slider(label='Speed',
                      min_value=0.5,
                      max_value=2.0,
                      value=1.0,
                      )
    if st.button('Generate') or txt != "":
        if txt == "":
            st.warning("Input words")
        else:
            nl = "{:0>3d}".format(n)
            text2speech = Text2Speech(
                train_config="yumi/config.yaml",
                model_file="yumi/100epoch.pth",
                speed_control_alpha=1.0/speed,
                noise_scale=0.333,
                noise_scale_dur=0.333,
            )
            wav = text2speech(txt)["wav"]
            sf.write("yumi/output/out"+nl+".wav", wav.numpy(), text2speech.fs, "PCM_16")
            # st.write("save out"+nl+".wav")
            st.audio("yumi/output/out"+nl+".wav")
            with open("yumi/output/out"+nl+".wav", "rb") as file:
                st.download_button(
                    label="Download audio",
                    data=file,
                    file_name="audio.wav"
            )
            with open("yumi/lines.txt", "a") as f:
                f.write(nl+": "+txt+"\n")
            with open("yumi/num.py", "r") as f:
                data  = f.read()
            data = data.replace(f"n = {n}",  f"n = {n+1}")
            with open("yumi/num.py", mode="w", encoding="cp932") as f:
                f.write(data)

if __name__ == "__main__":
    main()
