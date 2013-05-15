#-*-coding:utf-8-*-
"""
抓取微博评论, 当现场加用户分享一条消息到微博, 监控这条微博的所有评论
"""

import urllib
import hashlib
import weibo_tools
import httpsqs
import time
import urllib2
import json
import MySQLdb
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_statuses(count):
    hq = httpsqs.Httpsqs('202.85.215.157', 1218)
    weibos = []
    for i in range(count):
        #resp=hq.get('mining.comments_watch')
        #resp={"user_id": 17, "user_weibo_id": 2938518380, "status_id": 3550700656896440, "post_id": 327749, "time": "2013-02-28 15:27:19", "scene_id": 24}
        resp='{"user_id": 1566, "user_weibo_id": 1399737075, "status_id": 3550761994164937, "post_id": 327760, "time": "2013-02-28 19:31:03", "scene_id": 32}'
        if httpsqs.isOK(resp):
            weibo = json.loads(resp)
            weibos.append(weibo)
            time.sleep(1)
    return weibos

def post_data(data):
    url = 'http://1.livep.sinaapp.com/v1.0/scene_manager.php'
    jdata = json.dumps(data)
    req = urllib2.Request(url,data=jdata)
    req.add_header('Content-Type','application/json')
    response = urllib2.urlopen(req,timeout=20)

def get_comments(status):
    """
    request:
    source	false	string	采用OAuth授权方式不需要此参数，其他授权方式为必填参数，数值为应用的AppKey。
    access_token	false	string	采用OAuth授权方式为必填参数，其他授权方式不需要此参数，OAuth授权后获得。
    id	true	int64	需要查询的微博ID。
    since_id	false	int64	若指定此参数，则返回ID比since_id大的评论（即比since_id时间晚的评论），默认为0。
    max_id	false	int64	若指定此参数，则返回ID小于或等于max_id的评论，默认为0。
    count	false	int	单页返回的记录条数，默认为50。
    page	false	int	返回结果的页码，默认为1。
    filter_by_author
    """
    client = weibo_tools.DefaultWeiboClient()
    rec = client.comments__show(id=status['status_id'],count=10)
    if rec.has_key('comments'):
        comments = rec['comments']
        return comments
        # if len(comments)>0:
        #     process_comments(status = status,comments = comments)

from weibo_settings import DWC
def DefaultWeiboClient():
    APP_KEY = DWC['APP_KEY']
    APP_SECRET = DWC['APP_SECRET']
    CALLBACK_URL = DWC['CALLBACK_URL']
    user_name =DWC['user_name']
    user_psw = DWC['user_psw']
    return WeiboClient(APP_KEY,APP_SECRET,CALLBACK_URL,user_name,user_psw)

def if_user(status,user):
    login_name='weibo%s' % user['id']
    conn = MySQLdb.connect(host=host, user=user,passwd=passwd, db=db_app)
    cursor = conn.cursor()
    cursor.execute("select * from base_user where login_name=%s",(login_name+'1'))
    dbrow=cursor.fetchone()
    if dbrow==None:
        pwd=''
        post_id=status['post_id']
        to_comment_id=0
        to_user_id=status['user_weibo_id']
        scene_id=status['scene_id']
        if user['gender']=='f':
            gender=2
        elif user['gender']=='m':
            gender=1
        else:
            gender=0
        avatar_image=user['avatar_large']
        save_avatar(url=avatar_image,dst_dir='/data/image_storage/')

        signature=user['description']
        add_time=time.strftime("%Y-%m-%d %X",time.localtime())
        weibo_uid=user['id']
        new_user=(1,user['screen_name'],login_name,pwd,gender,avatar_image,signature,add_time)
        try:
            cursor.execute("insert into base_user(type, nickname,login_name,passwd,gender, avatar_image,signature,add_time) values(%s,%s,%s,%s,%s,%s,%s,%s)",new_user)
            conn.commit()
        except Exception,e:
            print e
        cursor.close()
        conn.close()

def save_avatar(url,dst_dir):
    pic=urllib.urlopen(url=url)
    avatar=pic.read()
    sha1=hashlib.sha1()
    sha1.update(avatar)
    digest=sha1.hexdigest()
    dir1=digest[:2]
    dir2=digest[2:4]
    file_path=os.path.join(dst_dir, dir1, dir2)
    file_name=os.path.join(file_path, digest+'.jpg')
    if not os.path.exists( file_path):
        os.makedirs(file_path)
    File=open(file_name,"wb" )
    File.write(avatar)
    File.close()

def process_comments(status,comments):
    post_id=status['post_id']
    to_comment_id=0
    to_user_id=status['user_weibo_id']
    scene_id=status['scene_id']
    all_comments=[]
    all_users=[]
    #评论倒序，全部插入表中，if_user判断如果是 新用户，要把人的资料插入到base_user，同时保留人的头像，根据sha1值保存到本地路径下
    for comment in comments[::-1]:
        content=comment['text']
        user_id=comment['user']['id']
        sina_comment_id=comment['id']
        all_comments.append((post_id,to_comment_id,user_id,to_user_id,scene_id,content))
        user=comment['user']
        if_user(status=status,user=user)

    conn = MySQLdb.connect(host=host, user=user,passwd=passwd,db=db_app)
    cursor = conn.cursor()
    cursor.executemany("insert into base_scene_post_comment(post_id, to_comment_id,user_id,to_user_id, scene_id, content) values (%s,%s,%s,%s,%s,%s)" ,all_comments)
    conn.commit()
    cursor.close()
    conn.close()

    #记录这条微博的最新评论，以便增量更新，实时更新
    comment=comments[0]
    since_id=comment['id']
    user_weibo_id=status['user_weibo_id']
    scene_id=status['scene_id']
    user_id=status['user_id']
    status_id=status['status_id']
    first_time=time.strftime("%Y-%m-%d %X",time.localtime())
    #resp='{"user_id": 1566, "user_weibo_id": 1399737075, "status_id": 3550761994164937, "post_id": 327760, "time": "2013-02-28 19:31:03", "scene_id": 32}'
    try:
        conn = MySQLdb.connect(host=host, user=user,passwd=passwd,db=db_crawl)
        cursor = conn.cursor()
        cursor.execute("insert into user_comment_log(user_id,user_weibo_id,status_id,since_id,first_time,last_time,times) values(%s,%s,%s,%s,%s,%s,%s)",\
            (user_id,user_weibo_id,status_id,first_time,0))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception,e:
        print e

from weibo_tools.weibo_settings import Run_config
if __name__ == '__main__':
    host, user, passwd, db_crawl, db_app = Run_config.values()
    flag = True
    while 1:
        status = {}
        status = {'status_id': 3577452087325613, 'count': 10}
        comments = get_comments(status=status)
        print "comments===", comments
        # time.sleep(1)
        # statuses=get_statuses(count=1)
        # if len(statuses)>0:
        #     for status in statuses:
        #         time.sleep(0.5)
        #         comments=get_comments(status=status)
        #         print "comments===", comments
        #         #process_comments(status=status,comments=comments)


