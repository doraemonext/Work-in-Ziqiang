# -*-coding:utf-8-*-
from sgmllib import SGMLParser
import urllib
import urllib2
from bs4 import BeautifulSoup#解析html的库
import cookielib
import re
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#抓取空闲研修室的方法，输出格式见API文档
class reseverlib(SGMLParser):
    def getroominfo(self,year,month,day,xuebu):#获取空闲研修室信息，参数为年月日和学部（1是本部，2是医学部）
        self.year=year
        self.month=month
        self.day=day
        self.xuebu=xuebu
        self.roomids=[]
        nump=re.compile("room=\d+")
        dic={}    #返回字典格式见文档
        rooms={}    
        rooms['1']=[]
        rooms['2']=[]
        rooms['3']=[]
        rooms['4']=[]    #返回四个时间段分别空闲的房间号
#本部
        if int(self.xuebu)==1:
            url_1_6='http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=6'%(year,month,day)
            url_1_8='http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=8'%(year,month,day)
            url_1_9='http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=9'%(year,month,day)
            #根据日期和area访问相应页面（6，8，9是本部的三个区域）
            try:
                soup_1_6=BeautifulSoup(urllib2.urlopen(url_1_6))
                soup_1_8=BeautifulSoup(urllib2.urlopen(url_1_8))
                soup_1_9=BeautifulSoup(urllib2.urlopen(url_1_9))
            except urllib2.HTTPError,e:
                pass
            else:
                soup_1_6=BeautifulSoup(urllib2.urlopen(url_1_6))
                soup_1_8=BeautifulSoup(urllib2.urlopen(url_1_8))
                soup_1_9=BeautifulSoup(urllib2.urlopen(url_1_9))
                s_1_6=soup_1_6.find_all('a',class_='new_booking')
                s_1_8=soup_1_8.find_all('a',class_='new_booking')
                s_1_9=soup_1_9.find_all('a',class_='new_booking')
                    #抓取可以预订的空闲研修室链  接
                list_1_6=[]
                for i in s_1_6:
                    room=nump.findall(str(i))[0]
                    hour=re.search("hour=..",str(i)).group()
                    minute=re.search("minute=..",str(i)).group()
                    if hour=="hour=08":
                        list_1_6.append(1)
                        rooms['1'].append(room)    
                    elif hour=="hour=11":
                        list_1_6.append(2)
                        rooms['2'].append(room)
                    elif hour=="hour=15":
                        list_1_6.append(3)
                        rooms['3'].append(room)
                    elif hour=="hour=18":
                        list_1_6.append(4)
                        rooms['4'].append(room)
            #判断空闲时间段，并加入该研修室列表中，下同
                dic['B1.2']=list_1_6
                list_1_8_8=[]
                list_1_8_4=[]
                for i in s_1_8:
                    room=nump.findall(str(i))[0]
                    hour=re.search("hour=..",str(i)).group()
                    minute=re.search("minute=..",str(i)).group()
                    if room=="room=105":
                        if hour=="hour=08":
                            list_1_8_8.append(1)
                            rooms['1'].append(room)
                        elif hour=="hour=11":
                            list_1_8_8.append(2)
                            rooms['2'].append(room)
                        elif hour=="hour=15":
                            list_1_8_8.append(3)
                            rooms['3'].append(room)
                        elif hour=="hour=18":
                            list_1_8_8.append(4)           
                            rooms['4'].append(room)
                    else:
                        if hour=="hour=08":
                            list_1_8_4.append(1)
                            rooms['1'].append(room)
                        elif hour=="hour=11":
                            list_1_8_4.append(2)    
                            rooms['2'].append(room)
                        elif hour=="hour=15":
                            list_1_8_4.append(3)
                            rooms['3'].append(room)
                        elif hour=="hour=18":
                            list_1_8_4.append(4)
                            rooms['4'].append(room)
                dic['B1.8']=list_1_8_8
                dic['B1.4']=list_1_8_4
                list_1_9=[]
                for i in s_1_9:
                    room=nump.findall(str(i))[0]
                    hour=re.search("hour=..",str(i)).group()
                    minute=re.search("minute=..",str(i)).group()
                    if hour=="hour=08":
                        list_1_9.append(1)
                        rooms['1'].append(room)
                    elif hour=="hour=11":
                        list_1_9.append(2)
                        rooms['2'].append(room)
                    elif hour=="hour=15":
                        list_1_9.append(3)
                        rooms['3'].append(room)
                    elif hour=="hour=18":
                        list_1_9.append(4)
                        rooms['4'].append(room)    
                dic['B2.2']=list_1_9
