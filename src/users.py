from typing import Optional
from db_object import Object


class User(Object):
    table = 'users'

    def __init__(self, id: Optional[int] = None, active: Optional[bool] = None) -> None:
        self.id = id
        self.active = active


class Profile(Object):
    table = 'profiles'

    def __init__(self,
                 id: Optional[int] = None,
                 name: Optional[str] = None,
                 age: Optional[int] = None,
                 about: Optional[str] = None,
                 bio: Optional[str] = None,
                 prefs: Optional[str] = None) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.about = about
        self.bio = bio
        self.prefs = prefs
