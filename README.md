# Swiss Alexa: Embedded Linux Project at OST

Welcome to the GitHub repository of the "Swiss Alexa" project. This project was a collaboration effort during the Embedded Linux Seminar at Fachhochschule Ostschweiz (OST) in Buchs.

## Overview

Swiss Alexa is a voice-activated music player that understands commands in Swiss German. Once you make a song request in Swiss German, Swiss Alexa will transcribe your request to German, search for the song on YouTube, and stream the audio through a Bluetooth speaker.

## Hardware Setup
- **Raspberry Pi 4**
- **USB Microphone**
- **128x64 Monochrome OLED Display**
- **Joystick Button**
- **3 LEDs (Red, Green, Blue)**
- **Bluetooth Speaker**

## Features
1. **Swiss German Voice Recognition**: Speak in Swiss German, and Swiss Alexa will understand you using the fHNW API.
2. **Feature Extraction with Chatbots**: Harnessing the power of [Huggingface](https://huggingface.co/chat) and [ChatGptX](https://chatgptx.de/) for text processing.
3. **Music Streaming**: The system finds music tracks on YouTube Music via Yahoo and streams them.
4. **Interactive OLED Display**: Get visual feedback and song details on the OLED display.
5. **LED Feedback**: LEDs provide feedback about the status (searching, playing, etc.).
6. **Simple Controls**: Control playback with a single press of the joystick button.

## How to Use
1. Ensure that all the hardware components are correctly connected.
2. Power on the Raspberry Pi 4.
3. Press the joystick button.
4. Make a song request in Swiss German (either by artist name, song title, or both).
5. The system will search and play the song via the Bluetooth speaker.
6. To stop playback, press the joystick button again.

## Software Stack
- **Voice Recognition**: The API from Fachhochschule Nordwestschweiz (fHNW) transcribes Swiss German voice commands to German. [API Link](https://stt4sg.fhnw.ch/)
- **Feature Extraction**: A web scraper extracts data using both [Huggingface](https://huggingface.co/chat) and [ChatGptX](https://chatgptx.de/).
- **Music Search**: The system uses Yahoo filtered for `site:music.youtube.com` to search for music, and then processes the URL with `yt-dlp`.
- **Audio Playback**: Using the `mpv` media player on Linux to stream only the audio from YouTube Music tracks.


## Contributors
- [Florian Baumgartner](https://github.com/FlorianBaumgartner)
- [Matthias Höfflin](https://github.com/Matthias-Hoefflin)


## Acknowledgements
We'd like to thank the Fachhochschule Ostschweiz (OST) and all the professors and participants of the Embedded Linux Seminar for their continuous support. Special thanks to Fachhochschule Nordwestschweiz (FHNW) for providing the Swiss German transcription API.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


Happy Listening with Swiss Alexa! 🎵🇨🇭