#医学部    
        elif int(self.xuebu)==2:
            url_2_14='http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=14'%(year,month,day)
            url_2_12='http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=12'%(year,month,day)
            try:
                soup_2_14=BeautifulSoup(urllib2.urlopen(url_2_14,timeout=4))
                soup_2_12=BeautifulSoup(urllib2.urlopen(url_2_12,timeout=4))
            except urllib2.HTTPError,e:
                return "Error:Connection Error."
            else:
                s_2_14=soup_2_14.find_all('a',class_='new_booking')
                s_2_12=soup_2_12.find_all('a',class_='new_booking')
                list_2_12=[]
                for i in s_2_12:
                    room=nump.findall(str(i))[0]    
                    hour=re.search("hour=..",str(i)).group()
                    minute=re.search("minute=..",str(i)).group()
                    if hour=="hour=08":
                        list_2_12.append(1)
                        rooms['1'].append(room)
                    elif hour=="hour=11":
                        list_2_12.append(2)
                        rooms['2'].append(room)
                    elif hour=="hour=15":
                        list_2_12.append(3)
                        rooms['3'].append(room)
                    elif hour=="hour=18":
                        list_2_12.append(4)
                        rooms['4'].append(room)
                dic['Y2.1']=list_2_12 
                list_2_14_4=[]
                list_2_14_8=[]      
                for i in s_2_14:
                    room=nump.findall(str(i))[0]
                    hour=re.search("hour=..",str(i)).group()
                    minute=re.search("minute=..",str(i)).group()
                    if room=="room=101" or room=="room=102":
                        if hour=="hour=08":
                            list_2_14_4.append(1)
                            rooms['1'].append(room)
                        elif hour=="hour=11":
                            list_2_14_4.append(2)
                            rooms['2'].append(room)
                        elif hour=="hour=15":
                            list_2_14_4.append(3)
                            rooms['3'].append(room)
                        elif hour=="hour=18":
                            list_2_14_4.append(4)
                            rooms['4'].append(room)
                    else:
                        if hour=="hour=08":
                            list_2_14_8.append(1)
                            rooms['1'].append(room)
                        elif hour=="hour=11":
                            list_2_14_8.append(2)
                            rooms['2'].append(room)
                        elif hour=="hour=15":
                            list_2_14_8.append(3)
                            rooms['3'].append(room)
                        elif hour=="hour=18":    
                            list_2_14_8.append(4)
                            rooms['4'].append(room)
                dic['Y1.4']=list_2_14_4
                dic['Y1.8']=list_2_14_8
        return dic,rooms
                                 #人数  #时间段（1，2，3，4，见文档）
    def choseroom(self,dic,rooms,number,time):#参数为抓取获得的字典和用户选择的人数及时间,返回的为area和room的值
        self.time=time
        fitroom=[]
        global area
        if number=='1':
            if int(time) in dic['Y2.1']:
                area='12'
                if time=='1':
                    for room in rooms['1']:
                        rnum=int(room[5:])
                        if 71<=rnum and rnum<=100:
                            fitroom.append(rnum)
                elif time=='2':
                    for room in rooms['2']:
                        rnum=int(room[5:])
                        if 71<=rnum and rnum<=100:
                            fitroom.append(rnum)
                elif time=='3':
                    for room in rooms['3']:
                        rnum=int(room[5:])
                        if 71<=rnum and rnum<=100:
                            fitroom.append(rnum)
                elif time=='4':
                    for room in rooms['4']:
                        rnum=int(room[5:])
                        if 71<=rnum and rnum<=100:
                            fitroom.append(rnum)
            else:
                 area='0'
                 return "Error:no room avilivable"
        elif number=='2':
            if self.xuebu=='1':
                if int(time) in dic['B1.2']:
                    area='6'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if 16<=rnum and rnum<=23:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:
                            rnum=int(room[5:])
                            if 16<=rnum and rnum<=23:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if 16<=rnum and rnum<=23:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])
                            if 16<=rnum and rnum<=23:
                                fitroom.append(rnum)
                    else:
                        return "Error:no room avilivable"
                elif int(time) in dic['B2.2']:
                    area='9'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if 28<=rnum and rnum<=40:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:
                            rnum=int(room[5:])
                            if 28<=rnum and rnum<=40:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if 28<=rnum and rnum<=40:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])
                            if 28<=rnum and rnum<=40:
                                fitroom.append(rnum)
                else:
                    area='0'
                    return "Error:no room avilivable"
            else:
                return "Error:医学部没有二人研修室"
        elif number=='4':
            if self.xuebu=='1':
                if int(time) in dic['B1.4']:
                    area='8'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                else:
                    area='0'
                    return "Error:no room avilivable"
            else:
                if int(time) in dic['Y1.4']:
                    area='14'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if rnum==101 or  rnum==102:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:
                            rnum=int(room[5:])
                            if rnum==101 or  rnum==102:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if rnum==101 or  rnum==102:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])
                            if rnum==101 or  rnum==102:
                                fitroom.append(rnum)
                else:
                    area='0'
                    return "Error:no room avilivable"
        elif number=='8':
            if self.xuebu=='1':
                if int(time) in dic['B1.8']:
                    area='8'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if rnum==105:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:    
                            rnum=int(room[5:])
                            if rnum==105:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if rnum==105:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])
                            if rnum==105:
                                fitroom.append(rnum)
                else:
                    area='0'
                    return "Error:no room avilivable"
            else:
                if int(time) in dic['Y1.8']:
                    area='14'
                    if time=='1':
                        for room in rooms['1']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='2':
                        for room in rooms['2']:
                            rnum=int(room[5:])    
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='3':
                        for room in rooms['3']:
                            rnum=int(room[5:])
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    elif time=='4':
                        for room in rooms['4']:
                            rnum=int(room[5:])    
                            if rnum==103 or rnum==104:
                                fitroom.append(rnum)
                    else:
                        return "Error:no room avilivable"
        else:
            area='0'
            return "Error:Wrong number for people"
        global room_
        room_=str(fitroom[0])
        return room_,area      
    def getcookie(self,sid,pwd):#登录获得cookie字符串
        self.sid=sid
        self.pwd=pwd
        login_path = 'http://metalib.lib.whu.edu.cn/pds'#登录处理链接
        postdata = {'func':'login','calling_system':'mrbs','term1':'short','selfreg':'','bor_id':self.sid,'bor_verification':self.pwd,'institute':'WHU','url':'http://metalib.lib.whu.edu.cn:80/pds?'}#Post数据
        data=urllib.urlencode(postdata)  #编码      
        data=data.encode('utf-8')
        req = urllib2.Request(url=login_path,data=data)#处理请求
        response=urllib2.urlopen(req)
        soup=BeautifulSoup(response)#处理返回链接
        raw=soup.find_all("a",attrs={"href":re.compile("pds_handle")})#抓取含有pds_handle的链接
        href=raw[0]["href"]#获取链接
        p=re.compile("=(.*)&(.*)&")       
        pattern=p.split(href)
        pds_handle=pattern[1]   #匹配并截取pds_handle的数字部分内容
        global cookie
        cookie= "PDS_HANDLE="+pds_handle+'''; path="/"; domain=".lib.whu.edu.cn"; path_spec; domain_dot; expires="2015-08-21 04:24:11Z"; version=0'''   #形成cookie字符串
        return cookie
    def getuserinfo(self):#获取用户信息（主要是name和ID）
        req = urllib2.Request("http://metalib.lib.whu.edu.cn/pds?func=bor-info")
        req.add_header('Cookie', cookie)
        soup = BeautifulSoup(urllib2.urlopen(req))
        global name,ID
        name=soup.find('name').string.encode('gb2312') 
        ID=soup.find('id').string.encode('gb2312')      #获取name和id,id用于预订时的表单数据,原来就为unicode字符，
        return name,ID                                  #在后面编码数据中会出错，这里转换为gb2312         
    def autoreserv(self,description,tel,email,area,room):#进行研修室预订，需要用户输入的参数为月份，日期，起始时间，二人四人或八人间
        handpage='http://reserv.lib.whu.edu.cn/edit_entry_handler.php'
        if self.time=='1':
            time=8
        elif self.time=='2':
            time=11.5
        elif self.time=='3':
            time=15
        elif self.time=='4':
            time=18.5
        postdata={'name':name,
'description':description,
'start_day':self.day,
'start_month':self.month,
'start_year':'2014',
'start_seconds':str(time*3600),
'all_day':'no',
'end_day':self.day,
'end_month':self.month,
'end_year':'2014',
'end_seconds':str(time*3600+12600),
'area':area,
'rooms[]':room,
'type':'I',
'confirmed':'1',
'f_bor_id': self.sid,
'f_entry_tel':tel,
'f_entry_email':email,
'f_entry_person1':'',
'f_entry_person2':'',
'f_entry_person3':'',
'returl':'http://reserv.lib.whu.edu.cn/day.php?year=2014&month=%s&day=%s&area=%s'%(self.month,self.day,area),
'create_by':ID,
'rep_id':'0',
'edit_type':'series'}
        req = urllib2.Request(url=handpage,data=urllib.urlencode(postdata))
        req.add_header('Cookie', cookie)
        soup=BeautifulSoup(urllib2.urlopen(req))
        pageinfo=str(soup)#以下代码为获取预订的房间id
        links=soup.find_all('a',attrs={'href':re.compile('view_entry')})#抓取已预订的房间链接
        global roomid
        for link in links:   #str                 #将gb2312编码为utf-8
            if link.renderContents()==name.decode('gb2312'):
                linkofid=link['href']#获得链接中的网址部分（id包含在其中）
                linkstr=str(linkofid)
                numid=re.compile("id=\d+")
                roomid=numid.findall(linkstr)[0][3:]#正则匹配出id
                self.roomids.append(roomid)
        if 'Fatal error' in pageinfo:
            return '预订出错，请稍后再试'
        elif 'repeat reservation' in pageinfo:
            return '您已经预订过，无法继续预订研修室'
        elif 'Go To Today' in pageinfo:
            return '预订成功,'+'您的订单id为'+roomid+',房间号为'+room_
        return roomids
    def reservbyroom(self,tel,email,description,area,room):
        self.area=area
        self.room=room
        handpage='http://reserv.lib.whu.edu.cn/edit_entry_handler.php'
        if self.time=='1':
            time=8
        elif self.time=='2':
            time=11.5
        elif self.time=='3':
            time=15
        elif self.time=='4':
            time=18.5
        postdata={'name':name,
'description':description,
'start_day':self.day,
'start_month':self.month,
'start_year':'2014',
'start_seconds':str(time*3600),
'all_day':'no',
'end_day':self.day,
'end_month':self.month,
'end_year':'2014',
'end_seconds':str(time*3600+12600),
'area':area,
'rooms[]':room,
'type':'I',
'confirmed':'1',
'f_bor_id': self.sid,
'f_entry_tel':tel,
'f_entry_email':email,
'f_entry_person1':'',
'f_entry_person2':'',
'f_entry_person3':'',
'returl':'http://reserv.lib.whu.edu.cn/day.php?year=2014&month=%s&day=%s&area=%s'%(self.month,self.day,area),
'create_by':ID,
'rep_id':'0',
'edit_type':'series'}
        req = urllib2.Request(url=handpage,data=urllib.urlencode(postdata))
        req.add_header('Cookie', cookie)
        soup=BeautifulSoup(urllib2.urlopen(req))
        pageinfo=str(soup)#以下代码为获取预订的房间id
        links=soup.find_all('a',attrs={'href':re.compile('view_entry')})#抓取已预订的房间链接
        global roomid
        for link in links:   #str                 #将gb2312编码为utf-8
            if link.renderContents()==name.decode('gb2312'):
                linkofid=link['href']#获得链接中的网址部分（id包含在其中）
                linkstr=str(linkofid)
                numid=re.compile("id=\d+")
                roomid=numid.findall(linkstr)[0][3:]#正则匹配出id
                self.roomids.append(roomid)
        if 'Fatal error' in pageinfo:
            return '预订出错，请检查房间是否为空，或稍后再试'
        elif 'repeat reservation' in pageinfo:
            return '您已经预订过，无法继续预订研修室'
        elif 'Go To Today' in pageinfo:
            return '预订成功,'+'您的订单id为'+roomid
    def cancle(self):
        for roomid in self.roomids:
            handpage="http://reserv.lib.whu.edu.cn/del_entry.php?id=%s&amp;series=0&year=%s&month=%s&day=%s&area=%s&room=%s"%(roomid,self.year,self.month,self.day,area,room_)
            req = urllib2.Request(url=handpage)
            req.add_header('Cookie', cookie)
            soup=BeautifulSoup(urllib2.urlopen(req))
            pageinfo=str(soup)
            if 'do not have access' in pageinfo:
                return '取消预订失败，请稍后再试'
            elif 'Go To Today' in pageinfo:
                return '取消预订成功'
            else:
                return '未知错误'


