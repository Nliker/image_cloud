from flask import request,send_file,jsonify
import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from auth import login_required,g
from tool import generate_random_sting

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
        extender=str(image.split('.')[1])
        filename=generate_random_sting(10)+'.'+extender
        result=image_service.save_image(image,filename,user_id)

        return f"{result}이미지를 저장 완료하였습니다.",200

    #회원인 유저들은 모든 사진에 접근 가능
    @app.route("/user/<int:user_id>/images",methods=["GET"])
    @login_required
    def user_images(user_id):
        images_info=image_service.get_user_image_links(user_id)
        return jsonify({'user_id':user_id,'images':images_info}),200
        
    @app.route("/images/<int:image_id>",methods=["GET"])
    @login_required
    def image(image_id):
        image_info=image_service.get_image_info(image_id)
        
        return jsonify(image_info),200
    
    @app.route("/download-image/<int:image_id>",["GET"])
    @login_required
    def download_image(image_id):
        image_info=image_service.get_image_info(image_id)
        image_user_id=image_info['user_id']
        image_path=f"{app.config['IMAGE_PATH']}/{image_user_id}/{image_id}"

        return send_file(image_path),200