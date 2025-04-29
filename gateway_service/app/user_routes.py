import os
import requests
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse

user_api = Namespace("users", description="User related endpoints")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
USER_SERVICE_PUBLIC_URL = os.getenv("USER_SERVICE_PUBLIC_URL")


login_model = user_api.model("Login", {
    "email": fields.String(required=True, description="Your Email"),
    "password": fields.String(required=True, description="Your Password")
})

signup_model = user_api.model("Signup", {
    "email": fields.String(required=True, description="Your Email"),
    "password": fields.String(required=True, description="Your Password")
})

refresh_model = user_api.model("Refresh", {
    "refresh": fields.String(required=True, description="Refresh token")
})


complete_profile_parser = reqparse.RequestParser()
complete_profile_parser.add_argument('first_name', type=str, required=False, location='form')
complete_profile_parser.add_argument('last_name', type=str, required=False, location='form')
complete_profile_parser.add_argument('profile_photo', type='file', required=False, location='files')


def host_address_to_public(response_json:dict, key:str):
    if response_json.get(key, None):
        response_json[key] = response_json[key].replace(USER_SERVICE_URL, USER_SERVICE_PUBLIC_URL)
    
    return response_json


@user_api.route("/login")
class Login(Resource):
    
    @user_api.expect(login_model)
    def post(self):
        
        login_data = request.get_json()
        
        try:
            response = requests.post(url=f"{USER_SERVICE_URL}/api/token/", json=login_data)
            
            if response.ok:
                return response.json(), response.status_code
            
            else:
                return {"message": "Login failed", "error": response.json()}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


@user_api.route("/login/refresh")
class RefreshToken(Resource):
    
    @user_api.expect(refresh_model)
    def post(self):
        
        access_token = request.headers.get("Authorization")
        headers = {
            "Authorization": access_token
        }

        refresh_data = request.get_json()
        
        try:
            response = requests.post(url=f"{USER_SERVICE_URL}/api/token/refresh/", json=refresh_data, headers=headers)
            
            if response.ok:
                return response.json(), response.status_code
            
            else:
                return {"message": "Refreshing token failed", "error": response.json()}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


@user_api.route("/signup")
class Signup(Resource):
    
    @user_api.expect(signup_model)
    def post(self):
        
        signup_data = request.get_json()

        try:
            response = requests.post(url=f"{USER_SERVICE_URL}/api/signup/", json=signup_data)
            
            if response.ok:
                return response.json(), response.status_code
            
            else:
                return {"message": "Signup failed", "error": response.json()}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500
        

@user_api.route("/user-info")
class UserInfo(Resource):
    
    def get(self):
        
        access_token = request.headers.get("Authorization")
        headers = {
            "Authorization": access_token
        }

        try:
            response = requests.get(url=f"{USER_SERVICE_URL}/api/user-info/", headers=headers)
            
            if response.ok:
                result = response.json()
                
                result = host_address_to_public(result, "profile_photo")
                
                return result, response.status_code

            else:
                return {"message": "Operation failed", "error": response.json()}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


@user_api.route("/complete-profile")
class CompleteProfile(Resource):
    
    @user_api.expect(complete_profile_parser)
    @user_api.doc(consumes=["multipart/form-data"])
    def post(self):
        
        access_token = request.headers.get("Authorization")
        
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        profile_photo = request.files.get("profile_photo")
        
        files = {'profile_photo': (profile_photo.filename, profile_photo.stream, profile_photo.mimetype)} if profile_photo else None
        data = {
            "first_name": first_name,
            "last_name": last_name
        }
        
        headers = {
            "Authorization": access_token
        }
        
        try:
            response = requests.put(url=f"{USER_SERVICE_URL}/api/complete-profile/", data=data, files=files, headers=headers)
            
            if response.ok:
                result = response.json()
                result = host_address_to_public(result, "profile_photo")
                
                return result, response.status_code
            
            else:
                return {"message": "Profile completion failed", "error": response.json()}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500
