from flask import g,current_app,request
from functools import wraps
import jwt

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kargs):
        access_token=request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload=jwt.decode(access_token,current_app.config['JWT_SECRET_KEY'],'HS256')
            except:
                return '유효하지 않은 토큰입니다!',401
            if 'user_id' not in payload and type(payload['user_id']) !=type(1):
                return '필수정보가 없는 토큰입니다!',401
        else:
            return '토큰이 존재하지 않습니다.',401

        g.user_id=payload['user_id']
        return f(*args,**kargs)
    return decorated_function