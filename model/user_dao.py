from sqlalchemy import text

class UserDao:
    def __init__(self,database):
        self.db=database
    
    
    def insert_user(self,user):
        return self.db.execute(text("""
            insert into users(
                name,
                email,
                profile,
                hashed_password
            ) values (
                :name,
                :email,
                :profile,
                :hashed_password
            )
        """),user).lastrowid
    def get_user_id_and_password(self,email):
        row=self.db.execute(text("""
            select 
            id,
            hashed_password
            from users
            where email=:email
        """),{'email':email}).fetchone()
        return {
            'id':row['id'],
            'hashed_password':row['hashed_password']
        } if row else None
    
    def get_user_info(self,user_id):
        row=self.db.execute(text("""
            select 
            id,
            name,
            email,
            profile
            from users
            where id=:user_id
        """),{'user_id':user_id}).fetchone()
        
        return {
            'id':row['id'],
            'name':row['name'],
            'email':row['email'],
            'profile':row['profile'],
        } if row else None
        