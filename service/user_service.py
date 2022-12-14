import bcrypt
import jwt
from datetime import datetime, timedelta

jwtExpireTime=  timedelta(seconds=600)

class UserService:
    def __init__(self,user_dao,config):
        self.user_dao=user_dao
        self.config=config
        
    def get_user_id_and_password(self,email):
        return self.user_dao.get_user_id_and_password(email)
    
    def create_new_user(self,new_user):
        new_user['hashed_password']=bcrypt.hashpw(
            new_user['password'].encode('utf-8'),bcrypt.gensalt()
        )

        new_user_id=self.user_dao.insert_user(new_user)
        return new_user_id
    
    def login(self,credential):
        email=credential['email']
        password=credential['password']
        user_credential=self.user_dao.get_user_id_and_password(email)
        authorized=user_credential and bcrypt.checkpw(password.encode('utf-8'),user_credential['hashed_password'].encode('utf-8'))
        return authorized

    def generate_access_token(self,user_id):
        payload={
            'user_id':user_id,
            'exp':datetime.utcnow()+jwtExpireTime,
            'iat':datetime.utcnow()
        }
        
        token=jwt.encode(payload,self.config['JWT_SECRET_KEY'],'HS256')
        return token
    
    def get_user_info(self,user_id):
        return self.user_dao.get_user_info(user_id)