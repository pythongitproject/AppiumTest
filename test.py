from appium import webdriver
import requests, json, os
# url = 'http://10.100.99.203:7100/api/v1/devices'
# post_url = 'http://10.100.99.203:7100/api/v1/user/devices'
url = 'http://192.168.21.128:7100/api/v1/devices'
post_url = 'http://192.168.21.128:7100/api/v1/user/devices'
token = '81d985e57c20457f8e980757666a3218b1b5b481afcf454086dc5b4c26003494'
headers = {
    'Authorization': 'Bearer ' + token
}
post_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token

}
def getDevices():
    try:
        print('获取stf设备...')
        result = requests.get(url, headers=headers)
        print('getDevices: ' + result.text)
        s = json.loads(result.text)
        listDevices = []
        devices = s["devices"]
        num = 0
        for device in devices:
            if device["present"] and not device["using"]:
                listDevices.append(device["serial"])
                num = num + 1
        if num == 0:
            return None
        else:
            return listDevices[0]
    except:
        print('获取stf设备失败')
        return None


def getDeviceinfo(device):
    uri = url + '/' + device
    result = requests.get(uri, headers=headers)
    info = json.loads(result.text)
    if info:
        print('getDeviceinfo:' + str(info))
        return info
    else:
        return None

def connectDevice(device):
    data = {"serial": device}
    data = json.dumps(data)
    result = requests.post(post_url, data=data, headers=post_headers)
    s = json.loads(result.text)
    print(s)
    if s["success"]:
        uri = post_url + '/' + device + '/remoteConnect'
        remote = requests.post(uri, headers=post_headers)
        print('remote:' + str(remote.text))
        remoteConnectUrl = json.loads(remote.text)
        return remoteConnectUrl["remoteConnectUrl"]
    else:
        print(device + '设备连接失败')
        return None
    return deviceName

list = getDevices()
print(1)
if list:
    info  = getDeviceinfo(list)
    print(2)
    deviceName = connectDevice(list)
    if deviceName:
        print(3)
        print(deviceName)
        print('http://'+deviceName)
        platformVersion = info["device"]["version"]

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = platformVersion
        desired_caps['deviceName'] = deviceName
        desired_caps['app'] = r'C:\Users\linweili\Desktop\AppiumTest\bili.apk'
        desired_caps['noReset'] = False
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        print(4.0)
        wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        print(4)
        wd.switch_to.alert.accept()
        print(5)
        wd.implicitly_wait(60)
        wd.quit()
    else:
        print('设备连接失败')
else:
    print('没有获取到设备')
