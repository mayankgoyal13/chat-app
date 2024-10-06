# from users.models import CustomUser
# import datetime


# from mongoengine import Document,StringField, DateTimeField, ListField, ReferenceField
# from users.models import CustomUser  # Make sure this import is correct

# class Conversation(Document):
#     participants = ListField(ReferenceField(CustomUser))
#     created_at = DateTimeField(default=datetime.datetime.utcnow)
#     user = ReferenceField(CustomUser)

#     def __str__(self):
#         return f"Conversation between {', '.join([str(user.username) for user in self.participants])}"
    
# class Message(Document):
#     conversation = ReferenceField(Conversation)
#     sender = ReferenceField(CustomUser)  # Removed reverse_delete_rule
#     content = StringField()
#     timestamp = DateTimeField(default=datetime.datetime.utcnow)

#     def __str__(self):
#         return f"Message from {self.sender.username} at {self.timestamp}"


from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
# from users.models import CustomUser  # Ensure the import is correct
import datetime

class Conversation(Document):
    participants = ListField(ReferenceField('CustomUser'))
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"Conversation between {', '.join([str(user.username) for user in self.participants])}"

class Message(Document):
    conversation = ReferenceField(Conversation)
    sender = ReferenceField('CustomUser')
    content = StringField()
    timestamp = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
