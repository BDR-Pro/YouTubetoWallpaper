import argparse
import os
import cv2
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim
from langdetect import detect_langs
import arabic_reshaper
from bidi.algorithm import get_display
from random import randint
import uuid
import yt_dlp
from bulk_fetcher import main as fetcher

def download_video_and_get_title(url, output_path='videos/video.mp4'):
    """
    Download a video using yt-dlp and return its title.

    Parameters:
    - url (str): The URL of the video to download.
    - output_path (str): The output path where the video will be saved.

    Returns:
    - str: The title of the video.
    """

    # Configuration for yt-dlp
    ydl_opts = {
        'format': 'best',  # Download the best quality
        'outtmpl': output_path,  # Set the output path
        # Other options can be added here
    }

    # Create a YoutubeDL instance with the specified options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract information from the URL, but don't download the video
        info_dict = ydl.extract_info(url, download=False)
        # Retrieve the video title
        video_title = info_dict.get('title', 'Unknown Title')

        # If you also want to download the video uncomment the next line
        # ydl.download([url])

    return fix_title(video_title)


def fix_title(title):
    """
    Fix the title of a video by reshaping it and converting it to displayable characters and 
    readable if it is arabic.

    Parameters:
    - title (str): The title of the video.

    Returns:
    - str: The fixed title of the video.
    """

    # Detect the language of the title
    lang = detect_langs(title)[0].lang

    # If the language is Arabic, reshape and convert the title
    if lang == 'ar':
        title = arabic_reshaper.reshape(title)
        title = get_display(title)

    return title.translate(str.maketrans('', '', '\\:/*?"<>|.'))

def print_help():
    print('''
Usage:
    python yt_to_shots.py <arguments>

Arguments:
    -u, --url     Enter the URL/VideoID of the YouTube video.
    -o, --output  Enter the output folder path to save the images in it. Default is the current folder.
    -f, --frame   Enter the number of frames to skip each capture. Default is 50.
    -m, --max     Enter the maximum number of frames to capture. Default is 1000.
    -d, --delete  Delete the downloaded video after processing.
    -s, --similar Enter the similarty percentage of frames to remove. Default is 50.
    -t, --txt     Enter the path of the text file containing the list of URLs 
    -q, --fetch,  Enter the search query to fetch videos from YouTube 
    -mr,--maxResults Enter the maxResults of the search query.
    -l, --login Login to YouTube using API KEY usage > -l YOUR_KEY


Examples:
    python yt_to_shots.py -u "QSNa8U1yGrM" -s 50 -f 500 -m 100 
    python yt_to_shots.py -u "https://www.youtube.com/watch?v=F5NN9h22ifU" -o "Screenshots" -f 100 -m 500 -d
    python yt_to_shots.py -u "ImTqvWxc2Fo" --delete
    python yt_to_shots.py -u "uD4izuDMUQA"  -f 20 -m 500 -d
    python yt_to_shots.py -u "fW4cLkdPoCs" -s 30 -f 200 -m 500 -d
    python yt_to_shots.py -u "QSNa8U1yGrM" -s 50 -f 500 -m 100

''')

def download_youtube_video(video_url):
    if "https://www.youtube.com/watch?v=" not in video_url:
        video_url = f"https://www.youtube.com/watch?v={video_url}"
    
    print(f"Downloading YouTube video ..")
    title = download_video_and_get_title(video_url)
    print(f"Download complete of {title}.")
    path = os.mv("videos/video.mp4", f"videos/{title}.mp4")
    print(f"Downloaded video path: {path}")
    return (path, title)

