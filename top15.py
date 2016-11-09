# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, jsonify
from updateItemList import updateItemListThread

app = Flask(__name__)
app.config.from_pyfile('top15.cfg')
handling = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iframe')
def iframe():
    items = 0
    user_id = request.args.get('user_id', '0', type=str)
    object_type = request.args.get('object_type', '0', type=str)
    group_type = request.args.get('group_type', '0', type=str)
    order_by = request.args.get('order_by', '0', type=str)
    tag = request.args.get('tag', '0', type=unicode)
    if tag == '':
        tag = '0'
    filePath = 'data/' + user_id + ' ' + object_type + ' ' + group_type + ' ' + \
        order_by + ' ' + tag + '.json'
    if not os.path.exists(filePath):
        if filePath not in handling:
            update_thread = updateItemListThread(user_id, object_type, group_type, order_by, tag)
            update_thread.start()
            handling.append(filePath)
        return render_template('wait.html',
                               user_id=user_id,
                               object_type=object_type,
                               group_type=group_type,
                               order_by=order_by,
                               tag=tag)
    else:
        if filePath in handling:
            handling.remove(filePath)
        with open(filePath, 'r') as itemsFile:
            items = json.loads(itemsFile.read())
        if items == 0:
            return render_template('item_404.html')
        else:
            return render_template('iframe.html', items=items, object_type=object_type)
    return '200'

@app.route('/check')
def check():
    user_id = request.args.get('user_id', '0', type=str)
    object_type = request.args.get('object_type', '0', type=str)
    group_type = request.args.get('group_type', '0', type=str)
    order_by = request.args.get('order_by', '0', type=str)
    tag = request.args.get('tag', '0', type=unicode)
    if tag == '':
        tag = '0'
    filePath = 'data/' + user_id + ' ' + object_type + ' ' + group_type + ' ' + \
        order_by + ' ' + tag + '.json'
    if not os.path.exists(filePath) and filePath not in handling:
        return jsonify(result='0')
    else:
        if os.path.exists(filePath) and filePath in handling:
            handling.remove(filePath)
            return jsonify(result='1')
    return '200'

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
