#-*-coding:utf-8-*-
__author__ = 'vic'

import crawl_comments
class weibo_comment:
    """
    {
        "comments": [
            {
                "created_at": "Wed Jun 01 00:50:25 +0800 2011",
                "id": 12438492184,
                "text": "love your work.......",
                "source": "<a href="http://weibo.com" rel="nofollow">新浪微博</a>",
                "mid": "202110601896455629",
                "user": {
                    "id": 1404376560,
                    "screen_name": "zaku",
                    "name": "zaku",
                    "province": "11",
                    "city": "5",
                    "location": "北京 朝阳区",
                    "description": "人生五十年，乃如梦如幻；有生斯有死，壮士复何憾。",
                    "url": "http://blog.sina.com.cn/zaku",
                    "profile_image_url": "http://tp1.sinaimg.cn/1404376560/50/0/1",
                    "domain": "zaku",
                    "gender": "m",
                    "followers_count": 1204,
                    "friends_count": 447,
                    "statuses_count": 2908,
                    "favourites_count": 0,
                    "created_at": "Fri Aug 28 00:00:00 +0800 2009",
                    "following": false,
                    "allow_all_act_msg": false,
                    "remark": "",
                    "geo_enabled": true,
                    "verified": false,
                    "allow_all_comment": true,
                    "avatar_large": "http://tp1.sinaimg.cn/1404376560/180/0/1",
                    "verified_reason": "",
                    "follow_me": false,
                    "online_status": 0,
                    "bi_followers_count": 215
                },
                "status": {
                    "created_at": "Tue May 31 17:46:55 +0800 2011",
                    "id": 11488058246,
                    "text": "求关注。"，
                    "source": "<a href="http://weibo.com" rel="nofollow">新浪微博</a>",
                    "favorited": false,
                    "truncated": false,
                    "in_reply_to_status_id": "",
                    "in_reply_to_user_id": "",
                    "in_reply_to_screen_name": "",
                    "geo": null,
                    "mid": "5612814510546515491",
                    "reposts_count": 8,
                    "comments_count": 9,
                    "annotations": [],
                    "user": {
                        "id": 1404376560,
                        "screen_name": "zaku",
                        "name": "zaku",
                        "province": "11",
                        "city": "5",
                        "location": "北京 朝阳区",
                        "description": "人生五十年，乃如梦如幻；有生斯有死，壮士复何憾。",
                        "url": "http://blog.sina.com.cn/zaku",
                        "profile_image_url": "http://tp1.sinaimg.cn/1404376560/50/0/1",
                        "domain": "zaku",
                        "gender": "m",
                        "followers_count": 1204,
                        "friends_count": 447,
                        "statuses_count": 2908,
                        "favourites_count": 0,
                        "created_at": "Fri Aug 28 00:00:00 +0800 2009",
                        "following": false,
                        "allow_all_act_msg": false,
                        "remark": "",
                        "geo_enabled": true,
                        "verified": false,
                        "allow_all_comment": true,
                        "avatar_large": "http://tp1.sinaimg.cn/1404376560/180/0/1",
                        "verified_reason": "",
                        "follow_me": false,
                        "online_status": 0,
                        "bi_followers_count": 215
                    }
                }
            },
            ...
        ],
        "previous_cursor": 0,
        "next_cursor": 0,
        "total_number": 7
    }

    返回值字段	字段类型	字段说明
    created_at	string	评论创建时间
    id	int64	评论的ID
    text	string	评论的内容
    source	string	评论的来源
    user	object	评论作者的用户信息字段 详细
    mid	string	评论的MID
    idstr	string	字符串型的评论ID
    status	object	评论的微博信息字段 详细
    reply_comment	object	评论来源评论，当本评论属于对另一评论的回复时返回此字段

    reposts_count	int	转发数
    comments_count	int	评论数
    attitudes_count	int	表态数
    """
    def __init__(self, id, idstr, mid,  text, created_at, source, user_id):
        self.id = id
        self.idstr = idstr
        self.mid = mid
        self.text = text
        self.created_at = created_at
        self.source = source
        self.user_id = user_id

    def get_comments(self):
         #comment list
         comments =  crawl_comments.get_comments()
         # user
         comment_user = comments[0]['user']

         # weibo user
         status = comments[0]['status']
         weibouser = status['user']

    def save(self):
        pass


class weibo_user:
    """
    1. 评论用户
    2. 微博用户
    """
    pass


