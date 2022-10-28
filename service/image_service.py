import os

class ImageService:
    def __init__(self,image_dao,config):
        self.image_dao=image_dao
        self.config=config

    #route("/image POST")
    def save_image(self,image,filename,user_id):
        upload_path=self.config['IMAGE_PATH']
        image_path_and_name=f"{upload_path}/{user_id}/{filename}"
        image.save(image_path_and_name)
        
        link=f"{self.config['IMAGE_URL']}/{filename}"

        new_image_id=self.image_dao.insert_image(user_id,link)
        return new_image_id

    def get_image_links(self,start,end):
        return self.image_dao.get_image_links(start,end)
    
    def get_user_image_links(self,user_id):
        return self.image_dao.get_image_links_by_user_id(user_id)

    def get_image_info(self,image_id):
        return self.image_dao.get_image_link_by_image_id(image_id)