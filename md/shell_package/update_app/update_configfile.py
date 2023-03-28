import re

new_file = "/media/ztc/Data/update/gdpm/gdpm_v2.0_2022121933/gdpm_v2.0_2022121933/config/user_gdpm_config.xml"
old_file = ""
with open(new_file, 'r') as f:
    new_config = f.readlines()

with open(old_file, 'r') as f:
    old_config = f.readlines()

for i, line in enumerate(old_config):
