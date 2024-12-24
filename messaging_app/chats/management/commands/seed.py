import uuid
from django.core.management.base import BaseCommand
from chats.models import CustomUser, Conversation, Message

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.seed_users()
        self.seed_conversations()
        self.seed_messages()
        self.stdout.write('Data seeded successfully.')

    def seed_users(self):
        users_data = [
            {'username': 'guest1', 'first_name': 'Guest', 'last_name': 'One', 'email': 'guest1@example.com', 'role': 'guest'},
            {'username': 'host1', 'first_name': 'Host', 'last_name': 'One', 'email': 'host1@example.com', 'role': 'host'},
            {'username': 'admin1', 'first_name': 'Admin', 'last_name': 'One', 'email': 'admin1@example.com', 'role': 'admin'},
        ]
        for user_data in users_data:
            user, created = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'user_id': uuid.uuid4(),
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'password_hash': 'hashed_password',  # Replace with actual hashed password
                    'role': user_data['role'],
                }
            )
            if created:
                self.stdout.write(f'Created user: {user.username}')

    def seed_conversations(self):
        users = CustomUser.objects.all()
        if users.count() < 2:
            self.stdout.write('Not enough users to create conversations.')
            return

        conversation, created = Conversation.objects.get_or_create()
        conversation.participants.set(users[:2])
        conversation.save()
        if created:
            self.stdout.write(f'Created conversation with ID: {conversation.conversation_id}')

    def seed_messages(self):
        conversations = Conversation.objects.all()
        if not conversations.exists():
            self.stdout.write('No conversations found to create messages.')
            return

        conversation = conversations.first()
        sender = conversation.participants.first()
        message, created = Message.objects.get_or_create(
            conversation=conversation,
            sender=sender,
            defaults={
                'message_id': uuid.uuid4(),
                'message_body': 'Hello, this is a test message.',
            }
        )
        if created:
            self.stdout.write(f'Created message with ID: {message.message_id}')
