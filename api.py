from flask import *
from application import *
app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login_api():
    if request.method != "POST":
        abort(400)
    else:
        data = json.loads(request.get_data(as_text=True))
        username = data['username']
        password = data['password']
        status, token = login(username, password)
        print(username, password)
        json_dict = {
            'status': status,
            'token': token
        }
        response = json.dumps(json_dict)
        return response


@app.route('/forum', methods=['POST'])
def forum_home_api():
    response_body = query_forum_home()
    json_dict = {
        'all': response_body
    }
    return json.dumps(json_dict)


@app.route('/new_post', methods=['POST'])
def new_post_api():
    data = json.loads(request.get_data(as_text=True))
    add_post(data['title'], data['username'], data['message'])
    json_dict = {
    }
    return json.dumps(json_dict)


@app.route('/thread_detail', methods=['POST'])
def get_thread_detail():
    data = json.loads(request.get_data(as_text=True))
    response = query_thread(data['id'])
    json_dict = {
        'replies': response[0],
        'root_info': response[1]
    }
    return json.dumps(json_dict)


@app.route('/reply_to_thread', methods=['POST'])
def reply_thread():
    data = json.loads(request.get_data(as_text=True))
    return json.dumps(reply_to_thread(data['root_id'], data['username'], data['message'])[1])


@app.route('/reply_to_reply', methods=['POST'])
def reply_floor():
    data = json.loads(request.get_data(as_text=True))
    return json.dumps({"subreplies": reply_to_floor(data['root_thread'], data['root_id'], data['parent_id'], data['username'], data['message'])})


@app.route('/subreps', methods=['POST'])
def get_subreps():
    data = json.loads(request.get_data(as_text=True))
    subreps = {
        "floor": query_subreps(data['floor_id'])
    }
    print(type(subreps))
    return json.dumps(subreps)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
