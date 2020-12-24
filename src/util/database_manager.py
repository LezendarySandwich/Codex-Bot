import pymongo
from . import constants
from collections import OrderedDict
from datetime import date
import time

client = pymongo.MongoClient(constants.MONOGODB_URI)
db = client["CodeStalker"]
User_db = db["Users"]
Contest_db = db["Contests"]

def schema_code_stalker():
    '''
    Creates the collection for Users in the database if the collection already does not exist
    '''
    if 'Users' not in db.list_collection_names():
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["handle", "subbed_code_stalk"],
                "properties": {
                    "handle": {
                        "bsonType": "string",
                        "description": "Codeforces handle of the discord users",
                    },
                    "subbed_code_stalk":{
                        "bsonType": "bool",
                        "description": "True if the user allows the bot to stalk him otherwise False"
                    },
                    "solved_problems": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["problem_link", "time_solved"],
                            "properties": {
                                "problem_link": {
                                    "bsonType": "string",
                                    "description": "Link of the solved codeforces problem",
                                },
                                "time_solved": {
                                    "bsonType": "string",
                                    "description": "Time at which problem was solved by the user"
                                }
                            }
                        }
                    }
                }
            }
        }
        db.create_collection('Users')
        query = [('collMod', 'Users'),
                 ('validator', validator)]
        db.command(OrderedDict(query))
        create_index_users()

def schema_contests_stalk():
    '''
    Creates the database for Contests if the collection does not exist
    '''
    if 'Contests' not in db.list_collection_names():
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["contestId", "time_created"],
                "properties": {
                    "contestId": {
                        "bsonType": "int",
                        "description": "The id of the contest"
                    },
                    "time_created": {
                        "bsonType": "string"
                    }
                }
            }
        }
        db.create_collection('Contests')
        query = [('collMod', 'Contests'),
                 ('validator', validator)]
        db.command(OrderedDict(query))
        create_index_contests()

def create_index_users():
    '''
    creates the required indexes over fields
    '''
    if not User_db.index_information():
        User_db.create_index([("handle", 1)])
        User_db.create_index([("solved_problems.problem_link", 1)])
        User_db.create_index([("solved_problems.time_solved", 1)])
        print(User_db.index_information())

def create_index_contests():
    '''
    creates the required indexes for Contests collection
    '''
    if not Contest_db.index_information():
        Contest_db.create_index([("contestId", 1)])
        Contest_db.create_index([("time_created", 1)])

async def user_exist_db(handle: str):
    '''
    returns true if the user exists in the database otherwise False
    '''
    query = {"handle": handle}
    doc = User_db.find(query)
    return bool(doc.count())

async def check_solved(handle: str, link: str):
    '''
    returns true if the user had solved the problem otherwise False
    '''
    query = {
        "handle": handle,
        "solved_problems": {
            "$elemMatch": {
                "problem_link": link}}}
    doc = User_db.find(query)
    return bool(doc.count())

async def stalk_sub_check(handle: str):
    '''
    returns True if the person is subscribed to stalking services of the bot otherwise returns False
    '''
    query = {"handle": handle}
    doc = User_db.find(query)
    entries_status = doc.count()
    for i in doc: doc = i
    result = doc["subbed_code_stalk"] if entries_status else True
    return result

async def stalk_sub_update(handle: str, sub_status: bool):
    '''
    updates the subbed_code_stalk field for the user
    '''
    query = {"handle": handle}
    newvalues = { "$set": { "subbed_code_stalk": sub_status } }
    User_db.update_one(query, newvalues)

async def insert_users_db(handle: str, link: str = None):
    '''
    inserts user in the database if it does not already exist\
        also pushes the link to his solved problems if not already present
    '''
    user_exists = await user_exist_db(handle=handle)
    if not user_exists:
        query = {"handle": handle, "subbed_code_stalk": True}
        User_db.insert_one(query)
    solved = await check_solved(handle=handle, link=link)
    if link is not None and not solved:
        date_current = date.today().strftime("%Y/%m/%d")
        User_db.update_one({"handle": handle}, {"$push": {"solved_problems": {
            "problem_link": link, "time_solved": date_current}}})

async def contest_check(contestId: int):
    query = {"contestId": contestId}
    doc = Contest_db.find(query)
    return bool(doc.count())

async def insert_contest(contestId: int):
    contest_exist = await contest_check(contestId)
    if not contest_exist:
        date_current = date.today().strftime("%Y/%m/%d")
        query = {
            "contestId": contestId,
            "time_created": date_current
        }
        Contest_db.insert_one(query)

schema_code_stalker()
schema_contests_stalk()
