import streamlit as st

import time
from datetime import datetime
import requests ,re ,json


def request_first(authorization):
    headers = {
        "Host": "park.lhsysz.com",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "GmToken": "9",
        "xweb_xhr": "1",
        "Authorization": authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        "Content-Type": "application/json",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        'Referer': 'https://servicewechat.com/wxda6d35e0951cf46d/71/page-frame.html',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    
    # url = "https://park.biz.baoneng.com/shop/v1/parking/info?car_no=%E7%B2%A4BBQ9667&type=car&gm_id=9" 
    url = "https://park.lhsysz.com/shop/v1/parking/info?car_no=%E7%B2%A4BBQ9667&type=car&gm_id=9" 

    response = requests.get(url, headers=headers)
    data = response.json()
    user_id = data['result']['card']['user_id']

    order = data['result']['orders']
    
    begin = order['begin']
    fee = order['fee']
    duration = order['stay_duration']
    third_no = order['third_no'] #第二次请求参数使用
    return third_no,fee,begin,duration,user_id

def request_second(authorization,third_no,fee,begin):
    url = "https://park.biz.baoneng.com/shop/v1/parking/pay"
    headers = {
        'Host': 'park.lhsysz.com',
        "Connection": "keep-alive",
        # "Content-Length": "318",  # Adjust based on actual data length
        "Accept": "application/json",
        "GmToken": "9",
        "xweb_xhr": "1",
        "Authorization": authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        "Content-Type": "application/json",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        'Referer': 'https://servicewechat.com/wxda6d35e0951cf46d/71/page-frame.html',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    data = {"code":"0c3Cgx0w30UKV23Hr10w3HLZER3Cgx0M","car_no":"粤BBQ9667","card_no":"粤BBQ9667","entry_time":begin,"third_pay":True,"third_no":third_no,"fee":fee,"discount_fee":fee,"coupon_code":"","coupon_name":"","coupon_fee":"","consume_point_fee":0,"discount_total":fee,"card_id":22}

    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    payurl = res['result']['data']['payUrl']

    pattern = r"orderNo=(\w+)"
    match = re.search(pattern, payurl)
    order_number = match.group(1)
    return order_number

def request_third(order_number):
    headers = {
        "Host": "sytgate.jslife.com.cn",
        "Connection": "keep-alive",
        "Content-Length": "365",
        "xweb_xhr": "1",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        'Referer': 'https://servicewechat.com/wx24b70f0ad2a9a89a/243/page-frame.html',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    data = {
        "userId": "",
        "orderNo": order_number, #///////
        "appType": "MINI_JSCARLIFE",
        "channelId": "LKL_WX",
        "subChannelId": "WeChat",
        "couponList": [],
        "callbackUrl": "MINI_JSCARLIFE",
        "payType": "MINI_PROGRAM",
        "reqSource": "WX_JTC",
        "openId": "ofjjT5LRjJb_dmRhPO0D3YqcT598",
        "appSource": "WX",
        "subAppSource": "WX_XCX_JTC",
        "unionId": "oRWxE56FsqijsUCbuZMUrKnXQKQ4",
        "version": "2.0"
    }
    data1 ={"orderNo":order_number,"appType":"SERVICE"}
    response = requests.post("https://sytgate.jslife.com.cn/core-gateway/payop/queryPayType", headers=headers, json=data1)
    
    response = requests.post("https://sytgate.jslife.com.cn/core-gateway/order/pay/prepay", headers=headers, json=data).json()
    print('支付信息:',response)
    resultCode = response['resultCode']
    return resultCode

  
def pay(authorization):
     
    try:
        # print("authorization：",authorization)
        first_results = request_first(authorization)
        third_no,fee,begin,duration,user_id = first_results
        print("third_no：",third_no, "入场时间：", begin, "用户ID：", user_id,"停车时长：",duration, "费用：",fee)
        # # //////////////////////////////2//////////////////////////////////////////////////////
        if(fee!=20): # 交费
            order_number = request_second(authorization,third_no,fee,begin)
            print("order_number：",order_number)
        # # /////////////////////////////3//////////////////////////////////////////////////////
            resultCode = request_third(order_number)
            if resultCode == 2323:
                return f"✅缴费成功 {fee}元"
            elif resultCode == 3138:
                return f"❌请求频繁系统拒绝 {fee}元"
            else:
                return f"❌支付码已经使用 {fee}元"
                
                    
        else:
            print(":::先不用交费")
            return "先不用交费"
    except Exception as e:
        print("异常>>>>>>>>>>>","问题原因：",e)
        return "异常"




     

st.title("🎈 My new app")


st.write("Hello world!")
st.write("I'm a paragraph")

if st.button("pay"):
    result = pay("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkyMWNkYmFhNzQ2NDkzZjdkZTgwYTgyOGExZTU2MWM5NWEyM2YyMDQ0YjA5MjQzY2MwYzdhMTUwNmNlODZkZTAwYmFiYmI1NjNiMDczY2ExIn0.eyJhdWQiOiIyIiwianRpIjoiOTIxY2RiYWE3NDY0OTNmN2RlODBhODI4YTFlNTYxYzk1YTIzZjIwNDRiMDkyNDNjYzBjN2ExNTA2Y2U4NmRlMDBiYWJiYjU2M2IwNzNjYTEiLCJpYXQiOjE3MzIwODA2ODMsIm5iZiI6MTczMjA4MDY4MywiZXhwIjoxNzM0NjcyNjgzLCJzdWIiOiI4NDcyNDUiLCJzY29wZXMiOlsiKiJdfQ.Fs3JCPGNXz85FdCw9dOtm3teZwOwjvXcoJjEp1eo2qVWUkHMW4EzK70blzqjRk2V-Tnn0opAgl3GCjA8Om6zQ730Br3pgUHe3cOSYFsKdaTGWlckbO2SWvycGDm3N1ymW4p0fOVCHlpFOR5bC9u5AfLj7Op4jnheBL__PCE3uqsu2gyC_Ho_FD13m57J3PyLhpZt41cNNZLSozWnO2HUxbyvimTgHo8M_zK8lyFuDLTrRyKm2aJn6jTr9AiEuanS3urgGjJrNp_J9fXz7EEvzpnvQHfyFwvF3B4cpUaramG3Ex5QI2z8T5-6l8aFIBrSw2CK5Wpqngb_tyzE6OVFUBJaU9EW-L2EmfTtrYJKxzDulx8ggpRKUF_XsF6InCEiw8ek6Bmdo2q5Cvv6iZKanVqrtDV2HQqlllezdavTEa2GhSDbfp_HVaTI2wBvaNiuPac1t8VqodAKysdDn34CHpxqZKnQAnbagEZLxLI819kIpYcTTAOiwzvEFiseRUuvp94sw2SFA76pCX6gCYd-3VfOXvKQBvrt4Wps3xU9ajuwmQy1qlNcp1W-IZVU4XdvpyvG2_jkDuo7Ihw8LEzRGXW77sh1Ny9I_B7pO4U0gWVWgBz6gZWJbFnUQerfCo71UbTVtLvT4495K5pp8NBqLMheSYnaCkGCVXDarRE7cCE")
    st.write(result)