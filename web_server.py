#!/usr/bin/env python
from bottle import get, post, request, run, static_file, abort, template
import datetime
import os

def check_ext(filename, desired_extensions):
  name, ext = os.path.splitext(filename)
  ext = ext.strip('.')
  if ext not in desired_extensions:
    abort(500, 'File extension not allowed.')

@get('/')
def index():
    return static_file("index.html", '.')

@get('/map/<id>')
def map(id):
    return static_file("map.html", '.')

@post('/upload')
def do_upload():
    seafet = request.files.get('seafet')
    gpx = request.files.get('gpx')
    check_ext(seafet.filename, ["xlsx"])
    check_ext(gpx.filename, ["gpx"])
    mid = str(datetime.datetime.now()).replace(':', '_')
    path = "datasets/" + mid
    os.makedirs(path)
    seafet.save(path + '/seafet.xlsx')
    gpx.save(path + '/tracks.gpx')
    return template('upload', mid=mid)

@get('/datasets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='datasets')

run(host='localhost', port=8080) 
