import requests as req 
import os
import tqdm
from Crypto.Cipher import AES   #pip install pycryptodome
from Crypto.Util.Padding import unpad
import base64
import re
import time
import os
import base64
import hashlib
from base64 import b64decode
from Crypto.Cipher import AES
import m3u8
import requests
import os
import threading
import re
import json
import mmap
import sys


user_id = "74312"
authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc0MzEyIiwiZW1haWwiOiJraHVtYXBva2hhcmVsMjA3OEBnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MzI2NDIyNzR9.Wz2iUOpyMzmuo_bi0PV-eu7JgnVVHFXj3PS4SagtmYQ"

host = "https://harkiratapi.classx.co.in"




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

def watch_video(cid,vid):
    headers2 = {
    "Authorization":authorization,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Origin": "https://harkirat.classx.co.in",
    "Host": "harkiratapi.classx.co.in",
    "Sec-Ch-Ua-Platform": "Linux",
    "Referer": "https://harkirat.classx.co.in/",
    "Auth-Key": "appxapi"
}
    headers2["content-type"]="application/x-www-form-urlencoded"
    data = f"user_id={user_id}&course_id={cid}&live_course_id={vid}&ytFlag=0&folder_wise_course=1"
    try:
        res = req.post(host+f"/post/watch_videov2",data=data,headers=headers2).json()
        # print(res)
    except Exception as e:
        print(e)


# for downloading video in real one

def get_data_enc_key(time_val,token):
    # Extract parts of the string
    n = time_val[-4:]  # Last 4 characters of time_val
    r = int(n[0])  # First character of n as an integer
    i = int(n[1:3])  # Next two characters of n as an integer
    o = int(n[3])  # Last character of n as an integer
    
    # Create the new string
    a = time_val + token[r:i]
    
    # Create SHA-256 hash
    s = hashlib.sha256()
    s.update(a.encode('utf-8'))
    c = s.digest()
    
    # Determine the sign based on the value of o
    if o == 6:
        sign = c[:16]  # First 16 bytes
    elif o == 7:
        sign = c[:24]  # First 24 bytes
    else:
        sign = c  # Entire hash

    key = base64.b64encode(sign).decode('utf-8')
    # Log values for debugging (optional)
    
    return key


def decrypt_data(data,key,ivb):
    i = b64decode(key)  # Key
    o = b64decode(ivb)  # Initialization Vector (IV)
    a = b64decode(data)  # Encrypted data
    
    # Create AES Cipher object
    cipher = AES.new(i, AES.MODE_CBC, o)
    
    # Decrypt the data
    l = cipher.decrypt(a)
    
    # Remove padding (PKCS7) if necessary
    # padding_length = l[-1]
    # if padding_length < 16:  # PKCS7 padding uses byte value equal to padding length
    #     l = l[:-padding_length]
    
    # Convert decrypted data to a UTF-8 string
    dec = l.decode('utf-8')

    # Return the decrypted string
    return dec


def decode_video_tsa(input_string):
    shift_value = 0xa * 0x2  # 3 in decimal
    result = ''
    
    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        xor_result = char_code -shift_value  # Perform XOR with the constant
        result += chr(xor_result)  # Convert back to a character and append to the result
        
    binary_data = base64.b64decode(result)

    return binary_data


def decode_video_tsb(input_string):
    xor_value = 0x3  # 42 in decimal
    shift_value = 0x2a  # 3 in decimal
    result = ''
    
    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        xor_result = char_code >> xor_value  # Perform XOR with the constant
        shifted_result = xor_result ^ shift_value  # Right shift the result by 3
        result += chr(shifted_result)  # Convert back to a character and append to the result
        
    binary_data = base64.b64decode(result)

    return binary_data

def decode_video_tsc(input_string):
    shift_value = 0xa  # 3 in decimal
    result = ''
    
    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        xor_result = char_code - shift_value  # Perform XOR with the constant
        result += chr(xor_result)  # Convert back to a character and append to the result
        
    binary_data = base64.b64decode(result)

    return binary_data

