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

def setup_functuon():
    print("======teardown_function======")
    print("테이블 초기화중")
    database.execute(text("""
        set foreign_key_checks=0
    """))
    database.execute(text("""
        truncate users
    """))
    database.execute(text("""
        truncate tweets
    """))
    database.execute(text("""
        truncate users_follow_list
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
        bcrypt.salt()
    )
    
    new_user={
        'id':1,
        'name':'test1',
        'email':'test1@naver.com',
        'profile':'testuser1',
        'hashed_password':hashed_password
    }
    
    database.execute(text("""
        isert into users (
            id,name,email,profile,hashed_password
        ) values (
            :id,:name,:email,:profile,:hashed_password
        )
    """),new_user)
    
    new_image={
        'id':1,
        'link':f"{config.test_config['IMAGE_URL']}/user/1/image/IMG_0626.JPG"
    }
    database.execute(text("""
        insert into images (
            user_id,link
        ) values (
            :user_id,:link
        )
    """),new_image)

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
        truncate tweets
    """))
    database.execute(text("""
        truncate users_follow_list
    """))
    database.execute(text("""
        set foreign_key_checks=1
    """))
    print("테이블 초기화 완료!!!")
    print("==========================")

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