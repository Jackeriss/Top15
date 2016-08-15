import os
import json
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, jsonify
from updateItemList import updateItemListThread

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
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
    filePath = 'data/' + user_id + ' ' + object_type + ' ' + group_type + ' ' + \
        order_by + '.json'
    if not os.path.exists(filePath):
        if filePath not in handling:
            update_thread = updateItemListThread(user_id, object_type, group_type, order_by)
            update_thread.start()
            handling.append(filePath)
        return render_template('wait.html',
                               user_id=user_id,
                               object_type=object_type,
                               group_type=group_type,
                               order_by=order_by)
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
    filePath = 'data/' + user_id + ' ' + object_type + ' ' + group_type + ' ' + \
        order_by + '.json'
    if not os.path.exists(filePath) and filePath not in handling:
        return jsonify(result='0')
    else:
        if os.path.exists(filePath) and filePath in handling:
            handling.remove(filePath)
            return jsonify(result='1')
    return '200'

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

if __name__ == '__main__':
    app.run()