def decode_video_tsd(input_string):
    shift_value = 0x2  # 3 in decimal
    result = ''
    
    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        # xor_result = char_code ^ shift_value  # Perform XOR with the constant
        shifted_result = char_code >> shift_value  # Right shift the result by 3
        result += chr(shifted_result)  # Convert back to a character and append to the result
        
    binary_data = base64.b64decode(result)

    return binary_data


def decode_video_tse(input_string):
    xor_value = 0x3  # 42 in decimal
    shift_value = 0x2a  # 3 in decimal
    result = ''
    
    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        xor_result = char_code ^ shift_value  # Perform XOR with the constant
        shifted_result = xor_result >> xor_value  # Right shift the result by 3
        result += chr(shifted_result)  # Convert back to a character and append to the result
        
    binary_data = base64.b64decode(result)

    return binary_data

def get_file_extension(url):
    # Regex to match a dot followed by word characters (\w+) at the end of the string ($)
    match = re.search(r'\.\w+$', url)
    if match:
        # Remove the leading dot and return the extension
        return match.group(0)[1:]
    return None



total = 0
current = 0

def download_and_decrypt_segment(segment_url, key=None, iv=None, output_path=None,bit=7):
    # Download the segment
    global current

    if os.path.exists(output_path):
        current = current  + 1
        print(f"Downloaded and decrypted segments: {current}/{total}",end="\r")
        return

    
    attempt = 0
    segment_data = None
    while attempt <=5:
        try:
            response = requests.get(segment_url, stream=True,timeout=15)
            response.raise_for_status()
            segment_data = response.content
            break
        except requests.exceptions.Timeout:
            attempt = attempt + 1
        except Exception as e:
            attempt = attempt + 1
    if not segment_data:
        return

    ext = get_file_extension(segment_url)
    if ext =="tsa":
        segment_data = decode_video_tsa(segment_data.decode("utf-8"))
    elif ext == "tsb":
        segment_data = decode_video_tsb(segment_data.decode("utf-8"))
    elif ext == "tsc":
        segment_data = decode_video_tsc(segment_data.decode("utf-8"))
    elif ext == "tsd":
        segment_data = decode_video_tsd(segment_data.decode("utf-8"))
    elif ext == "tse":
        segment_data = decode_video_tse(segment_data.decode("utf-8"))

    

    # Decrypt the segment if a key is provided
    cipher = AES.new(key, AES.MODE_CBC, iv)
    segment_data = cipher.decrypt(segment_data)

    # Save the segment to a file
    with open(output_path+".bak", "wb") as f:
        f.write(segment_data)
    os.rename(output_path+".bak",output_path)
    current = current  + 1
    print(f"Downloaded and decrypted: {current}/{total}",end="\r")

def download_m3u8_playlist(playlist, output_file,key,directory,max_thread=1,max_segment=0):
    # Load the m3u8 playlist
    
    os.makedirs(directory, exist_ok=True)
    print(f"Downloading video with max segment {max_segment} "+output_file)
    # print("Downloading video "+output_file)
    if not playlist.segments:
        raise ValueError("No segments found in the playlist")

    # Download and decrypt segments
    segment_files = []
    global total,current 
    current = 0
    total = len(playlist.segments)
    for i in range(0,len(playlist.segments),max_thread):
        threads = []
        batch = playlist.segments[i:i + max_thread]

        for j, segment in enumerate(batch):
            # print(i+j)
            # print(max_segment)
            if not max_segment == 0 and max_segment < i+j:
                break

            segment_url = segment.uri
            segment_file = f"segment_{i+j}.ts"
            segment_files.append(segment_file)

            


            # print(segment.key.method)
            # exit()
            # Get the AES key and IV if encrypted
            iv = None
            if segment.key:
                if segment.key.method == "AES-128":
                    key_url = segment.key.uri
                    iv = bytes.fromhex(segment.key.iv[2:]) if segment.key.iv else None

            thread = threading.Thread(target=download_and_decrypt_segment,args=(segment_url, key, iv, directory+segment_file))
            # download_and_decrypt_segment(segment_url, key, iv, directory+segment_file)
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()
    # Combine segments into a single file
    if current != len(segment_files):
        print("All files are not downloaded")
        exit()
    with open(output_file+".bak", "wb") as output:
        for segment_file in segment_files:
            with open(directory+segment_file, "rb") as segment:
                output.write(segment.read())
            os.remove(directory+segment_file)  # Clean up segment file
    os.rename(output_file+".bak",output_file)

    print(f"Video saved as {output_file}")


