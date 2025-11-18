from database import SessionLocal, User, create_db_and_tables
from auth import get_password_hash

create_db_and_tables()

db = SessionLocal()
try:
    username = 'GameBros'
    email = 'gamebros@gmail.com'
    full_name = 'Game Bros'
    password = '123456'

    # check existing
    if db.query(User).filter(User.username == username).first():
        print('username exists')
    if db.query(User).filter(User.email == email).first():
        print('email exists')

    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print('created', db_user.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
