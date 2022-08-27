import app.api.endpoints as e
from app.api import app_api


app_api.add_resource(e.Login, "/users/sign_in")
app_api.add_resource(e.ActiveUser, "/users/active")