from errno import errorcode
import re
import pandas as pd
from pyparsing import lineStart
from datetime import datetime

error_code_info_dict = {
    "": "",
    "E1001": "vsm收图1s超时",
    "E1002": "vsm收图校验错误",
    "E1003": "vpm解码超时异常",
    "E1004": "vpm解码错误",
    "E1005": "vpm连接dpm失败",
    "E1006": "发图给ddp错误",
    "E1007": "收到ddp错误码",
    "E1008": "接收ddp应答1s超时（包括错误码和推理结果）",
    "E1009": "帧对齐buffer被清空",
    "E1010": "帧对齐buffer满",
    "E1011": "ddp接收应答校验",
    "E1012": "与dpm连接重置",
    "E2001": "ddp收图1s超时",
    "E2002": "ddp收图校验错误",
    "E2003": "ddp发送数据错误",
    "E2004": "dpm解码超时异常",
    "E2005": "dpm解码错误",
    "E2006": "dpm连续解码错误（20次）",
    "E2007": "dpm启动进程60s之内没有收到图",
    "E2008": "dpm解码后Yuv大小不符合预期",
    "E2009": "dpm推理错误"
}

def get_line_info(line_string):
    time = line_string[0:23]
    error_code = line_string[-5:]
    return time, error_code


def log_strip(input_file_path, output_file_path):
    output_file = open(output_file_path, "w")
    match_lines = []
    with open(input_file_path) as input_file:
        lines = input_file.readlines()
        regex_string = r"App error code"
        rs1=r"ATCF1"
        rs2=r"ATCF2"
        for line in lines:
            pattern = re.compile(regex_string)
            pattern1 = re.compile(rs1)
            pattern2 = re.compile(rs2)

            result_list = pattern.findall(line) #进行匹配，找到所有满足条件的
            result_list1 = pattern1.findall(line)
            result_list2 = pattern2.findall(line)

            result_list.extend(result_list1)
            result_list.extend(result_list2)


            if len(result_list) > 0:
                print(line)
                with open(f'{save_excel_path}', 'a+', encoding='utf-8') as f:
                    f.write(line)
                    f.close()
                match_lines.append(line)
                output_file.write(line)


root_path = "/media/ztc/Data/work/LOG/2022-06-12/20/chhs/UB_28/"

vpm_original_file_path1 = root_path + "opt/log/LOG_ODM_System_1.txt"
vpm_original_file_path2 = root_path + "opt/log/LOG_ODM_System_2.txt"
vpm_file_path1 = root_path + "opt/log/log1_strip.txt"
vpm_file_path2 = root_path + "opt/log/log2_strip.txt"

dpm_original_file_path1 = root_path + "home/magicdepth/ztc/dpmlog/LOG_ODM_System_1.txt"
dpm_original_file_path2 = root_path + "home/magicdepth/ztc/dpmlog/LOG_ODM_System_2.txt"
dpm_file_path1 = root_path + "home/magicdepth/ztc/dpmlog/log1_strip.txt"
dpm_file_path2 = root_path + "home/magicdepth/ztc/dpmlog/log2_strip.txt"

save_excel_path = root_path + "/errorcode_timeline.txt"

# 筛选出有Error Code的代码行
log_strip(vpm_original_file_path1, vpm_file_path1)
log_strip(vpm_original_file_path2, vpm_file_path2)
log_strip(dpm_original_file_path1, dpm_file_path1)
log_strip(dpm_original_file_path2, dpm_file_path2)

# # 整理成时间线
# match_lines = []
# vpm_file1 = open(vpm_file_path1)
# vpm_file2 = open(vpm_file_path2)
# dpm_file1 = open(dpm_file_path1)
# dpm_file2 = open(dpm_file_path2)
# vpm_data1 = vpm_file1.read()
# vpm_data2 = vpm_file2.read()
# vpm_data = vpm_data1 + vpm_data2
# dpm_data1 = dpm_file1.read()
# dpm_data2 = dpm_file2.read()
# dpm_data = dpm_data1 + dpm_data2

