import requests

def request_server(com, devid, status):
    try:
        response = requests.get(f"http://data.magicdepth.com/caliupd/{com}/{devid}/{status}")
        if response.text == "0":
            ret = 0
        else:
            ret = -1
    except Exception as e:

        ret = -1
    return ret
 