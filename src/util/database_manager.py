from collections import OrderedDict
from datetime import date

def schema_code_stalker():
    '''
    Creates the collection for Users in the database if the collection already does not exist
    '''
    if collection not in db.list_collection_names():
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
        db.create_collection(collection)
        query = [('collMod', collection),
                 ('validator', validator)]
        db.command(OrderedDict(query))


def create_index_users(collection):
    '''
    creates the required indexes over fields
    '''
    if not collection.index_information():
        collection.create_index([("handle", 1)])
        collection.create_index([("solved_problems.problem_link", 1)])
        collection.create_index([("solved_problems.time_solved", 1)])
        print(collection.index_information())


def user_exist_db(handle: str, collection):
    '''
    returns true if the user exists in the database otherwise False
    '''
    query = {"handle": handle}
    doc = collection.find(query)
    return bool(doc.count())


def check_solved(handle: str, link: str, collection):
    '''
    returns true if the user had solved the problem otherwise False
    '''
    query = {
        "handle": handle,
        "solved_problems": {
            "$elemMatch": {
                "problem_link": link}}}
    doc = collection.find(query)
    return bool(doc.count())


def insert_users_db(handle: str, collection, link: str = None):
    '''
    inserts user in the database if it does not already exist\
        also pushes the link to his solved problems if not already present
    '''
    if not user_exist_db(handle=handle, collection=collection):
        query = {"handle": handle}
        collection.insert_one(query)
    if link is not None and not check_solved(handle=handle, link=link, collection=collection):
        date_current = date.today().strftime("%Y/%m/%d")
        collection.update_one({"handle": handle}, {"$push": {"solved_problems": {
                                  "problem_link": link, "time_solved": date_current}}})
