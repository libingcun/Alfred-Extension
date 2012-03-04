#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2012 Henson <libingcun@gmail.com>
# Time-stamp: <2012-03-04 18:00:30 Henson>

import os, sys
import webbrowser
import cPickle as pickle

from qqweibo import OAuthHandler, API, JSONParser, ModelParser

API_KEY = 'd8d7cfaba418427dac1e38274d582fa5'
API_SECRET = '5573302d23865d0fa8900b637d457832'

class AlfredQQWeibo():
	auth = OAuthHandler(API_KEY, API_SECRET)
	setting = {}

	def load_setting(self):
		with open ('setting.pickle','rb') as f:
			self.setting = pickle.load(f)

	def save_setting(self):
		with open ('setting.pickle','wb') as f:
			pickle.dump(self.setting,f)

	def verify(self):
		auth_url = self.auth.get_authorization_url()

		requestToken = self.auth.request_token.key
		requestTokenSecret = self.auth.request_token.secret

		if (requestToken != None and requestToken.count > 0):
			print "确认授权后,运行:\n \"qwb pin {授权码}\""
			self.setting['request_token'] = requestToken
			self.setting['request_token_secret'] = requestTokenSecret
			self.save_setting()
			webbrowser.open(auth_url)
		else:
			print 'ERROR, try again pls.'

	def getAccessToken(self, pin):
		self.load_setting()
		self.auth.set_request_token(self.setting['request_token'], self.setting['request_token_secret'])
		access_token = self.auth.get_access_token(pin)

		if (access_token.key != None and access_token.secret != None 
		and access_token.key.count > 0 and access_token.secret.count >0):
			self.setting['access_token'] = access_token.key;
			self.setting['access_token_secret'] = access_token.secret;
			self.save_setting()
			print '验证成功.运行"qwb {message}",发送微博'
		else:
			print "ERROR, try again pls."
	
	def tweet(self, message):
		self.load_setting()
		self.auth.set_request_token(self.setting['request_token'],self.setting['request_token_secret'])
		self.auth.set_access_token(self.setting['access_token'],self.setting['access_token_secret'])

		api = API(self.auth, parser=ModelParser())
		ret = api.tweet.add(message, clientip='127.0.0.1')

		if (ret):
			tw = api.tweet.show(ret.id)
			print ('发送成功:微博ID={0.id}\n用户名={0.nick}\n内容={0.text}'.format(tw))

def main():
    argv = sys.argv[1:][0]
    parm = argv.split(" ")
	
    alfredQQWeibo = AlfredQQWeibo() 
    
    if (parm[0] == "setup"):
    	alfredQQWeibo.verify()
    elif (parm[0] == "pin"):
    	alfredQQWeibo.getAccessToken(parm[1])
    else:
    	alfredQQWeibo.tweet(argv)

if __name__ == "__main__":
    main()



