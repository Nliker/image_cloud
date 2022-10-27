import bcrypt
import pytest
import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import config

from model import UserDao,ImageDao
from sqlalchemy import create_engine,text

database=create_engine(config.test_config['DB_URL'],encoding='utf-8',max_overflow=0)

@pytest.fixture
def user_dao():
    return UserDao(database)

@pytest.fixture
def image_dao():
    return ImageDao(database)

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
        'link':f"{config.test_config['IMAGE_URL']}/1"
    },{
        'id':2,
        'user_id':1,
        'link':f"{config.test_config['IMAGE_URL']}/2"
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

def get_image(image_id):
    row=database.execute(text("""
        select id,user_id,link
        from images
        where id=:image_id
    """),{'image_id':image_id}).fetchone()

    return {
        'id':row['id'],
        'user_id':row['user_id'],
        'link':row['link'],
    } if row else None

def get_user(user_id):
    row=database.execute(text("""
        select id,name,email,profile
        from users
        where id=:user_id
    """),{'user_id':user_id}).fetchone()

    return {
        'id':row['id'],
        'name':row['name'],
        'email':row['email'],
        'profile':row['profile']
    } if row else None
    

def test_insert_user(user_dao):
    hashed_password=bcrypt.hashpw(
        b"test",
        bcrypt.gensalt()
    )
    new_user={
        'name':'test2',
        'email':'test2@naver.com',
        'profile':'testuser2',
        'hashed_password':hashed_password
    }
    assert user_dao.insert_user(user=new_user)==2

    inserted_user=get_user(user_id=2)
    assert inserted_user=={
        'id':2,
        'name':'test2',
        'email':'test2@naver.com',
        'profile':'testuser2'
    }
    
def test_get_user_id_and_password(user_dao):
    email="test1@naver.com"
    user_credential=user_dao.get_user_id_and_password(email=email)
    assert ('id' in user_credential) and ('hashed_password' in user_credential)
    assert user_credential['id']==1

    password="test"
    
    authorized=bcrypt.checkpw(password.encode('UTF-8'),user_credential['hashed_password'].encode('UTF-8'))
    
    assert authorized ==True

def test_get_user_info(user_dao):
    user_info=user_dao.get_user_info(1)
    
    assert user_info=={
        'id':1,
        'name':'test1',
        'email':'test1@naver.com',
        'profile':'testuser1'
    }

def test_insert_image(image_dao):
    user_id=1
    test_link="http://test.com"
    inserted_image_id=image_dao.insert_image(user_id=user_id,link=test_link)
    
    assert type(inserted_image_id)==type(1)
    
    inserted_image=get_image(inserted_image_id)
    
    assert inserted_image=={
        'id':inserted_image_id,
        'link':test_link,
        'user_id':user_id
    }
    
def test_get_image_link_by_user_id(image_dao):
    user_id=1
    
    user_images=image_dao.get_image_links_by_user_id(user_id=user_id)
    
    assert user_images==[
        {
            'id':1,
            'link':f"{config.test_config['IMAGE_URL']}/1"
        },
        {
            'id':2,
            'link':f"{config.test_config['IMAGE_URL']}/2"
        }
    ]

def test_get_image_link_by_image_id(image_dao):
    image_id=1
    
    image=image_dao.get_image_link_by_image_id(image_id=image_id)
    
    assert image=={
        'id':image_id,
        'link':f"{config.test_config['IMAGE_URL']}/{image_id}",
        'user_id':1
    }
