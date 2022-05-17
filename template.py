# 二进制有符号整型
def sign_int(bits):
    if bits[0] == '1':
        # 负数 反码-补码
        bits=bits.replace('1','2')
        bits=bits.replace('0','1')
        bits=bits.replace('2','0')
        return -(int(bits,2)+1)
    else:
        return int(bits, 2)

# ascii解码
def decod_str(bits):
    data = ""
    for k in range(len(bits)//6):
        letter = int(bits[6*k:6*(k+1)],2)
        if letter < 32:
            letter+=64
        letter = chr(letter)
        if letter != '@':
            data += letter
    return data.rstrip()

# 第一类: type=1, 2, 3 位置报告
def decod_1(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['转发指示符']      = int(data[6:8],2)
    ais_data['MMSI']            = int(data[8:38],2)
    ais_data['导航状态']        = int(data[38:42],2)
    ais_data['旋转速率']        = sign_int(data[42:50])
    ais_data['SOG']             = int(data[50:60], 2)
    ais_data['位置准确度']      = data[60]
    ais_data['经度']            = sign_int(data[61:89]) / 600000.0
    ais_data['纬度']            = sign_int(data[89:116]) / 600000.0
    ais_data['COG']             = int(data[116:128],2) * 0.1
    ais_data['实际航向']        = int(data[128:137],2)
    ais_data['时戳']            = int(data[137:143],2)
    ais_data['特定操作指示符']  = int(data[143:145],2)
    ais_data['RAIM标志']        = data[148]
    ais_data['通信状态']        = int(data[149:168], 2)
    return ais_data

# 第二类: type=4 基站报告
def decod_4(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['转发指示符']      = int(data[6:8],2)
    ais_data['MMSI']            = int(data[8:38],2)
    ais_data['UTC年']           = int(data[38:52], 2)
    ais_data['UTC月']           = int(data[52:56], 2)
    ais_data['UTC日']           = int(data[56:61], 2)
    ais_data['UTC时']           = int(data[61:66], 2)
    ais_data['UTC分']           = int(data[66:72], 2)
    ais_data['UTC秒']           = int(data[72:78], 2)
    ais_data['位置准确度']      = data[78]
    ais_data['经度']            = sign_int(data[79:107]) / 600000.0
    ais_data['纬度']            = sign_int(data[107:134]) / 600000.0
    ais_data['定位装置类型']    = int(data[134:138], 2)
    ais_data['RAIM标志']        = data[148]
    ais_data['通信状态']        = int(data[149:168], 2)
    return ais_data

# 第三类: type=5 静态和航行相关数据
def decod_5(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['转发指示符']      = int(data[6:8],2)
    ais_data['MMSI']            = int(data[8:38],2)
    ais_data['AIS版本']         = int(data[38:40],2)
    ais_data['IMO编号']         = int(data[40:70],2)
    ais_data['呼号']            = decod_str(data[70:112])
    ais_data['名称']            = decod_str(data[112:232])
    ais_data['船舶和货物类型']  = int(data[232:240],2)
    ais_data['到船首']          = int(data[240:249],2)
    ais_data['到船尾']          = int(data[249:258],2)
    ais_data['到左舷']          = int(data[258:264],2)
    ais_data['到右舷']          = int(data[264:270],2)
    ais_data['定位装置类型']    = int(data[270:274],2)
    ais_data['UTC月']           = int(data[274:278],2)
    ais_data['UTC日']           = int(data[278:283],2)
    ais_data['UTC时']           = int(data[283:288],2)
    ais_data['UTC分']           = int(data[288:294],2)
    ais_data['最大静态吃水']    = float(int(data[294:302],2)/10)
    ais_data['目的地']          = decod_str(data[302:422])
    ais_data['DTE']             = data[423]
    return ais_data

# 第四类: type=18 标准B类设备的位置报告
def decod_18(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['转发指示符']      = int(data[6:8],2)
    ais_data['MMSI']            = int(data[8:38],2)
    ais_data['SOG']             = int(data[46:56],2)
    ais_data['位置准确度']      = data[56]
    ais_data['经度']            = sign_int(data[57:85])/600000.0
    ais_data['纬度']            = sign_int(data[85:112])/600000.0
    ais_data['COG']             = int(data[112:124],2)*0.1
    ais_data['实际航向']        = int(data[124:133],2)
    ais_data['时戳']            = int(data[133:139],2)
    ais_data['装置标志']        = data[141]
    ais_data['显示器标志']      = data[142]
    ais_data['DSC标志']         = data[143]
    ais_data['带宽标志']        = data[144]
    ais_data['消息22标志']      = data[145]
    ais_data['模式标志']        = data[146]
    ais_data['RAIM标志']        = data[147]
    ais_data['通信状态']        = int(data[148:168],2)
    return ais_data

# 第五类: type=19 拓展B类设备的位置报告
def decod_19(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['SOG']             = int(data[46:56],2)
    ais_data['位置准确度']      = data[56]
    ais_data['经度']            = sign_int(data[57:85])/600000.0
    ais_data['纬度']            = sign_int(data[85:112])/600000.0
    ais_data['COG']             = int(data[112:124],2)*0.1
    ais_data['实际航向']        = int(data[124:133],2)
    ais_data['时戳']            = int(data[133:139],2)
    ais_data['名称']            = decod_str(data[143:263])
    ais_data['到船首']          = int(data[271:280],2)
    ais_data['到船尾']          = int(data[280:288],2)
    ais_data['到左舷']          = int(data[289:295],2)
    ais_data['到右舷']          = int(data[295:301],2)
    ais_data['定位装置类型']    = int(data[301:305],2)
    ais_data['RAIM标志']        = data[305]
    ais_data['DTE']             = data[306]
    ais_data['搭配模式标志']    = data[307]
    return ais_data

# 第六类: type=21 助航设备报告
def decod_21(data):
    ais_data = {}
    ais_data['消息ID']          = int(data[0:6],2)
    ais_data['转发指示符']      = int(data[6:8],2)
    ais_data['MMSI']            = int(data[8:38],2)
    ais_data['设备类型']        = int(data[38:43],2)
    ais_data['设备名称']        = decod_str(data[43:163])
    ais_data['位置准确度']      = data[163]
    ais_data['经度']            = sign_int(data[164:192]) / 600000.0
    ais_data['维度']            = sign_int(data[192:219]) / 600000.0
    ais_data['到船首']          = int(data[219:228], 2)
    ais_data['到船尾']          = int(data[228:237], 2)
    ais_data['到左舷']          = int(data[237:243], 2)
    ais_data['到右舷']          = int(data[243:249], 2)
    ais_data['定位装置类型']    = int(data[249:253], 2)
    ais_data['时戳']            = int(data[253:259], 2)
    ais_data['偏置位置指示符']  = data[259]
    ais_data['AtoN状态']        = int(data[260:268], 2)
    ais_data['RAIM标志']        = data[268]
    ais_data['虚拟AtoN状态']    = data[269]
    ais_data['搭配模式标志']    = data[270]
    ais_data['设备名称拓展']    = decod_str(data[272:361])
    return ais_data

# 第七类: type=24 静态数据报告
def decod_24(data):
    ais_data = {}
    ais_data['消息ID']              = int(data[0:6],2)
    ais_data['转发指示符']          = int(data[6:8],2)
    ais_data['MMSI']                = int(data[8:38],2)
    ais_data['部分编号']            = int(data[38:40],2)
    if not(ais_data['部分编号']):
        # A部分
        ais_data['名称']            = decod_str(data[40:160])
    else:
        # B部分
        ais_data['船舶和货物类型']  = int(data[40:48],2)
        ais_data['供应商ID']        = int(data[48:66],2)
        ais_data['制造商ID']        = decod_str(data[48:90])  
        ais_data['单位模式码']      = int(data[66:70],2)
        ais_data['单位序列号']      = int(data[70:90],2)
        ais_data['呼号']     = decod_str(data[90:132])
        if not(ais_data['MMSI']//10000000 == 98):
            ais_data['到船首']      = int(data[132:141],2)
            ais_data['到船尾']      = int(data[141:150],2)
            ais_data['到左舷']      = int(data[150:156],2)
            ais_data['到右舷']      = int(data[156:162],2)
        else:
            ais_data['母船MMSI']    = int(data[132:162],2)
    return ais_data