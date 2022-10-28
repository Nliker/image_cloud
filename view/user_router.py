from flask import request,jsonify
import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from auth import login_required,g

def image_route(app,services):
    user_service=services.user_service
    
    
    #name,profile,email,password
    @app.route("/sign-up",methods=["POST"])
    def sign_up():
        new_user=request.json
        new_user_id=user_service.create_new_user(new_user)
        created_new_user=user_service.get_user_info(new_user_id)

        return jsonify(created_new_user),200
        
    #email,password
    @app.route("/login",methods=["POST"])
    def login():
        credential=request.json
        authorized=user_service.login(credential)

        if authorized:
            user_credential=user_service.get_user_id_and_password(email=credential['email'])
            token=user_service.generate_access_token(user_id=user_credential['id'])
            return jsonify({'access_token'}),200
        else:
            return '권한이 없습니다.',401
        
    @app.route("/user/<int:user_id>",methods=["GET"])
    def user(user_id):
        user_info=user_service.get_user_info(user_id)
        
        return jsonify(user_info),200
        