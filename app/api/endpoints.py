from flask import request
from flask import abort
from flask_restful import (
    Resource,  
    reqparse
)

from app.api.auth import basic_auth, generate_token, token_auth


class Login(Resource):
    decorators = [basic_auth.login_required]
    def get(self):
        user = basic_auth.current_user()
        return {
            "token": user.generate_token()
        }

class ActiveUser(Resource):
    decorators = [token_auth.login_required]
    def get(self):
        user = token_auth.current_user()
        return {
            "id": user.id,
            "uid": user.unique_id,
            "username": user.username,
            "name": user.full_name,
            "display_name": user.get_name(),
            "email": user.email
        }




# class GetAllAnnouncements(Resource):
#     def get(self):
#         """get 
        
#         Get all the announcements, in a JSON form. Then in static site,
#         we will add a parser to render like in achievements.
#         """
#         # return jsonify.
#         return_obj = []
#         for ann in Announcement.get_all():
#             return_obj.append({
#                 # "author_username" : ann.author.username,
#                 "title" : ann.title,
#                 "body" : ann.body,
#                 "timestamp" : ann.timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             })
        
#         return return_obj

# app_api.add_resource(GetAllAnnouncements, "/announcements")