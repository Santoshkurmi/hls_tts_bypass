import requests as req 


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
    cookie = res["data"]["cookie_value"]
    return [token,cookie]

def get_video_html(token,cookie):
    headers2 = {
    # "Authorization":authorization,

}
    res = req.get(f"https://player.akamai.net.in/secure-player?token={token}&watermark=",headers=headers2).text
    return res

def start():
    courses = get_all_purchases()

    c = 1
    for course in courses:
        name =  course["coursedt"][0]["course_name"]
        # id = course["itemid"]
        print(f"{c}. {name}")
        c = c + 1
    
    choice = input("Enter the course: ")
    cid = courses[int(choice)-1]["itemid"]


    titles = get_titles(cid)
    c=1
    for title in titles:
        print(f"{c}. {title['Title']} | {title['material_type']}")
        c = c + 1
    
    choice = input("Enter the choice: ")
    pid = titles[int(choice)-1]["id"]


    titles = get_titles(cid,pid)
    c=1
    for title in titles:
        print(f"{c}. {title['Title']} | {title['material_type']}")
        vid = title["id"]
        c = c + 1
    
        # choice = input("Enter the choice: ")
        # vid = titles[int(choice)-1]["id"]

        vtoken,cookie = get_video_token(cid,vid)
        # print(vtoken)
        # print(cookie)

        html = get_video_html(vtoken,cookie)
        html = html.replace('src="/','src="https://player.akamai.net.in/')
        html = html.replace('href="/','href="https://player.akamai.net.in/')
        html = html.replace('"quality":"360p","isPremier":','"quality":"720p","isPremier":')

        
        
        with open(vid+".html","w") as e:
            e.write(html)




    


start()