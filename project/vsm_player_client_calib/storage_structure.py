import struct
from enum import Enum


class VpmBaseSubDataType(Enum):
    eBSDT_LeftCorrectGrayImage = 0
    eBSDT_RightCorrectGrayImage = 1
    eBSDT_LeftCorrectYuvImage = 2
    eBSDT_RightCorrectYuvImage = 3
    eBSDT_LeftCorrectH264Image = 4
    eBSDT_RightCorrectH264Image = 5
    eBSDT_LeftCorrectRgbImage = 6
    eBSDT_RightCorrectRgbImage = 7
    eBSDT_DepthImage = 8
    eBSDT_EscalatorWorkStatus = 9
    eBSDT_ExtraRgbImage = 10  # extra RGB image for eBSDT_LeftCorrectRgbImage or eBSDT_RightCorrectRgbImage
    eBSDT_BackgroundDepthImage = 11
    eBSDT_End = 12


class SVPCM_IMAGE_TYPE(Enum):
    IMAGE_TYPE_UNDEFINE = 0
    IMAGE_TYPE_LEFT_GRAY = 1
    IMAGE_TYPE_RIGHT_GRAY = 2
    IMAGE_TYPE_LEFT_COLOR = 3
    IMAGE_TYPE_RIGHT_COLOR = 4
    IMAGE_TYPE_DEPTH = 5
    IMAGE_TYPE_END = 6


def tag_image_frame(data):
    TimeStampLow = struct.unpack('I', data[20:24])[0]
    TimeStampHigh = struct.unpack('I', data[24:28])[0]
    TimeStamp = TimeStampHigh + TimeStampLow / 1000000
    return {
        'PacketLength': struct.unpack('I', data[:4])[0],
        'ImageType': struct.unpack('I', data[4:8])[0],
        'ImageSequence': struct.unpack('I', data[8:12])[0],
        'CheckSum': struct.unpack('I', data[12:16])[0],
        'ImageWidth': struct.unpack('H', data[16:18])[0],
        'ImageHeight': struct.unpack('H', data[18:20])[0],
        'TimeStampLow': struct.unpack('I', data[20:24])[0],
        'TimeStampHigh': struct.unpack('I', data[24:28])[0],
        'TimeStamp': TimeStamp,
        'ImageQuality': struct.unpack('B', data[28:29])[0],
        'Reserved1': struct.unpack('B', data[29:30])[0],
        'Reserved2': struct.unpack('B', data[30:31])[0],
        'ImageExposure': struct.unpack('B', data[31:32])[0],
        # 'ImageBuffer': data[32:struct.unpack('I', data[:4])[0]]
    }



def check_sum_32(data, data_length):
    sum_number = 0
    # 前64个字节
    sum_len = 0
    buffer = data[0:64]
    while sum_len < 64:
        if 12 <= sum_len < 16:
            sum_len += 1
            continue
        sum_number += buffer[sum_len]
        sum_len += 1
    # 后64个字节
    sum_len = 0
    buffer = data[data_length - 64:]
    while sum_len < 64:
        sum_number += buffer[sum_len]
        sum_len += 1
    return sum_number


def vpm_image_data_decoder(data):
    DataLength = struct.unpack('>i', data[52:56])[0]
    return {
        "ChannelIndex": struct.unpack('>h', data[0:2])[0],  # int16_t  ChannelIndex;
        "Type": struct.unpack('>h', data[2:4])[0],
        "Width": struct.unpack('>h', data[4:6])[0],
        "Height": struct.unpack('>h', data[6:8])[0],
        "BitWidth": struct.unpack('>h', data[8:10])[0],
        "Quality": struct.unpack('>h', data[10:12])[0],
        "IsIFrame": struct.unpack('>l', data[12:16])[0],
        "Timestamp": struct.unpack('>Q', data[16:24])[0],
        "SequenceNumber": struct.unpack('>Q', data[24:32])[0],
        "DataLength": struct.unpack('>i', data[52:56])[0]
        # "Data": struct.unpack(f'>{struct.unpack(">i", data[52:56])[0]}b', data[56:]),  # int8_t   Data[8];
        # "rawdata": data[56:DataLength+56]
    }