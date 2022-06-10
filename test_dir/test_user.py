import json
import bcrypt

from models import User, Permission
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import pytest


class UserCreateRequest(BaseModel):
    user_account: str
    password: str
    user_name: str
    admin_permission: Permission
    review_permission: bool
    ip_list: List[str]


def test_user_create(test_db_session: Session):
    user_info = {
        "user_account": "test_account",
        "password": "1234",
        "user_name": "test_user",
        "admin_permission": "ADMIN",
        "review_permission": 1,
        "ip_list": [],
    }
    request = UserCreateRequest(**user_info)

    find_user = (
        test_db_session.query(User)
        .filter(User.user_account == request.user_account)
        .first()
    )
    assert find_user is None

    ip_list = json.dumps(request.ip_list, ensure_ascii=False)

    user = User(
        user_name=request.user_name,
        user_account=request.user_account,
        password=bcrypt.hashpw(
            request.password.encode("utf-8"), bcrypt.gensalt()
        ).decode(),
        admin_permission=request.admin_permission,
        review_permission=request.review_permission,
        ip_list=ip_list,
    )
    test_db_session.add(user)
    test_db_session.commit()

    find_user = (
        test_db_session.query(User)
        .filter(User.user_account == request.user_account)
        .first()
    )
    assert find_user is not None
    assert find_user.user_name == request.user_name

    test_db_session.query(User).filter(User.user_id == find_user.user_id).delete(
        synchronize_session="fetch"
    )
    test_db_session.commit()

    find_user = (
        test_db_session.query(User)
        .filter(User.user_account == request.user_account)
        .first()
    )
    assert find_user is None
