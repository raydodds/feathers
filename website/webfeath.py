#!/usr/bin/python3
#
#
#

__author__ = 'Ray Dodds'

from bottle import route, run, template, static_file, get, post, request

# Make it look back directories
import sys
sys.path.append('../')
from delaunay.delaunayPreProc import proc_all

import os

	
@route('/favicon.ico')
def get_fav(filepath=None):
	return None

@route('/images/<filepath:path>')
def get_image(filepath=None):
	return static_file(filepath, root='./')

@route('/style/<filename>')
def get_style(filename=None):
	return static_file(filename, root='./')


@get('/')
@get('/<name:path>')
def main_page(name=None):
	vec_file = ''
	if('.' in name):
		taxa = []
		path = './'+name[:name.rfind('.')]+'_feath'
		#vec_file = open('testvec.svg').read()
		vec_file = proc_all(path, 2, 5, 0.25, 'c', 0, False)
	else:
		taxa = os.listdir('./'+name)
		taxa = filter(lambda x: '_feath' not in x, taxa)
		
	last_name= name[:name.rfind('/')]
	if('/' not in last_name):
		last_name = 'demoAves'

	
	return template('index', name=name, vec_file=vec_file, img_name='/images/'+name, taxa=taxa, last_name=last_name)

@post('/<name:path>')
def apply_settings(name=None):

	path = name[:name.rfind('.')]+'_feath'
	num_feath = int(request.forms.get('num_feath'))
	sample_thresh = int(request.forms.get('threshold'))
	sample_rate = int(request.forms.get('sample_rate'))/100
	filter_type = request.forms.get('filter')
	border_width = int(request.forms.get('border_width'))
	color = request.forms.get('color')


	vec_file = proc_all(path, num_feath, sample_thresh, sample_rate, filter_type, border_width, color)

	last_name= name[name.rfind('/')]
	img_name = '/images/'+name
	#vec_file = open('testvec.svg').read()
	return template('index', name=name, vec_file=vec_file, img_name=img_name, taxa = [], last_name=last_name)



	
run(host='localhost', port=5000)
