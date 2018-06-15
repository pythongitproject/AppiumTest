#/usr/bin/env python3
#coding=utf-8
import requests, json, subprocess

class Utils():
    def __init__(self):
        self.url = 'http://10.100.99.203:7100/api/v1/devices'
        self.post_url = 'http://10.100.99.203:7100/api/v1/user/devices'
        self.token = '7ab6ffd9254a48c787b9d483a755acf82fa005f416934eed95cd470a8932e1de'
        # url = 'http://192.168.21.128:7100/api/v1/devices'
        # self.post_url = 'http://192.168.21.128:7100/api/v1/user/devices'
        # self.token = '81d985e57c20457f8e980757666a3218b1b5b481afcf454086dc5b4c26003494'
        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }
        self.post_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token

        }
        self.appium_url = 'http://10.100.99.151:4723/wd/hub'

    #获取stf设备列表
    def getDevices(self):
        try:
            print('获取stf设备...')
            result = requests.get(self.url, headers=self.headers)
            print('Devices: ' + result.text)
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
                return listDevices
        except:
            print('获取stf设备列表失败')
            return None

    # 获取单个可用设备的详细信息
    def getDeviceInfo(self,serial):
        global remote_device
        if serial:
            for device in serial:
                uri = self.url + '/' + device
                result = requests.get(uri, headers=self.headers)
                info = json.loads(result.text)
                print('info:'+str(info))
                if info['success']:
                    remote_device = device
                    break
            return remote_device,info
        else:
            return None,None

    #获取设备远程连接url
    def get_remote_url(self,device):
        data = {"serial": device}
        data = json.dumps(data)
        result = requests.post(self.post_url, data=data, headers=self.post_headers)
        s = json.loads(result.text)
        print(s)
        try:
            if s["success"]:
                uri = self.post_url + '/' + device + '/remoteConnect'
                remote = requests.post(uri, headers=self.post_headers)
                print('remote:' + str(remote.text))
                remoteConnectUrl = json.loads(remote.text)
                if remoteConnectUrl:
                    return remoteConnectUrl['remoteConnectUrl']
                else:
                    return None
        except:
            return None

    #连接设备
    def connectDevice(self,remote_url):
        status = self.adb_connect(remote_url)
        if status:
            return True
        else:
            return False


    #adb连接
    def adb_connect(self,remote_url):
        cmd = 'adb devices'
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.readlines())
        cmd = 'adb devices'
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.readlines())
        cmd = 'adb connect %s' % remote_url
        print(cmd)
        result = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.readlines())
        cmd = 'adb connect %s' % remote_url
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.readlines())
        cmd = 'adb devices'
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.readlines())
        if result:
            return result
        else:
            return False

    # 断开设备
    def deleteDevice(self,serial):
        uri = self.post_url + '/' + serial
        result = requests.delete(uri, headers=self.headers)
        result = json.loads(result.text)
        if result["success"] is True:
            print(serial + '设备断开连接成功')
        else:
            print(serial + '设备断开连接失败')

    #appium
    def appium_run(self,device,remote_url,device_info):
        if device_info and device and remote_url:
            desired_caps = {}
            desired_caps['platformName'] = device_info['device']['platform']
            desired_caps['platformVersion'] = device_info['device']['version']
            desired_caps['deviceName'] = remote_url
            desired_caps['app'] = 'E:\\PycharmProjects\\AppiumTest\\bili.apk'
            desired_caps['noReset'] = False
            desired_caps["unicodeKeyboard"] = "True"
            desired_caps["resetKeyboard"] = "True"
            print(4.0)
            from appium import webdriver
            try:
                wd = webdriver.Remote(self.appium_url, desired_caps)
                # wd.switch_to.alert.accept()
                print(5)
                wd.implicitly_wait(60)
                wd.quit()
                self.deleteDevice(device)
            except:
                self.deleteDevice(device)
        else:
            self.deleteDevice(device)
            print('数据异常')
