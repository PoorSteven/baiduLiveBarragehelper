import wmi
import hashlib
import random
c = wmi.WMI()

# # # 硬盘序列号
# for physical_disk in c.Win32_DiskDrive():
#     print(physical_disk.SerialNumber)

# CPU序列号
for cpu in c.Win32_Processor():
    print(cpu.ProcessorId.strip())

# 主板序列号
for board_id in c.Win32_BaseBoard():
    print(board_id.SerialNumber)

# mac地址
# for mac in c.Win32_NetworkAdapter():
    # print(mac.MACAddress)

# bios序列号
for bios_id in c.Win32_BIOS():
    print(bios_id.SerialNumber.strip())

def get_str_sha1_secret_str(res:str):
    
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(res.encode('utf-8'))
    encrypts = sha.hexdigest()
    print(encrypts)
    return encrypts

def ran_tag_str(num):
    # 随机变量
    suiji = 'abcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        i = random.choice(suiji)
        salt += i
    return salt

mac_address = get_str_sha1_secret_str(ran_tag_str(32))

with open('C:/Windows/mac.ini','w',encoding='utf-8')as f:
    f.write(mac_address)
    f.close()

