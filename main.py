import requests as req 
import os
import tqdm
from Crypto.Cipher import AES   #pip install pycryptodome
from Crypto.Util.Padding import unpad
import base64
import re
import time
import os
import mmap

# requests tqdm pycryptodome

def decrypt_video(file_path, key):

    # key = "4006957"
    with open(file_path, "r+b") as f:
        file_size = os.path.getsize(file_path)
        
        # Determine the length to process (minimum of file size or 28 bytes)
        length = min(file_size, 28)
        
        # Memory-map the file
        with mmap.mmap(f.fileno(), length, access=mmap.ACCESS_WRITE) as mm:
            # Iterate through the mapped file
            for i in range(length):
                # Read a byte
                byte = mm[i]
                
                # Modify the byte
                if i <= len(key) -1:
                    modified_byte = ord(key[i]) ^ byte
                else:
                    modified_byte = byte ^ i
                
                # Write the modified byte back
                mm[i] = modified_byte

def decrypt_url(encrypted_string, key="638udh3829162018"):
    # Split the input string into ciphertext and IV
    split = encrypted_string.split(":")
    if len(split) != 2:
        return None
    # Decode the Base64-encoded IV and ciphertext
    iv = base64.b64decode(split[1])
    encrypted_data = base64.b64decode(split[0])
    
    # Create an AES cipher with the provided key and IV
    cipher = AES.new(key.encode('ISO-8859-1'), AES.MODE_CBC, iv)
    
    # Decrypt the data and unpad the result
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    # Convert the decrypted bytes to a string
    return decrypted_data.decode("utf-8")


authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc0MzEyIiwiZW1haWwiOiJraHVtYXBva2hhcmVsMjA3OEBnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MzI2NDIyNzR9.Wz2iUOpyMzmuo_bi0PV-eu7JgnVVHFXj3PS4SagtmYQ"
host = "https://harkiratapi.classx.co.in"
user_id = "74312"

headers = {
    "Authorization":authorization,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Origin": "https://harkirat.classx.co.in",
    "Host": "harkiratapi.classx.co.in",
    "Sec-Ch-Ua-Platform": "Linux",
    "Referer": "https://harkirat.classx.co.in/",
    "Auth-Key": "appxapi"
}

def get_all_purchases():
    res = req.get(host+f"/get/get_all_purchases?userid={user_id}&item_type=10",headers=headers).json()
    res = res["data"]
    return res

def get_titles(id,pid=-1):
    res = req.get(host+f"/get/folder_contentsv2?course_id={id}&parent_id={pid}",headers=headers).json()
    res = res["data"]
    return res

def get_video_token(cid,vid):
    res = req.get(host+f"/get/fetchVideoDetailsById?course_id={cid}&video_id={vid}&ytflag=0&folder_wise_course=1",headers=headers).json()
    token = res["data"]["video_player_token"]
    # cookie = res["data"]["cookie_value"]
    return token

def get_video_enc_links(cid,vid):
    res = req.get(host+f"/get/fetchVideoDetailsById?course_id={cid}&video_id={vid}&ytflag=0&folder_wise_course=1",headers=headers).json()
    res = res["data"]["encrypted_links"]
    # cookie = res["data"]["cookie_value"]
    return res

def get_video_html(token):

    res = req.get(f"https://player.akamai.net.in/secure-player?token={token}&watermark=").text
    return res

def extract_key(url):
    # Regular expression to match "encrypted-xxxxx"
    match = re.search(r'encrypted-[^/]+', url)
    if match:
        return match.group(0).split("-")[1]  # Return the matched string
    return None


def download_file(url, output_path):
    # Send a GET request to the URL
    response = req.get(url, stream=True)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()
    
    # Get the total file size from the headers
    total_size = int(response.headers.get('content-length', 0))
    
    # Open the output file in binary write mode
    with open(output_path, "wb") as file:
        # Create a progress bar with tqdm
        with tqdm.tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading") as progress_bar:
            # Write the file in chunks
            for chunk in response.iter_content(chunk_size=1024):
                # Filter out keep-alive chunks
                if chunk:
                    file.write(chunk)
                    # Update the progress bar
                    progress_bar.update(len(chunk))


def start():
    courses = get_all_purchases()
    print("\n\n")

    c = 1
    for course in courses:
        name =  course["coursedt"][0]["course_name"]
        # id = course["itemid"]
        print(f"{c}. {name}")
        c = c + 1
    
    choice = input("\n\nEnter the course: ")
    c_title = "courses/"+courses[int(choice)-1]["coursedt"][0]["course_name"]
    cid = courses[int(choice)-1]["itemid"]

    

    os.makedirs(c_title, exist_ok=True)

    titles = get_titles(cid)
    c=1
    if len(titles) !=1:
        for title in titles:
            print(f"{c}. {title['Title']} | {title['material_type']}")
            c = c + 1
    
        choice = input("\n\nEnter the choice: ")
    else:
        choice = "1"

    pid = titles[int(choice)-1]["id"]

    titles = get_titles(cid,pid)


    choice= input("\n\nChoose option: \n1. Download links only to play in browser\n2. Download videos and decrypt to play in any player\n=>")


    if choice=="2":
        c=1
        for title in titles:
            print(f"{c}. {title['Title']} | {title['material_type']}")
            vid = title["id"]
            c = c + 1
            
            enc_links = get_video_enc_links(cid,vid)

            for enc in enc_links:
                quality = enc["quality"]
                path = decrypt_url(enc["path"])
                if "https" in path:
                    path_n = c_title+"/"+title["Title"]
                    ext = path.rsplit('.', 1)[-1] if '.' in path else "mkv"
                    key =  extract_key(path)
                    
                    file = path_n+"/"+quality+" "+key+" ."+ext
                    # print(file)
                    # print(path)
                    
                    
                    if ext=="zip":
                        print("Ignoring zip file download and decryption for now key is "+key)
                    else:
                        os.makedirs(path_n, exist_ok=True)
                        print("Downloading quality:"+quality)
                        download_file(path,file)
                        print("Decrypting the file with password "+key)
                        decrypt_video(file,key)
                        print("Done decrypting the file\n\n")

                # print(path)


    


    if choice == "1":
        c=1
        for title in titles:
            print(f"{c}. Downloading link of {title['Title']} | {title['material_type']}")
            vid = title["id"]
            c = c + 1
        
            # choice = input("Enter the choice: ")
            # vid = titles[int(choice)-1]["id"]

            vtoken = get_video_token(cid,vid)
            # print(vtoken)
            # print(cookie)

            html = get_video_html(vtoken)
            html = html.replace('src="/','src="https://player.akamai.net.in/')
            html = html.replace('href="/','href="https://player.akamai.net.in/')
            html = html.replace('"quality":"360p","isPremier":','"quality":"720p","isPremier":')

            # print(c_title)
            if "Token Expired" in html:
                print("This one is expired...\n")
                print("Waiting for 30 seconds to prevent rate limiting\n")
                time.sleep(30)
                continue

            with open(c_title+"/"+title["Title"]+".html","w") as e:
                e.write(html)

            print("Waiting for 30 seconds to prevent rate limiting\n")
            time.sleep(30)

            




    


start()