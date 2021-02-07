from typing import Optional
from gm_object import Object


class User(Object):
    table = 'users'

    def __init__(self, uid: Optional[int] = None, active: Optional[bool] = None) -> None:
        self.uid = uid
        self.active = active


class Profile(Object):
    table = 'profiles'

    def __init__(self,
                 uid: Optional[int] = None,
                 name: Optional[str] = None,
                 age: Optional[int] = None,
                 status: Optional[str] = None,
                 bio: Optional[str] = None,
                 prefs: Optional[str] = None) -> None:
        self.uid = uid
        self.name = name
        self.age = age
        self.status = status
        self.bio = bio
        self.pref = prefs