test=reseverlib()#实例化
room_input=raw_input("请输入想要查询空闲研修室的日期（格式为yyyy,mm,dd),和你所在学部，本部为1，医学部为2,均用英文逗号隔开")
room_param=room_input.split(",")
dic=test.getroominfo(room_param[0],room_param[1],room_param[2],room_param[3])[0]#查询空闲研修室
rooms=test.getroominfo(room_param[0],room_param[1],room_param[2],room_param[3])[1]
print dic,rooms
chose_input=raw_input("请输入需要预订的人数（文理学部只有2人4人8人间，医学部有1人4人8人间）和时间段（8:00~11:30——1，11:30~15:00——2，15:00~18:30——3，18:30~22:00——4），用英文逗号隔开")
chose_param=chose_input.split(",")
print test.choseroom(dic,rooms,chose_param[0],chose_param[1])#如果没有房间，输出Error,不进行预订操作
if test.choseroom(dic,rooms,chose_param[0],chose_param[1])=="Error:no room avilivable":
    pass
else: 
    test.getcookie('2013302480033','114028')
    room=test.choseroom(dic,rooms,chose_param[0],chose_param[1])[0]
    area=test.choseroom(dic,rooms,chose_param[0],chose_param[1])[1]
    test.getuserinfo()
    info_input=raw_input("输入研修室用途，您的手机号和邮箱，用英文逗号隔开~")
    info_param=info_input.split(",")
    print test.autoreserv(info_param[0],info_param[0],info_param[0],area,room_)#自动分配研修室，返回房间号和订单Id
    #print test.reservbyroom('zzjh','1820717818','963949236@qq.com',area,'28')#用户通过输入房间号选择研修室
    print test.cancle()

