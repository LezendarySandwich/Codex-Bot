import os
from dotenv import load_dotenv

load_dotenv()
'''
Mongo connection for atlas server
'''
USERNAME_DB = os.environ.get('username_db')
PASSWORD_DB = os.environ.get('password_db')
MONOGODB_URI = f"mongodb://{USERNAME_DB}:{PASSWORD_DB}@clustercodexbot-shard-00-00.grs5l.mongodb.net:27017,clustercodexbot-shard-00-01.grs5l.mongodb.net:27017,clustercodexbot-shard-00-02.grs5l.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-kzt40j-shard-0&authSource=admin&retryWrites=true&w=majority"

'''
constants for codeforces manager
'''
MAX_SUBMISSIONS_RETRIEVED = os.environ.get("MAX_SUBMISSIONS_RETRIEVED")
SUBMISSION_RETRIEVAL_DELAY = os.environ.get("SUBMISSION_RETRIEVAL_DELAY")
'''
constants for discord manager
'''
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD = os.environ.get("DISCORD_GUILD")
DISCORD_BOT_CHANNEL_ID = int(os.environ.get('DISCORD_BOT_CHANNEL_ID'))
LOGGING_COG_CHANNEL_ID = int(os.environ.get('LOGGING_COG_CHANNEL_ID'))
CODEX_ICON_URI = os.environ.get('CODEX_ICON_URI')
HALL_OF_FAME_ID = os.environ.get('HALL_OF_FAME_ID')