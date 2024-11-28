
# Video Downloading bug report

This is a report generated from testing the website https://harkiratapi.classx.co.in and its dependency domain.

 in the github, html_old folder contains html file of video for course Complete Web development + Devops Cohort to test for it. You can also run the script to perform downloading of html and video using both bug.

## Bug lists
- Bug1: Download encrypted video metadata file to play and share video in any browser locally without downloading and decrypting the actual video file.

- Bug2: Download the video file and decrypt it too which is accessible to the android app (*100xdevs*) upto 720p resoultion . Currently zip file can be downloaded but not able to decrypt.

## Bug1 reproduction:
 To download video metadata html, first we need access to following things
 - course id
 - parent id
 - video id
 - token of video id



 #### Course Id

host = "https://harkiratapi.classx.co.in"

header should be like this similar
```json
{
    "Authorization":authorization,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Origin": "https://harkirat.classx.co.in",
    "Host": "harkiratapi.classx.co.in",
    "Sec-Ch-Ua-Platform": "Linux",
    "Referer": "https://harkirat.classx.co.in/",
    "Auth-Key": "appxapi"
}

```

 Send this get request in the api endpoint
 ```json
 /get/get_all_purchases?userid={user_id}&item_type=10 
 ```
 in place of user_id place the user_id of the user.

 It returns all courses user has purchased.
 Make sure you add authorization headers token in the request. We get course id from this for all the courses.

 #### parent id
 We need to have access to parent id of the course which you want to see the videos.

 To get the parent id, send this request
 ```json
 /get/folder_contentsv2?course_id={course_id}&parent_id=-1
 ```
 here, place course_id and parent_id to -1.
 It will return list of parent mainly single one. We just need the id of teh response parents.

 #### video ids
 Send the same request as above of parent id, insted of parent_id=-1, replace with the actual parent id found above.

 It will return all the videos with its id of that course.

 #### token for video
 Token is required for each video id to access the video.
 
 Send this request to get token id. Also for second bug, it provides link to download video too up to 720p
 ```json
 /get/fetchVideoDetailsById?course_id={cid}&video_id={vid}&ytflag=0&folder_wise_course=1
 ```

 #### Last Step
 After getting all the neccessary details, at last we only need the token id of the above step and send this request to get the video metadata.

 ```
 https://player.akamai.net.in/secure-player?token={token}&watermark=
 ```

 Make sure to not send many request to this endpoint in short interval, it has rate limiting. Once you cross the limit, it will respond with Token Expired. After few hours again everything will work.

To get video html without rate limiting, set the interval to each request to more than 1 minute or so.

By the way rate limiting here doesnot prevent from downloading all the video html file.Sending request in few minute delay for each video will work.

From my testing, i am able to download all the html file of videos of the course in few minutes.

 This is not the actual domain as video player is handled by other domain. 

 set token in the token part of teh video, leave watermark empty if you dont want watermark in video.

 - It returns html file in which it has script tag having json.
 - The json have *kstr* and *jstr* may be fullform as key string and json string. The jstr has encrypted data for each video quality. I have not found the decryption mechanism but it seem kstr is used as a key to decrypt the jstr.
 

 But we don't need to decrypt the jstr to get file meta data. I am sure even after decrypting jstr, we will have to again decrypt all teh video segment too present in the decrypted data.

 The bug is that, once I have this html response having kstr and jstr , i can save it to a file. Modify the relative path with absoulte path of some scripts and css as running in locally the html file, the domain is localhost so.

 - Make sure to replace relative url with absoulte in the he tml of above otherwise running locally won't work. The browser will show empty white page only.

 After downloading the html returned by that api call, it can be used to watch video. This file can be shared with other too. No need to login. We dont have to download video, we can use only this html and watch all quality of videos with it.

 I have python script that perform all this task and save all video html file to access and share later. The html files can be embeded in android or windows app like flutter too for easy access without manually opening each html file in browser or using live server. The files generated are saved in "courses" directory.

 #### Fix of bug1
 This bug can be fixed by expiring the video after few minutes. Once expire, it need to access user token againt to play the video.

 But in the website, once the html file is downloaed, no further validation is taking place, no authorization as well as no token expiration seem to be working.

 I dont know how long the html file is valid, but in my observation ,it been 2 days still all the html files are playing well in any browser without login or anyting.


## Bug 2:
In this bug, the video can be downloaded and decrypted too.
For now, I am not able to decrypt zip file as it contains m3u8 with encrypted tse. I am sure with enough testing, the step to decrypt zip file video too will also be found.

- We need to send this request to get encrypted links of video that can be downloaded.

 
 Send this request to get encypted_links for each quality up to 720p. We don't need video token returned by it as the token is used in first bug to play in browser.

 ```json
 /get/fetchVideoDetailsById?course_id={cid}&video_id={vid}&ytflag=0&folder_wise_course=1
 ```

 It returns encrypted links for each quality up to 720p, having path,key.

 - path is the encypted link to download the file
 - key is the key to decrypt the video

 #### Decryption of path and key
 Both path and key are encypted too. To decrypt it we have to use AES decryption algorith which is illustrated using python code below
 ```python
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

 ```
 "638udh3829162018" this is the key used to encrypt the link and path.By the way this key is used to decrypt the key of the response.

 I mean video is encryped by key and that key is again encypted by another key which is 638udh3829162018

 This return the decrypted path as well as key passing in the function.

 The key need to be decoded againt to base64 which get converted into few digit number only.

 Now we have decrypted path and actual key to decrypt the video.

 The algorith uses XOR operation on the video with the key above in the first 28 bit of the video. I think it is encrypting only the meta data file of the video so that other player won't recognize the video. This also make the encyption and decryption faster.

 ```python

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

 ```
 This read the file using mmap to load file in memory to do the xor operation with the key. Algorithm is preety simple to understand from the code. Applying the same algorith again encrypt it. This is the power of xor algorithm encryption.

 This is used to decrypt .mkv,.mp4 or other video format link but not .zip as .zip file contains m3u8 and tse file.

 This feature too is implemented in the python script. Running the python main.py , it will shows all the courses purchased by the user, choice to download html using bug1 method or video using bug2.


 Make sure set token and user_id variable of the script and install neccessary module.

 zip file link  are encrypted using AES-128 using key, to get key, we have to send request to endpoint with the URI present in the m3u8. But it seem the key is not working.

 ```json 
 url = "https://harkiratapi.akamai.net.in/post/generate_key_session"

data = {"url":"https://appx-transcoded-videos-mcdn.akamai.net.in/videos/harkirat-data/164118-1732615576/encrypted-1e52ca/720p.zip",
"is_ios":"0",
"ck_placer":"1732618042-728703"}

 ```
 ck_placer is URI of the m3u8 file after extracting .zip file. 

 

 
