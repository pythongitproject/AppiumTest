from appium import webdriver

from ADBUtils import Utils
adb = Utils()


if __name__ == '__main__':
    devices_list = adb.getDevices()
    print('可用设备列表:' + str(devices_list))
    device,device_info = adb.getDeviceInfo(devices_list)
    print('device:'+str(device))
    print('device_info:'+str(device_info))
    remote_url = adb.get_remote_url(device)
    print('remote_url:'+remote_url)
    if device and device_info and remote_url:
        print(device_info)
        status = adb.connectDevice(remote_url)
        if status:
            adb.appium_run(device,remote_url,device_info)
        else:
            print('设备连接失败')
    else:
        print('获取设备数据失败')




