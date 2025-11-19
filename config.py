import math
import random
import time
import hashlib
api_url="https://api3.hilife.sg/hilife_v3/smarthome/device/list"
payload = {"hilifeUnit": "Tri-Zen Residencies2Block4608Unit"}
clientId = "mVQg6kJDgp"
 
clientSecret = "P7CUuui05fYj3YvIlwnurwo9Op12";
#unixEpochTime = math.floor(datetime.timestamp(datetime.now()) / 1000);
unixEpochTime = int(time.time()*1000)
min = 100000
max = 999999
Nonce = math.floor(random.random() * (max - min + 1)) + min

 

concatStr = clientId + clientSecret + str(unixEpochTime) + str(Nonce)


SignCode = hashlib.md5(concatStr.encode("utf-8")).hexdigest()

header= {
        "Content-Type": "application/json",
        "Client-Id": clientId,
        "Time": str(int(unixEpochTime)),
        "Nonce": str(Nonce),
        "Sign":SignCode
    }
