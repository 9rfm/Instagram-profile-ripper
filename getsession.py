import requests,uuid,random,re,hashlib,string,time,json,os
timestamp = str(int(time.time()))
uu = '83f2000a-4b95-4811-bc8d-0f3539ef07cf'

def run(username, password, proxies=None):
    try:
        def RandomStringChars(n=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(n))
        def RandomString(n=10):
            letters = string.ascii_lowercase + '1234567890'
            return ''.join(random.choice(letters) for i in range(n))
        def randomStringWithChar(stringLength=10):
            letters = string.ascii_lowercase + '1234567890'
            result = ''.join(random.choice(letters) for i in range(stringLength - 1))
            return RandomStringChars(1) + result
        class sessting:
            def generateUSER_AGENT(self):
                Devices_menu = ['HUAWEI', 'Xiaomi', 'samsung', 'OnePlus']
                DPIs = ['480', '320', '640', '515', '120', '160', '240', '800']
                randResolution = random.randrange(2, 9) * 180
                lowerResolution = randResolution - 180
                DEVICE_SETTINTS = {
                    'system': "Android",
                    'Host': "Instagram",
                    'manufacturer': f'{random.choice(Devices_menu)}',
                    'model': f'{random.choice(Devices_menu)}-{randomStringWithChar(4).upper()}',
                    'android_version': random.randint(18, 25),
                    'android_release': f'{random.randint(1, 7)}.{random.randint(0, 7)}',
                    "cpu": f"{RandomStringChars(2)}{random.randrange(1000, 9999)}",
                    'resolution': f'{randResolution}x{lowerResolution}',
                    'randomL': f"{RandomString(6)}",
                    'dpi': f"{random.choice(DPIs)}"
                }
                return '{Host} 155.0.0.37.107 {system} ({android_version}/{android_release}; {dpi}dpi; {resolution}; {manufacturer}; {model}; {cpu}; {randomL}; en_US)'.format(**DEVICE_SETTINTS)
            def generate_DeviceId(self , ID):
                volatile_ID = "12345"
                m = hashlib.md5()
                m.update(ID.encode('utf-8') + volatile_ID.encode('utf-8'))
                return 'android-' + m.hexdigest()[:16]
        s = sessting()
        device_id = s.generate_DeviceId(username)
        headers = {'User-Agent': s.generateUSER_AGENT(),'Host': 'i.instagram.com','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','accept-encoding': 'gzip, deflate','x-fb-http-engine': 'Liger','Connection': 'close'}
        data = {'guid': uu,'enc_password': f"#PWD_INSTAGRAM:0:{timestamp}:{password}",'username': username,'device_id': device_id,'login_attempt_count': '0'}
        req = requests.post("https://i.instagram.com/api/v1/accounts/login/", headers=headers, data=data, proxies=proxies)
        if "logged_in_user" in req.text:
            coo = req.cookies
            sessionid = coo.get("sessionid")
            return True, f"Logged in @{username}\nSession: {sessionid}"
        elif 'checkpoint_challenge_required' in req.text:
            return False, "Checkpoint required"
        else:
            try:
                regx_error = re.search(r'"message":"(.*?)",', req.text).group(1)
                return False, regx_error
            except:
                return False, req.text
    except Exception as e:
        return False, str(e)

username = input("your_username")
password = input("your_password")
result = run(username, password)
print(result[1])