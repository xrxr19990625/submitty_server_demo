from peewee import *
import time

db = SqliteDatabase('server.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    id = PrimaryKeyField()
    username = CharField(null=False)
    password = CharField(null=False)


class Forum(BaseModel):
    id = PrimaryKeyField()
    username = CharField(null=False)
    time = BigIntegerField(null=False)
    title = CharField()
    message = CharField(null=False)
    last_reply = BigIntegerField(null=True)

    class Meta:
        order_by = ('last_reply',)


class Reply(BaseModel):
    id = PrimaryKeyField()
    root = IntegerField()
    message = CharField(null=False)
    username = CharField(null=False)
    time = BigIntegerField()

    class Meta:
        order_by = ('id',)


class SubReply(BaseModel):
    id = PrimaryKeyField()
    root = ForeignKeyField(Reply, to_field='id')
    parent = IntegerField()
    message = CharField(null=False)
    username = CharField(null=False)
    time = IntegerField(null=False)

    class Meta:
        order_by = ('id', )


class Floor(BaseModel):
    root_reply = ForeignKeyField(Reply, to_field='id')
    sub_reply = ForeignKeyField(SubReply)

    class Meta:
        order_by = ('id', )


class Thread(BaseModel):
    root_thread = ForeignKeyField(Forum, to_field='id')
    reply = ForeignKeyField(Reply)


if __name__ == "__main__":
    # Users.create_table()
    # Forum.create_table()
    # Reply.create_table()
    # SubReply.create_table()
    # Floor.create_table()
    # Thread.create_table()
    # Users.create(username="xur2", password="xuran1")
    Users.create(username="xur3", password="xuran1")
