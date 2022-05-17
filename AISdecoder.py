import os
import template

def ais_check(ais_data):
    # 第一步验证字段为 AIS 数据
    # 1. 不能为空字段
    # 2. 开头合法
    # 3. 校验值正确

    if ais_data == '':
        return False
    
    # 分割字段
    data = ais_data.split(',')
    # 获得开头
    data_type = data[0]
    # 验证开头是否合法
    if not(data_type == "!AIVDM" or data_type == "!AIVDO"):
        return False
    # 获得校验值与数据（NMEA 0183 Standard CRC16）
    Checksum = data[-1].split("*")[-1]
    if ais_data[0] == "!":
        s = ais_data[1:ais_data.rfind('*')]
    else:
        s = ais_data[0:ais_data.rfind('*')]
    csc = 0
    for c in s:
        # 按位异或值
        csc = csc ^ ord(c)
    csc = ("%x" % csc).zfill(2).upper()
    # 验证校验值
    if csc == Checksum:
        return True
    else:
        return False

def ais_bits_decode(bits):
    # 解析数据
    # 1. 识别类型
    # 2. 通过协议对应解析数据

    # 识别类型
    ais_type = int(bits[0:6],2)
    data = {}
    print("类型：", ais_type)
    match ais_type:
        case 1 | 2 | 3:
            data = template.decod_1(bits)
        case 4:
            data = template.decod_4(bits)
        case 5:
            data = template.decod_5(bits)
        case 18:
            data = template.decod_18(bits)
        case 19:
            data = template.decod_19(bits)
        case 21:
            data = template.decod_21(bits)
        case 24:
            data = template.decod_24(bits)
        case _:
            data = None
    print(data)
    return data

def ais_decode(file_dir, counter = 0):
    # 解析AIS数据主函数
    # 1. 读取AIS（单行/多行)
    # 2. 校验
    # 3. 解析

    result = {}
    files = os.listdir(file_dir)
    for file in files:
        if file[-4:] != ".txt":
            continue
        ais_filespath = file_dir + '/' + file
        with open(ais_filespath) as f:

            globAisData = ""        # 存储多行的AIS数据

            for line in f.readlines():
                ais_input = line.replace('\n', '')
                # 校验
                if not ais_check(ais_input):
                    continue

                data = ais_input.split(',')

                try:
                    ais_lines = int(data[1])             # AIS消息行数
                    ais_line_num = int(data[2])          # AIS消息行号
                    ais_data = data[5]              # 数据内容
                except:
                    continue
                # 提取出单行/多行的AIS数据
                if ais_lines != 1:
                    if globAisData == '' and ais_line_num > 1:
                        # 缺行，未能获取到数据，比对下一条数据
                        continue
                    elif globAisData != '' and ais_line_num == 1:
                        # 缺行，未能获取完数据，清除全局变量
                        globAisData = ""
                    
                    if ais_lines != ais_line_num:
                        # 读取数据
                        globAisData = globAisData + ais_data
                        continue
                    else:
                        ais_data = globAisData + ais_data
                        globAisData = ""
                        
                print("AIS数据为:", ais_data)
                # 单行数据或多行合并的数据
                ais_bits_data = ""
                # 转二进制
                for i in ais_data:
                    c = ord(i) - 48
                    if c > 40:
                        c = c - 8
                    bits = '{0:b}'.format(c)
                    bits = bits.zfill(6)

                    ais_bits_data = ais_bits_data + bits
                # AIS解析
                result[counter] = ais_bits_decode(ais_bits_data)
                counter += 1
                print("\n")
    return result






# ais_input = "!AIVDM,1,1,,A,E>ldCi?;Pb2a@22`:4@HrGK6P0044b3T6Jde@00003v01P,4*0C"
file_dir = "data"

print(ais_decode(file_dir))