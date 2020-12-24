import requests
import logging
import json
from . import constants
from . import database_manager as db

logger = logging.getLogger(__name__)


class Problem:

    def __init__(self, contest_id, index, rating, tags, problem_name, handle):
        self.contest_id = contest_id
        self.index = index
        self.rating = rating
        self.tags = tags
        self.problem_name = problem_name
        self.handle = handle

    def get_key(self):
        '''
        differentiate between two questions
        '''
        return (self.contest_id, self.index)

    def url_get(self):
        return f'http://codeforces.com/contest/{self.contest_id}/problem/{self.index}'


async def parse_submissions_response(username: str, response: str):
    '''
    return a list of Problems from the json
    :rtype: list(Problem)
    '''
    if not response:
        return list()
    if response['status'] == 'FAILED':
        comment = response['comment']
        logger.warn(f'Status: Failed, handle: {username}, comment: {comment}')
        return list()
    submissions = response['result']
    new_solved_problems = []

    for submission in submissions:
        if 'verdict' in submission and submission['verdict'] == 'OK':
            task = submission["problem"]
            rating = "??" if not 'rating' in task else str(task['rating'])
            problem = Problem(str(task["contestId"]), str(task["index"]), rating, list(task["tags"]), str(task["name"]), username)
            solved = await db.check_solved(handle=username, link=problem.url_get())
            if not solved:
                await db.insert_users_db(handle=username, link=problem.url_get())
                new_solved_problems.append(problem)
    return new_solved_problems


async def get_latest_submissions(username: str):
    '''
    returns a list of latest problems by the user
    '''
    try:
        response = requests.get(
            f'http://codeforces.com/api/user.status?handle={username}&from=1&count={constants.MAX_SUBMISSIONS_RETRIEVED}')
        response = json.loads(response.text)
        new_solved = await parse_submissions_response(username, response)
        return new_solved
    except requests.exceptions.ConnectionError:
        logger.exception('Connection Error')
        return parse_submissions_response(username, response=None)

async def latest_get_contest(handle: str):
    '''
    return last two contests given by the user
    :rtype: list of object RatingChange: e.g. https://codeforces.com/api/user.rating?handle=Fefer_Ivan
    '''
    response = requests.get(f'https://codeforces.com/api/user.rating?handle={handle}')
    response = json.loads(response.text)
    if response['status'] == 'FAILED':
        comment = response['comment']
        logger.warn(f'Status: Failed, handle: {handle}, comment: {comment}')
        return None
    else: 
        in_database = await db.contest_check(response['result'][-1]['contestId'])
        if not in_database: return response['result'][-1]
        else: return None