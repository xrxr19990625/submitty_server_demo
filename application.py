from db import *
from flask import json
import time


def login(username, password):
    query = Users.select().where(Users.username == username)
    if len(query) == 0:
        return 0, ""
    else:
        for result in query:
            if result.password == password:
                return 200, "3267TRGEYUDHBWY247T3R3278GYUEB2G78R328GYUBEI1HEGBYUD"
            else:
                return 1, ""


def query_forum_home():
    query = Forum.select().order_by(Forum.last_reply).where(True)
    messages = []
    for result in query:
        json_dict = {
            "id": result.id,
            "username": result.username,
            "time": result.time,
            "message": result.message,
            'title': result.title,
            "last_reply": result.last_reply
        }
        messages.append(json.dumps(json_dict))
    return messages


def add_post(title, username, message):
    current_time = int(round(time.time() * 1000))
    Forum.create(title=title, username=username, time=current_time, message=message, last_reply=current_time)


def query_thread(id):
    query = Thread.select().where(Thread.root_thread == id)
    replies = []
    for rep in query:
        subreplies = []
        query_subreply = Floor.select().where(Reply.id == rep.reply.id)
        for subrep in query_subreply:
            subreply = {
                'id': subrep.sub_reply.id,
                'root': subrep.sub_reply.root,
                'parent': subrep.sub_reply.parent,
                'username': subrep.sub_reply.username,
                'message': subrep.sub_reply.message,
                'time': subrep.sub_reply.time,
                'parent_name': SubReply.get(id == subrep.sub_reply.id).username
            }
            subreplies.append(subreply)

        reply = {
            'id': rep.reply.id,
            'username': rep.reply.username,
            'message': rep.reply.message,
            'root': rep.reply.root,
            'time': rep.reply.time,
            'subreplies': subreplies
        }
        print(rep.reply.id, rep.reply.username, rep.reply.message, rep.reply.root, rep.reply.time)
        replies.append(json.dumps(reply))
    query1 = Forum.select().where(Forum.id == id)
    for root in query1:
        root_dict = {
            'id': root.id,
            'username': root.username,
            'time': root.time,
            'title': root.title,
            'message': root.message
        }
        return replies, json.dumps(root_dict)


def reply_to_thread(root_id, username, message):
    current_time = int(round(time.time() * 1000))
    reply_id = Reply.create(root=root_id, message=message, username=username, time=current_time).id
    reply_instance = Reply.get(id=reply_id)
    Thread.create(root_thread=root_id,
                  reply=reply_instance)
    forum_instance = Forum().get(id=root_id)
    forum_instance.last_reply = current_time
    forum_instance.save()


def reply_to_floor(root_thread, root_id, parent_id, username, message):
    current_time = int(round(time.time() * 1000))
    subreply_id = SubReply.create(root=root_id, parent=parent_id, message=message, username=username, time=current_time).id
    subreply_instance = SubReply.get(id=subreply_id)
    Floor.create(root_reply=root_id, sub_reply=subreply_instance)
    forum_instance = Forum().get(id=root_thread)
    forum_instance.last_reply = current_time
    forum_instance.save()


if __name__ == '__main__':
    print(login("xricxy1314", 'xuran1'))
    query_forum_home()
