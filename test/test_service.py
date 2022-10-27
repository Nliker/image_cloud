import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import pytest
import bcrypt
import jwt
from unittest import mock

from model import ImageDao,UserDao
from service import ImageService,UserService
from sqlalchemy import create_engine,text
import config

database=create_engine(config.test_config['DB_URL'],encoding='utf-8',max_overflow=0)

@pytest.fixture
def user_service():
    return UserService(UserDao(database),config.test_config)
@pytest.fixture
def image_service():
    return ImageService(ImageDao(database),config.test_config)

def setup_function():
    print("======teardown_function======")
    print("테이블 초기화중")
    database.execute(text("""
        set foreign_key_checks=0
    """))
    database.execute(text("""
        truncate users
    """))
    database.execute(text("""
        truncate images
    """))
    database.execute(text("""
        set foreign_key_checks=1
    """))
    print("테이블 초기화 완료!!!")
    print("==========================")
    print("======setup function======")
    print("데이터베이스 저장중")

    hashed_password=bcrypt.hashpw(
        b"test",
        bcrypt.gensalt()
    )
    
    new_user={
        'id':1,
        'name':'test1',
        'email':'test1@naver.com',
        'profile':'testuser1',
        'hashed_password':hashed_password
    }
    
    database.execute(text("""
        insert into users (
            id,name,email,profile,hashed_password
        ) values (
            :id,:name,:email,:profile,:hashed_password
        )
    """),new_user)
    
    new_images=[{
        'id':1,
        'user_id':1,
        'link':f"{config.test_config['IMAGE_URL']}/IMG_0582.JPG"
    },{
        'id':2,
        'user_id':1,
        'link':f"{config.test_config['IMAGE_URL']}/IMG_0626.JPG"
    }]
    
    database.execute(text("""
        insert into images (
            id,user_id,link
        ) values (
            :id,:user_id,:link
        )
    """),new_images)

    print("샘플 데이터 저장 성공!")
    print("==========================")

def teardown_function():
    print("======teardown_function======")
    print("테이블 초기화중")
    database.execute(text("""
        set foreign_key_checks=0
    """))
    database.execute(text("""
        truncate users
    """))
    database.execute(text("""
        truncate images
    """))
    database.execute(text("""
        set foreign_key_checks=1
    """))
    print("테이블 초기화 완료!!!")
    print("==========================")
    
def get_user(user_id):
    row=database.execute(text("""
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
        'profile':row['profile']
    } if row else None
def get_image(image_id):
    row=database.execute(text("""
        select
        id,
        user_id,
        link
        from images
        where id=:image_id    
    """),{'image_id':image_id}).fetchone()
    return {
        'id':row['id'],
        'user_id':row['user_id'],
        'link':row['link'],
    } if row else None
    
def test_get_user_id_and_password(user_service):
    user_credential=user_service.get_user_id_and_password(email='test1@naver.com')
    assert user_credential and user_credential['id']==1
    
def test_create_new_user(user_service):
    new_user={
        'name':'test2',
        'profile':'test2user',
        'email':'test2@naver.com',
        'password':'test'
    }
    new_user_id=user_service.create_new_user(new_user)
    assert new_user_id and new_user_id==2
    
    created_new_user=get_user(new_user_id)
    assert created_new_user=={
        'id':new_user_id,
        'name':new_user['name'],
        'email':new_user['email'],
        'profile':new_user['profile']
    }
def test_login(user_service):
    credential={'email':'test1@naver.com','password':'test'}
    authorized=user_service.login(credential)
    assert authorized

def test_generate_access_token(user_service):
    user_id=1
    token=user_service.generate_access_token(user_id)
    decoded_payload=jwt.decode(token,config.test_config['JWT_SECRET_KEY'],'HS256')

    assert decoded_payload['user_id']==user_id

def test_save_image(image_service):
    image=mock.Mock()
    filename="test.png"
    user_id=1
    
    new_image_id=image_service.save_image(image,filename,user_id)
    new_image_info=get_image(image_id=new_image_id)

    assert new_image_info=={
        'id':new_image_id,
        'user_id':1,
        'link':f"{config.test_config['IMAGE_URL']}/{filename}"
    }
    
def test_get_user_image_links(image_service):
    user_id=1
    image_links=image_service.get_user_image_links(user_id)
    
    assert image_links==[
        {
            'id':1,
            'link':f"{config.test_config['IMAGE_URL']}/IMG_0582.JPG"
        },{
            'id':2,
            'link':f"{config.test_config['IMAGE_URL']}/IMG_0626.JPG"
        }
    ]
    
def test_get_image_info(image_service):
    image_id=1
    
    image_info=image_service.test_get_image_info(image_id)
    assert image_info==get_image(image_id)
    