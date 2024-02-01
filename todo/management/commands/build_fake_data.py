from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker

from ...models import Todo

User = get_user_model()


class Command(BaseCommand):
    help = "build fake uesr and todo"

    def add_arguments(self, parser):
        parser.add_argument(
            "user_count",
            type=int,
            help="count of fake users you want to be created",
        )
        parser.add_argument(
            "todo_count",
            type=int,
            help="count of fake todos you want to be created",
        )

    def handle(self, *args, **kwargs):
        user_count = kwargs["user_count"]
        todo_count = kwargs["todo_count"]

        self.stdout.write(self.style.SUCCESS(f"building {user_count} users..."))
        self.build_fake_user(user_count)

        self.stdout.write(self.style.SUCCESS(f"building {todo_count} todo..."))
        self.build_fake_todo(todo_count)

        self.stdout.write(self.style.SUCCESS("fake data built successfully."))

    def build_fake_user(self, user_count):
        for i in range(user_count):
            fake = Faker()
            username = fake.user_name() + str(i)
            email = fake.email()
            password = get_random_string(length=12)
            User.objects.create_user(username=username, email=email, password=password)  # type: ignore

    def build_fake_todo(self, todo_count):
        for _ in range(todo_count):
            fake = Faker()
            title = fake.word()
            details = fake.text()
            user = User.objects.order_by("?").first()

            Todo.objects.create(
                title=title,
                details=details,
                user=user,
            )
