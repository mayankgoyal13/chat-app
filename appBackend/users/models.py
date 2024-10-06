# # users/models.py

# from mongoengine import Document, StringField, EmailField, DateTimeField, signals
# from mongoengine.queryset import QuerySet
# import datetime
# import bcrypt

# class CustomUser(Document):
#     username = StringField(required=True, unique=True, max_length=50)
#     email = EmailField(required=True, unique=True)
#     first_name = StringField(required=True, max_length=50)
#     last_name = StringField(required=True, max_length=50)
#     phone_number = StringField(required=True, unique=True, max_length=15)
#     password = StringField(required=True, min_length=8)
#     created_at = DateTimeField(default=datetime.datetime.utcnow)

#     meta = {
#         'collection': 'users',
#         'indexes': ['username', 'email', 'phone_number']
#     }

#     def set_password(self, raw_password):
#         self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     def check_password(self, raw_password):
#         return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "username": self.username,
#             "email": self.email,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "phone_number": self.phone_number,
#             "created_at": self.created_at.isoformat()
#         }
#     @property
#     def is_authenticated(self):
#         return True

# # Automatically hash passwords before saving
# def pre_save_user(sender, document, **kwargs):
#     if not document.password.startswith('$2b$'):
#         document.set_password(document.password)

# signals.pre_save.connect(pre_save_user, sender=CustomUser)


# users/models.py

# from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, signals
# import datetime
# from mongoengine.queryset import QuerySet
# import bcrypt

# class CustomUser(Document):
#     username = StringField(required=True, unique=True, max_length=50)
#     email = EmailField(required=True, unique=True)
#     first_name = StringField(required=True, max_length=50)
#     last_name = StringField(required=True, max_length=50)
#     phone_number = StringField(required=True, unique=True, max_length=15)
#     password = StringField(required=True, min_length=8)
#     created_at = DateTimeField(default=datetime.datetime.utcnow)
#     last_seen = DateTimeField(default=datetime.datetime.utcnow)  # Track when the user was last seen
#     is_online = BooleanField(default=False)  # Indicates if the user is currently online

#     meta = {
#         'collection': 'users',
#         'indexes': ['username', 'email', 'phone_number']
#     }

#     def set_password(self, raw_password):
#         self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     def check_password(self, raw_password):
#         return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "username": self.username,
#             "email": self.email,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "phone_number": self.phone_number,
#             "created_at": self.created_at.isoformat(),
#             "last_seen": self.last_seen.isoformat(),  # Include last_seen in JSON representation
#             "is_online": self.is_online  # Include is_online in JSON representation
#         }
    
#     @property
#     def is_authenticated(self):
#         return True

# # Automatically hash passwords before saving
# def pre_save_user(sender, document, **kwargs):
#     if not document.password.startswith('$2b$'):
#         document.set_password(document.password)

# signals.pre_save.connect(pre_save_user, sender=CustomUser)


# from mongoengine import Document, StringField, EmailField, DateTimeField, signals, BooleanField
# import datetime
# import bcrypt

# class CustomUser(Document):
#     username = StringField(required=True, unique=True, max_length=50)
#     email = EmailField(required=True, unique=True)
#     first_name = StringField(required=True, max_length=50)
#     last_name = StringField(required=True, max_length=50)
#     phone_number = StringField(required=True, unique=True, max_length=15)
#     password = StringField(required=True, min_length=8)
#     created_at = DateTimeField(default=datetime.datetime.utcnow)
#     last_seen = DateTimeField(default=datetime.datetime.utcnow)  # New field
#     is_online = BooleanField(default=False)  # New field

#     meta = {
#         'collection': 'users',
#         'app_label' : 'my_app',
#         'indexes': ['username', 'email', 'phone_number']
#     }

#     def set_password(self, raw_password):
#         self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     def check_password(self, raw_password):
#         return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "username": self.username,
#             "email": self.email,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "phone_number": self.phone_number,
#             "created_at": self.created_at.isoformat(),
#             "last_seen": self.last_seen.isoformat(),  # Include last_seen in JSON
#             "is_online": self.is_online  # Include is_online in JSON
#         }
#     @property
#     def is_authenticated(self):
#         return True

# # Automatically hash passwords before saving
# def pre_save_user(sender, document, **kwargs):
#     if not document.password.startswith('$2b$'):
#         document.set_password(document.password)

# signals.pre_save.connect(pre_save_user, sender=CustomUser)



from mongoengine import Document, StringField, EmailField, DateTimeField, signals, BooleanField
import datetime
import bcrypt
from chat.models import Conversation

class CustomUser(Document):
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    phone_number = StringField(required=True, unique=True, max_length=15)
    password = StringField(required=True, min_length=8)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    last_seen = DateTimeField(default=datetime.datetime.utcnow)
    is_online = BooleanField(default=False)

    meta = {
        'collection': 'users',
        'app_label': 'my_app',
        'indexes': ['username', 'email', 'phone_number']
    }

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "is_online": self.is_online
        }

    @property
    def is_authenticated(self):
        return True

    # Method to retrieve conversations the user is a participant in
    def get_conversations(self):
        return Conversation.objects.filter(participants__in=[self])


# Automatically hash passwords before saving
def pre_save_user(sender, document, **kwargs):
    if not document.password.startswith('$2b$'):
        document.set_password(document.password)

signals.pre_save.connect(pre_save_user, sender=CustomUser)
