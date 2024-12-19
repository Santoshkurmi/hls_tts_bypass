
# Video Downloading bug report

This is a report generated from testing the website https://harkiratapi.classx.co.in and its dependency domain.


- Bug: Download encrypted video metadata file to play and share video in any browser locally without downloading and decrypting the actual video file.

You might say there is token expiration after playing it few times. Right?. But I am not talking about this. The expiration of token works to get the html file of the video that has all the video metadata. Once I get that file(html) having all the metadata, there is no need of token, any authorization at all. I can play video by live serving that html file locally saving in the computer.

So the bug is,once I get the video html file where video is playing, then there is no expiration system. By the way, you have to save the video html file locally and then run it locally.  Copying the link from the browser for that video won't work as it will again fetch the video metadata where there is token expiration.


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
 ```
 /get/get_all_purchases?userid={user_id}&item_type=10 
 ```
 in place of user_id place the user_id of the user.

 It returns all courses user has purchased.
 Make sure you add authorization headers token in the request. We get course id from this for all the courses.

 #### parent id
 We need to have access to parent id of the course which you want to see the videos.

 To get the parent id, send this request
 ```
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
 ```
 /get/fetchVideoDetailsById?course_id={cid}&video_id={vid}&ytflag=0&folder_wise_course=1
 ```

 #### Last Step
 After getting all the neccessary details, at last we only need the token id of the above step and send this request to get the video metadata.

 ```
 https://player.akamai.net.in/secure-player?token={token}&watermark=
 ```

 Make sure to not send many request to this endpoint in short interval, it has rate limiting. Once you cross the limit, it will respond with Token Expired. After few hours again everything will work.

To get video html without rate limiting, set the interval to each request to few minutes or longer and leave the script running.

By the way rate limiting here doesnot prevent from downloading all the video html file.Sending request in few minute delay for each video will work.

From my testing, i am able to download all the html file of videos of the course in few minutes.

 This is not the actual domain as video player is handled by other domain. 

 set token in the token part of teh video, leave watermark empty if you dont want watermark in video.

 - It returns html file in which it has script tag having json.
 - The json have *kstr* and *jstr* may be fullform as key string and json string. The jstr has encrypted data for each video quality. I have not found the decryption mechanism but it seem kstr is used as a key to decrypt the jstr.
 

 - But we don't need to decrypt the jstr to get file meta data. I am sure even after decrypting jstr, we will have to again decrypt all teh video segment too present in the decrypted data.

 - The bug is that, once I have this html response having kstr and jstr , i can save it to a file. Modify the relative path with absoulte path of some scripts and css as running in locally the html file, the domain is localhost so.

 - Make sure to replace relative url with absoulte in the html of above otherwise running locally won't work. The browser will show empty white page only.

 - After downloading the html returned by that api call, it can be used to watch video. This file can be shared with other too. No need to login. We dont have to download video, we can use only this html and watch all quality of videos with it.

 - I have python script that perform all this task and save all video html file to access and share later. The html files can be embeded in android or windows app like flutter too for easy access without manually opening each html file in browser or using live server. The files generated are saved in "courses" directory.

 #### Fix of bug1
 This bug can be fixed by expiring the video after few minutes. Once expire, it need to access user token againt to play the video.

 But in the website, once the html file is downloaed, no further validation is taking place, no authorization as well as no token expiration seem to be working.

 After understanding how the video is encrypted and decrypted and played, this html file is not expired.

 The javascript files embeded in the head of the html file will not work if the server has build the javascript again, as the name of the javascript changed. 

 Either download all the javascript locally and link it ,doing this will work all the time.
 or else just update the javascript file seeing the new html.

