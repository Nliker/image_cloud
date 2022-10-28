from flask import request,send_file,jsonify
import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from auth import login_required,g

def image_router(app,services):
    image_service=services.image_service
    # @app.route("/images",methods=["GET"])
    # @login_required
    # def images():
        
    # @app.route("/image",methods=["POST"])
    # @login_required
    # def image():
        
    #image in files
    @app.route("/user/<int:user_id>/image",methods=["POST"])
    @login_required
    def user_image(user_id):
        current_user_id=g.user_id
        if current_user_id!=user_id:
            return '요청하는 유저와 로그인된 유저가 다릅니다.',401
        if 'image' not in request.files or request.files['image'].filename=='':
            return 'file is missing',404
        
        image=request.files['image']
        
    @app.route("/user/<int:user_id>/images",methods=["GET"])
    def user_images():
        
    @app.route("/image/<int:image_id>",methods=["GET"])
    def image():
        