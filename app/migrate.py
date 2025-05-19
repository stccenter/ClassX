from os import environ
from typing import List
from classxlib.database import DatabaseService
from classxlib.database.model import User, UserResearchField
from dotenv import load_dotenv

load_dotenv(".env")

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+environ.get('MYSQL_ROOT_USER')+':'+environ.get('MYSQL_ROOT_PASSWORD')+'@'+environ.get('HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('DB')

db = DatabaseService(SQLALCHEMY_DATABASE_URI)


users: List[User] = db.user_service.repo.get_all_by_args()
default_ids = db.research_field_service.get_default_fields()

for user in users:
    for default_id in default_ids:
        db.user_research_fields_service.add_research_field(user.id, default_id.id)
    