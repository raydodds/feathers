#!/usr/bin/python3
#
#
#

__author__ = 'Ray Dodds'

from bottle import route, run, template, static_file


@route('/')
@route('/<name>')
def main_page(name=None):
	vec_file=open('testvec.svg').read()
	img_name = 'images/ROSP_wing_male.png'
	return template('index', name=name, vec_file=vec_file, img_name=img_name)

@route('/images/<filename>')
def get_image(filename=None):
	return static_file(filename, root='./')

run(host='localhost', port=5000)
