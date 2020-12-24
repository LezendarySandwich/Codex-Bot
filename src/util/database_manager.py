import pymongo
from . import constants
from collections import OrderedDict
from datetime import date

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
                "required": ["handle"],
                "properties": {
                    "handle": {
                        "bsonType": "string",
                        "description": "Codeforces handle of the discord users",
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

def user_exist_db(handle: str):
    '''
    returns true if the user exists in the database otherwise False
    '''
    query = {"handle": handle}
    doc = User_db.find(query)
    return bool(doc.count())


def check_solved(handle: str, link: str):
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


def insert_users_db(handle: str, link: str = None):
    '''
    inserts user in the database if it does not already exist\
        also pushes the link to his solved problems if not already present
    '''
    if not user_exist_db(handle=handle):
        query = {"handle": handle}
        User_db.insert_one(query)
    if link is not None and not check_solved(handle=handle, link=link):
        date_current = date.today().strftime("%Y/%m/%d")
        User_db.update_one({"handle": handle}, {"$push": {"solved_problems": {
            "problem_link": link, "time_solved": date_current}}})

def contest_check(contestId: int):
    query = {"contestId": contestId}
    doc = Contest_db.find(query)
    return bool(doc.count())

def insert_contest(contestId: int):
    if not contest_check(contestId):
        date_current = date.today().strftime("%Y/%m/%d")
        query = {
            "contestId": contestId,
            "time_created": date_current
        }
        Contest_db.insert_one(query)

schema_code_stalker()
schema_contests_stalk()