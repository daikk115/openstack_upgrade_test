from keystoneauth1.identity import v3
from keystoneauth1 import session

from config import *


auth = v3.Password(auth_url=AUTH_URL,
                    user_domain_name='default',
                    username=USERNAME,
                    password=PASSWORD,
                    project_domain_name='default',
                    project_name=PROJECT_NAME)

session = session.Session(auth=auth)
TOKEN = session.get_token()
PROJECT_ID = session.get_project_id()