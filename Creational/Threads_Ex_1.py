import os
import requests
from datetime import datetime 
from concurrent.futures import ThreadPoolExecutor

os.makedirs("Test_images",exist_ok=True)

image_urls = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/300/300",
    "https://picsum.photos/400/300",
    "https://picsum.photos/500/300",
]

def download_image(url):

    image_name = url.split("/")[-2] + ".jpg"

    image_path = os.path.join("Test_images",image_name)

    response = requests.get(url)
    
    print(f"Response For Image {image_name} is",response)

    with open(image_path,"wb") as f:

        f.write(response.content)

    print(f"Downloaded Image {image_name}")

    return image_path

st = datetime.now()

for image in image_urls:

    download_image(image)
    # pass

et = datetime.now()

ms = (et-st).total_seconds() * 1000

print(f"Total Time Took For Sequential Processing is {ms:.2f}")


#================================== Threadead Execution ====================
st = datetime.now()

def download_all_images():

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = list(executor.map(download_image,image_urls))

        return results

image_files = download_all_images()

et = datetime.now()

ms = (et-st).total_seconds() * 1000

print(f"Total Time Took For Processing using Threads is {ms:.2f}")



