# 🌟 YT to Shots: Snag Your Space! 🚀

## What's This Magic? ✨

Hey there, space cadet! 🌌 Welcome to `yt_to_shots.py`, your new best buddy for grabbing breathtaking space visuals straight from YouTube and turning your PC into a cosmic wonder. This Python script is all about downloading those stellar YouTube videos, extracting frames like a pro photographer, ditching the deja-vu frames, and if you wish, saying "bye-bye" to the video after snagging its best shots. Whether it's for creating an out-of-this-world wallpaper collection or fueling your galactic projects, we've got you covered!

## Features That Are Outta This World! 🌠

- **Download YouTube Videos** with just a URL or VideoID. 📥
- **Extract Frames** like you're jumping through space-time! Set your own intervals to capture the cosmos. 📸
- **Remove Similar Frames** because who needs duplicates in a universe of infinite variety? 🔄
- **Optional Video Deletion** because, after the magic, who needs the spellbook? 🚮
- **Arabic Title Support** 'cause we love and respect the universal language of stars, including Arabic. 🌍➡🌌

## Before You Launch 🚀

Make sure your spaceship is equipped with the following:

- Python 3.6 or newer (the language of our space guild) 🐍
- [pytube](https://pytube.io/en/latest/user/install.html) for those YouTube voyages 🎥
- [OpenCV](https://opencv.org/) for our image deciphering tools 🔍
- [tqdm](https://tqdm.github.io/) for watching the stars go by as we work 📊
- [scikit-image](https://scikit-image.org/) for spotting cosmic twins 🌒🌓
- [langdetect](https://pypi.org/project/langdetect/), because the universe speaks in mysterious ways 🗣️
- [arabic-reshaper](https://pypi.org/project/arabic-reshaper/) & [python-bidi](https://pypi.org/project/python-bidi/) for when the stars align in Arabic ✨

Hop on the terminal and run:

```sh
pip install yt-dlp pytube opencv tqdm scikit-image langdetect arabic-reshaper python-bidi
```

## Let's Get This Party Started! 🎉

Ready to grab those cosmic visuals? Here's how:

```sh
python yt_to_shots.py -u <URL/VideoID> [options]
```

### Cosmic Commands 🌙

- `-u`, `--url` : The YouTube video URL or VideoID. Where your journey begins! 🚀
- `-o`, `--output`: Where to store your interstellar captures. Defaults to your current starbase (folder). 📁
- `-f`, `--frame`: How many frames to skip in your cosmic leap. More skips = faster travel! 🛸
- `-m`, `--max`: Your cargo limit. How many frames to keep before you say "that's enough beauty for today". 📦
- `-d`, `--delete`: Wanna erase the traces of your journey? Toggle this on! 🧹
- `-s`, `--similar`: Set your tolerance for cosmic similarities. Sometimes, one moon is just enough! 🌖
- `-t`, `--txt`: Enter the path of the text file containing the list of URLs or VideoIDs. 📄
- `-q`, `--fetch`:  Enter the search query to fetch videos from YouTube
- `-mr`,`--maxResults`: Enter the maxResults of the search query. Default is 50.
- `-l`, `--login`: Login to YouTube using API KEY usage python bulk_fetcher.py -l YOUR_KEY

### Example Commands

```sh
python yt_to_shots.py -u "https://www.youtube.com/watch?v=CfjNMLgax2s" -o "GalaxyPics" -f 100 -m 500 -d 
python yt_to_shots.py -u "ImTqvWxc2Fo" --delete 
python yt_to_shots.py -u "uD4izuDMUQA" -f 20 -m 500 -d 

```

## It's a Wrap! 🌈

There you have it, space ranger! Everything you need to fill your digital universe with wonders. Let `yt_to_shots.py` be your telescope to the cosmos, and who knows what breathtaking views you'll discover for your PC's backdrop? 🌠

**Happy Exploring!** 🌟