def handle_download_start(html,isFile=False,output_file="",max_thread=1,max_segment=0):
                pattern = r'<script(.*?) id="__NEXT_DATA__"(.*?)>(.*?)</script>'
                if isFile:
                    with open(html,"r") as f:
                        html = f.read()

                match = re.search(pattern, html, re.DOTALL)

                if match:
                    # Extract the JSON content from the match
                    json_content = match.group(3).strip()
                    decoded = json.loads(json_content)["props"]["pageProps"]

                    datetime = decoded["datetime"]
                    bit = datetime[-1]
                    token = decoded["token"]
                    iv = decoded["ivb6"]
                    urls = decoded["urls"]

            
                    data_dec_key = get_data_enc_key(datetime,token)

                    one = urls[0]
                    quality = one["quality"]
                    # print(quality)
                    kstr = one["kstr"]
                    jstr = one["jstr"]

                    output_file = output_file +" "+quality+".mp4"
                    if os.path.exists(output_file):
                        print(f"This video {output_file} is already downloaded")
                        return

                    video_dec_key = decrypt_data(kstr,data_dec_key,iv)
                    # print(video_dec_key)
                    video_dec_key = base64.b64decode(video_dec_key)

                    # video_dec_key = video_dec_key.ljust(24, b'\x00')
                    # print( len(video_dec_key))
                    # exit()
                    video_m3u8 = decrypt_data(jstr,data_dec_key,iv)


                    playlist = m3u8.loads(video_m3u8)

                    download_m3u8_playlist(playlist, output_file,video_dec_key,".temp/",max_thread,max_segment)

                    # print(video_m3u8)


# end of this 


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
    
        choice = input("\nEnter the choice: ")
    else:
        choice = "1"

    pid = titles[int(choice)-1]["id"]

    titles = get_titles(cid,pid)


    choice= input("Choose Download options: \n1. Links only\n2. Download Links and Videos both\n=>")

    


    if True:

        if sys.argv[1]:
            segement_size = int( sys.argv[1] )
        else:
            segement_size = 40

        if sys.argv[2]:
            thread_size = int( sys.argv[2] )
        else:
            thread_size = 50
        c=1
        for title in titles:
            print(f"\n{c}. Downloading link of '{title['Title']} | {title['material_type']}'")
            vid = title["id"]
            if title['material_type'] !="VIDEO":
                print("Ignoring this file as it is not video")
                continue
            c = c + 1

            if os.path.exists(c_title+"/"+title["Title"]+".html"):
                print("Already downloaded link for "+"'"+title["Title"]+"'\n")
                handle_download_start(c_title+"/"+title["Title"]+".html",True,c_title+"/"+title["Title"],thread_size,segement_size)
                continue

            # exit()
        
            # choice = input("Enter the choice: ")
            # vid = titles[int(choice)-1]["id"]

            vtoken = get_video_token(cid,vid)
            watch_video(cid,vid)
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

            if choice=="2":
                handle_download_start(html,False,c_title+"/"+title["Title"],thread_size,segement_size)

            print("Waiting for 30 seconds to prevent rate limiting\n")
            time.sleep(30)


start()