def get_images(video_path, output_folder, frame_skip, title):
    print(f"Extracting frames from video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    images = []
    
    folder = os.path.join(output_folder, f"{title}_frames")  # Use os.path.join for compatibility

    os.makedirs(folder, exist_ok=True)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in the video: {num_frames}")
    i = 0  # Start from first frame
    pbar = tqdm(total=min(num_frames, frame_skip * 1000), desc="Extracting Frames", unit="frame")
    while True:
        success, frame = cap.read()
        if not success or i >= 1000 * frame_skip:  # Limit to max_frames to prevent infinite loop
            break
        if i % frame_skip == 0:  # Only save frames based on the skip interval
            unique_id = str(uuid.uuid4())
            file_ = os.path.join(folder, f"frame_{i//frame_skip:04d}_{unique_id[:5]}.jpg")
            images.append(file_)
            cv2.imwrite(file_, frame)
        i += 1
        pbar.update(1)
    cap.release()
    pbar.close()
    return images

def remove_similar_images(images_tuple, similarity_percentage):
    images = list(images_tuple)
    print("Removing similar images...")
    for i in tqdm(range(len(images)-1), desc="Comparing Images"):  # Adjusted for accurate progress reporting
        for j in range(i+1, len(images)):  # Start comparison from the next image
            if compare_images(images[i], images[j], similarity_percentage):
                os.remove(images[j])
                images.pop(j)  # Use pop to remove by index
                break  # Exit the inner loop once a match is found and removed

def remove_extra_images(max_frames, output_folder, title):
    folder = os.path.join(output_folder, f"{title}_frames")
    images = os.listdir(folder)
    removed_count = 0
    while removed_count < len(images) - max_frames:  # Ensure only excess images are removed
        rand_index = randint(0, len(images)-1)
        os.remove(os.path.join(folder, images[rand_index]))
        images.pop(rand_index)  # Remove the deleted file from the list
        removed_count += 1
    print(f"Removed {removed_count} extra images.") if removed_count else print("No extra images removed.")
    return len(images)  # Return the updated count of files in the folder


def compare_images(image1, image2, SP):
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    similarity_index = ssim(image1_gray, image2_gray)
    similarity_percentage = (similarity_index + 1) / 2 * 100
    return similarity_percentage >= SP


def download_one_video(args):
    print(f"Processing video: {args.url}")
    path, title = download_youtube_video(args.url)
    images = get_images(path, args.output, args.frame, title)
    remove_similar_images(tuple(images), args.similar)
    folder_length = remove_extra_images(args.max, args.output, title)
    
    if args.delete:
        os.remove(path)
        print("Downloaded video deleted.")
    
    print(f"Downloaded {folder_length} images from the video {title}.")
    
def download_multiple_videos(args):
    file_path=args.txt if args.txt else f"search_results/{args.fetch}.txt"
    with open(file_path, "r") as file:
        urls = file.readlines()
    for url in urls:
        args.url = url.strip()
        download_one_video(args)
        
def main(args):
    if args.url:
        download_one_video(args)
        
    elif args.txt:
        download_multiple_videos(args)
        
    elif args.fetch:
        print(f"Bulk fetching videos for query: {args.fetch} with maxResults: {args.maxResults}")
        fetcher(args.fetch, args.maxResults)
        download_multiple_videos(args)
        
    elif args.login:
        print("Login to YouTu`be using API KEY")
        with open(".env", "w") as file:
            file.write(f"API_KEY={args.login}")
        print("Login successful")
        
        
    else:
        print_help()
        
        

if __name__ == "__main__":
    print_help()
    parser = argparse.ArgumentParser(description="Download YouTube videos")
    parser.add_argument("-u", "--url", help="Enter the URL/VideoID of the YouTube video")
    parser.add_argument("-t","--txt" , help="Enter the path of the text file containing the list of URLs" )
    parser.add_argument("-q","--fetch", help="Enter the search query to fetch videos from YouTube")
    parser.add_argument("-mr","--maxResults", help="Enter the maxResults of the search query" , type=int)
    parser.add_argument("-o", "--output", help="Enter the output folder path to save the images in it. Default is the current folder.", default=os.getcwd())
    parser.add_argument("-f", "--frame", help="Enter the number of frames to skip each capture. Default is 50.", type=int, default=50)
    parser.add_argument("-m", "--max", help="Enter the maximum number of frames to capture. Default is 1000.", type=int, default=1000)
    parser.add_argument("-s", "--similar", help="Enter the similarity percentage of frames to remove. Default is 50.", type=int, default=50)
    parser.add_argument("-d", "--delete", help="Delete Downloaded video", action='store_true')
    parser.add_argument("-l","--login",help="Login to YouTube using API KEY" , action='store_true')

    args = parser.parse_args()
    main(args)

