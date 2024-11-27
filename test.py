
# Example usage
encrypted_string = "tE+QIdJCmpRtsniTXxxuMgutc2rRTYnU+QXUswv79TRmGMCRL9sbQ9kT7MoymSRfG8EjcccztiTSooU1bJrdX0WO2zotrcitbgPePexipAYTcafHY4ErX6qwGX5xmHUnfLD/ibYe64JoaipBkMDMxlXo8+rafRGjgxMv3RyFyEo=:ZmVkY2JhOTg3NjU0MzIxMA=="
key = "638udh3829162018"



try:
    decrypted_text = decrypt_string(encrypted_string, key)
    print("Decrypted text:", decrypted_text)
except Exception as e:
    print("Error during decryption:", str(e))


import re

def extract_key(url):
    # Regular expression to match "encrypted-xxxxx"
    match = re.search(r'encrypted-[^/]+', url)
    if match:
        return match.group(0).split("-")[1]  # Return the matched string
    return None

# Example usage
url = "https://appx-transcoded-videos-mcdn.akamai.net.in/videos/harkirat-data/163848-1732615575/encrypted-592dbf/240p.zip"
key = extract_key(url)
print(f"Extracted key: {key}")
