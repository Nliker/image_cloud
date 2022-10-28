from sqlalchemy import text

class ImageDao:
    def __init__(self,database):
        self.db=database
    
    def insert_image(self,user_id,link,public):
        return self.db.execute(text("""
            insert into images(
                link,
                user_id,
                public
            ) values (
                :link,:user_id,:public
            )
        """),{'user_id':user_id,'link':link,'public':public}).lastrowid
    
    #유저의 사진 목록들을 get 요청시 처리하기 위함

    def get_image_links(self,start,end):
        rows=self.db.execute(text("""
            select
            id,
            link
            from images
            where public=:public
            order by id
            limit :start,:end
        """),{'start':start,'end':end,'public':1}).fetchall()

        data=[{'id':row['id'],'link':row['link']} for row in rows]

        return data
    
    def get_image_links_by_user_id(self,user_id,start,end,public):
        rows=self.db.execute(text("""
            select 
            id,
            link
            from images
            where user_id=:user_id and public=:public
            limit :start,:end
            """),{'user_id':user_id,'start':start,'end':end,'public':public}).fetchall()
        
        data=[{'id':row['id'],'link':row['link']} for row in rows]
        
        return data
    
    #사진의 링크를 get요청시 처리하기 위함
    def get_image_link_by_image_id(self,image_id):
        row=self.db.execute(text("""
            select
            id,
            link,
            user_id 
            from images
            where id=:image_id
            """),{'image_id':image_id}).fetchone()
        
        return {
            'id':row['id'],
            'link':row['link'],
            'user_id':row['user_id']
        } if row else None
           