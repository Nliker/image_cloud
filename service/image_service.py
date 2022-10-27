import os

class Image_Service:
    def __init__(self,image_dao,config):
        self.image_dao=image_dao
        self.config=config

    #route("/image POST")
    def save_image(self,image,filename,user_id):
        upload_path=self.config['IMAGE_PATH']
        image_path_and_name=f"{upload_path}{filename}"
        image.save(image_path_and_name)

        new_image_id=self.image_dao.insert_image(user_id,link=image_path_and_name)
        return new_image_id

    def get_user_image_links(self,user_id):
        return self.image_dao.get_image_link_by_image_id(user_id)

    def get_image_info(self,image_id):
        return self.image_dao.get_image_link_by_user_id(image_id)