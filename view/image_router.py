from flask import request,send_file,jsonify
import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from auth import login_required,g
from tool import generate_random_sting

def image_router(app,services):
    image_service=services.image_service
    
    #start,end(원하는 페이지 만큼 불러오기),public(공용 or 사용)
    @app.route("/images",methods=["GET"])
    @login_required
    def images():
        payload=request.json
        start=payload['start']
        end=payload['end']
        public=payload['public']
        image_links=image_service.get_image_links(start,end)

        return jsonify({'images':image_links}),200
    
    #image in files
    @app.route("/user/<int:user_id>/image",methods=["POST"])
    @login_required
    def user_image(user_id):
        current_user_id=g.user_id
        if current_user_id!=user_id:
            return '요청하는 유저와 로그인된 유저가 다릅니다.',401
        if 'image' not in request.files or request.files['image'].filename=='':
            return 'file is missing',404

        pulbic=request.json['public']
        image=request.files['image']
        
        extender=str(image.split('.')[1])
        filename=generate_random_sting(10)+'.'+extender
        result=image_service.save_image(image,filename,user_id,public)

        return f"{result}이미지를 저장 완료하였습니다.",200

    #회원인 유저는 공용 상태인 사진에 모두 접근 가능
    @app.route("/user/<int:user_id>/images",methods=["GET"])
    @login_required
    def user_images(user_id):
        images_links=image_service.get_user_image_links(user_id)
        return jsonify({'user_id':user_id,'images':images_links}),200
        
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