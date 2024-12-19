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
import sys

def get_data_key(time_val,token):
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
    # print(f"have {len(i)}")
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





def decode_video_file_in_chunks(input_file, output_file, chunk_size=1024*1024):
    # Step 1: Open the input and output files
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # Read a chunk of the file
            chunk = f_in.read()
            binary_data = decode_string(chunk.decode("utf-8"))


            # Write the decoded chunk to the output file
            f_out.write(binary_data)

def read_m3u8(filename):
    playlist = m3u8.load(filename)
    # Access playlist attributes
    print("Playlist type:", playlist.playlist_type)
    print("Segments:")
    for segment in playlist.segments:
        print("URI:", segment.uri)
        print("Duration:", segment.duration)

total = 0
current = 0

def get_file_extension(url):
    # Regex to match a dot followed by word characters (\w+) at the end of the string ($)
    match = re.search(r'\.\w+$', url)
    if match:
        # Remove the leading dot and return the extension
        return match.group(0)[1:]
    return None


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




text = ""

with open(sys.argv[1],"r") as f:
    text = f.read()

# pattern = r'<script id="__NEXT_DATA__"(.*?)>(.*?)</script>'
pattern = r'<script(.*?) id="__NEXT_DATA__"(.*?)>(.*?)</script>'

# Use re.search to find the match
match = re.search(pattern, text, re.DOTALL)

if match:
    # Extract the JSON content from the match
    json_content = match.group(3).strip()
    decoded = json.loads(json_content)["props"]["pageProps"]

    datetime = decoded["datetime"]
    token = decoded["token"]
    iv = decoded["ivb6"]
    urls = decoded["urls"]

    # print(datetime)
    # print(token)

    json_dec_key = get_data_key(datetime,token)
    # print(json_dec_key)
    # print( len(json_dec_key) )

    one = urls[0]
    quality = one["quality"]
    # print(quality)
    kstr = one["kstr"]
    jstr = one["jstr"]
    output_file = "output.mp4"

    video_dec_key = decrypt_data(kstr,json_dec_key,iv)


    # exit()

    video_dec_key = base64.b64decode(video_dec_key)
    # video_dec_key = video_dec_key.ljust(24, b'\x00')
    # print(video_dec_key)
    # print(len(video_dec_key))


    video_m3u8 = decrypt_data(jstr,json_dec_key,iv)

    playlist = m3u8.loads(video_m3u8)

    if sys.argv[2]:
        segement_size = int( sys.argv[2] )
    else:
        segement_size = 30

    download_m3u8_playlist(playlist, output_file,video_dec_key,".temp/",500,segement_size)

    # print(video_m3u8[0:500])

    # print(decoded)
else:
    print("JSON not found")
