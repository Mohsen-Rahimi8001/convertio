import os
import requests
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse


media_api = Namespace("media-management", description="Media related endpoints")


MEDIA_SERVICE_URL = os.getenv("MEDIA_SERVICE_URL")
MEDIA_SERVICE_PUBLIC_URL = os.getenv("MEDIA_SERVICE_PUBLIC_URL")


video_upload_parser = reqparse.RequestParser()
video_upload_parser.add_argument('title', type=str, required=False, location='form')
video_upload_parser.add_argument('file', type='file', required=True, location='files')


reverse_model = media_api.model("ReverseVideoInput", {
    "video_id": fields.Integer(required=True, description="ID of the video to reverse")
})


def host_address_to_public(response_json:dict, key:str):
    if response_json.get(key, None):
        response_json[key] = response_json[key].replace(MEDIA_SERVICE_URL, MEDIA_SERVICE_PUBLIC_URL)
    
    return response_json


@media_api.route("/video-upload")
class UploadVideo(Resource):
    
    @media_api.expect(video_upload_parser)
    @media_api.doc(consumes=["multipart/form-data"])
    def post(self):
        
        access_token = request.headers.get("Authorization")
        
        title = request.form.get("title")
        video = request.files.get("file")
        
        video = {"file": (video.filename, video.stream, video.mimetype)} if video else None
        
        data = {
            "title": title,
        }
        
        headers = {
            "Authorization": access_token,
        }
        
        try:
            response = requests.post(url=f"{MEDIA_SERVICE_URL}/api/upload-video/", data=data, files=video, headers=headers)
            
            if response.ok:
                result = response.json()
                result = host_address_to_public(result, "file")
                
                return result, response.status_code
            
            else:
                return {"message": "Video upload failed", "error": response.json()}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


@media_api.route("/user-videos")
class UserVideos(Resource):
    
    def get(self):
        
        access_token = request.headers.get("Authorization")
        headers = {
            "Authorization": access_token,
        }

        try:
            response = requests.get(f"{MEDIA_SERVICE_URL}/api/user-videos/", headers=headers)
            if response.ok:
                result = []
                
                for value in response.json():
                    result.append(host_address_to_public(value, "file"))
                
                return result, response.status_code

            else:
                return {"message": "Operation failed", "error": response.json()}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


@media_api.route("/reverse-video")
class ReverseVideo(Resource):
    
    @media_api.expect(reverse_model)
    def put(self):
        
        access_token = request.headers.get("Authorization")
        headers = {
            "Authorization": access_token,
        }

        data = request.get_json()
        
        video_id = data.get("video_id")
        

        try:
            response = requests.put(f"{MEDIA_SERVICE_URL}/api/reverse-video/{video_id}/", headers=headers)
            if response.ok:
                
                return response.json(), response.status_code

            else:
                return {"message": "Operation failed", "error": response.json()}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Service error", "error": str(e)}, 500


