from libgravatar import Gravatar
from sqlalchemy.orm import Session

from fastapi_app.src.database.models import User, Photo
from fastapi_app.src.schemas import UserModel, ProfileStatusUpdate
from fastapi_app.src.services.auth import auth_service


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by their email.

    :param email: The email address of the user.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user object if found, otherwise None.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()

async def get_user_by_username(username: str, db: Session) -> User:
    """
    Retrieves a user by their username.

    :param username: The username of the user.
    :type username: str
    :param db: The database session.
    :type db: Session
    :return: The user object if found, otherwise None.
    :rtype: User
    """
    return db.query(User).filter(User.username == username).first()

async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The user registration details.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user object.
    :rtype: User
    :raises Exception: If an error occurs while fetching the Gravatar image.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
        
    if db.query(User).count() == 0:
        role = "admin"
    else:
        role = "user"
        
    new_user = User(**body.dict(), avatar = avatar, role = role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user.

    :param user: The user object.
    :type user: User
    :param token: The new refresh token, or None to clear it.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms a user's email address.

    :param email: The email address to be confirmed.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar URL for a user.

    :param email: The email address of the user.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user object.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

async def get_profile(username: str, db: Session):
    """
    Retrieve the profile information for a given username.

    :param username: The username of the user whose profile is to be retrieved.
    :type username: str
    :param db: The database session used to query the user information.
    :type db: Session
    :return: A dictionary containing the user's profile information or None if the user does not exist.
    :rtype: dict or None
    """
    user_information = db.query(User).filter(User.username==username).first()
    if not user_information:
        return None
    amount_of_user_photos = db.query(Photo).filter(Photo.user_id==user_information.id).count()
    profile_information = {
                            'username':     user_information.username,
                            'avatar':       user_information.avatar,
                            'created_at':   user_information.created_at,
                            'email':        user_information.email,
                            'role':         user_information.role,
                            'photo_amount': amount_of_user_photos
    }
    return profile_information

async def ban_user(username: str, current_user: User, db: Session):
    """
    Ban a user from the system.

    This function bans a user by deleting their record from the database.
    Only users with the 'admin' role are allowed to perform this action.

    :param username: The username of the user to be banned.
    :type username: str
    :param current_user: The user performing the ban action.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The banned user object if the operation was successful, otherwise None.
    :rtype: User or None
    """
    if current_user.role!="admin":
        return None
    user = db.query(User).filter(User.username==username).first()
    db.delete(user)
    db.commit()
    return user

async def update_user_profile(username: str,body: ProfileStatusUpdate, current_user: User, db: Session):
    """
    Update a user's profile.

    This function allows the current user to update their profile information if the username matches.

    :param username: The username of the user whose profile is being updated.
    :type username: str
    :param body: The profile status update data.
    :type body: ProfileStatusUpdate
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session dependency.
    :type db: Session
    :return: The updated user profile or None if the username does not match the current user.
    :rtype: User or None
    """
    if current_user.username!=username:
        return None
    user = db.query(User).filter(User.username==username).first()
    if user:
        if body.username: user.username=body.username
        if body.password: user.password=auth_service.get_password_hash(body.password)
        db.commit()
    return user

async def get_current_user_profile(user: User, db: Session):
    """
    Retrieve the current user's profile information.

    This function fetches the profile information of the current authenticated user,
    including the number of photos they have uploaded.

    :param user: The current authenticated user.
    :type user: User
    :param db: The database session dependency.
    :type db: Session
    :return: A dictionary containing the user's profile information.
    :rtype: dict
    """
    amount_of_user_photos = db.query(Photo).filter(Photo.user_id==user.id).count()
    profile_information = {
                            'username':     user.username,
                            'avatar':       user.avatar,
                            'created_at':   user.created_at,
                            'email':        user.email,
                            'role':         user.role,
                            'photo_amount': amount_of_user_photos
    }
    return profile_information