# vpm_line_list = vpm_data.split("\n")
# dpm_line_list = dpm_data.split("\n")

# vpm_line_cursor = 0
# dpm_line_cursor = 0
# last_time = datetime.utcnow()
# df = pd.DataFrame(columns=['Time', 'VPM', 'DPM', 'Description'])
# while True:
#     if vpm_line_cursor >= len(vpm_line_list) and dpm_line_cursor >= len(dpm_line_list):
#         break
#     if vpm_line_cursor >= len(vpm_line_list):
#         dpm_line = dpm_line_list[dpm_line_cursor]
#         dpm_time_string, dpm_error_code = get_line_info(dpm_line)
#         print(f"dpm: {dpm_time_string}, {dpm_error_code}")
#         df.loc[len(df) + 1] = [dpm_time_string, "", dpm_error_code, error_code_info_dict[dpm_error_code]]
#         dpm_line_cursor = dpm_line_cursor + 1
#         if  dpm_time_string == "":
#             dpm_line_cursor = dpm_line_cursor + 1
#             continue
#         dpm_time = datetime.strptime(dpm_time_string,"%Y-%m-%d %H:%M:%S %f")
#         if (dpm_time-last_time).seconds > 10:
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#         last_time = dpm_time
#         continue
#     if dpm_line_cursor >= len(dpm_line_list):
#         vpm_line = vpm_line_list[vpm_line_cursor]
#         vpm_time_string, vpm_error_code = get_line_info(vpm_line)
#         print(f"vpm: {vpm_time_string}, {vpm_error_code}")
#         vpm_line_cursor = vpm_line_cursor + 1
#         if  vpm_time_string == "":
#             vpm_line_cursor = vpm_line_cursor + 1
#             continue
#         vpm_time = datetime.strptime(vpm_time_string,"%Y-%m-%d %H:%M:%S %f")
#         if (vpm_time-last_time).seconds > 10:
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#         df.loc[len(df) + 1] = [vpm_time_string, vpm_error_code, "", error_code_info_dict[vpm_error_code]]
#         last_time = vpm_time
#         continue

#     vpm_line = vpm_line_list[vpm_line_cursor]
#     dpm_line = dpm_line_list[dpm_line_cursor]
#     vpm_time_string, vpm_error_code = get_line_info(vpm_line)
#     dpm_time_string, dpm_error_code = get_line_info(dpm_line)
#     if  vpm_time_string == "":
#         vpm_line_cursor = vpm_line_cursor + 1
#         continue
#     if  dpm_time_string == "":
#         dpm_line_cursor = dpm_line_cursor + 1
#         continue
#     vpm_time = datetime.strptime(vpm_time_string,"%Y-%m-%d %H:%M:%S %f")
#     dpm_time = datetime.strptime(dpm_time_string,"%Y-%m-%d %H:%M:%S %f")
#     if vpm_time < dpm_time:
#         print(f"vpm: {vpm_time_string}, {vpm_error_code}")
#         vpm_line_cursor = vpm_line_cursor + 1
#         if (vpm_time-last_time).seconds > 10:
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#         df.loc[len(df) + 1] = [vpm_time_string, vpm_error_code, "", error_code_info_dict[vpm_error_code]]
#         last_time = vpm_time
#     else:
#         print(f"dpm: {dpm_time_string}, {dpm_error_code}")
#         dpm_line_cursor = dpm_line_cursor + 1
#         if (dpm_time-last_time).seconds > 10:
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#             df.loc[len(df) + 1] = ["", "", "", ""]
#         df.loc[len(df) + 1] = [dpm_time_string, "", dpm_error_code, error_code_info_dict[dpm_error_code]]
#         last_time = dpm_time


# df.to_excel(save_excel_path)