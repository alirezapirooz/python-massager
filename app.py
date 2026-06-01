import csv
import datetime
from pathlib import Path


class SocialMediaApp:
    def __init__(self):
        self.users_file = "users.csv"
        self.posts_file = "posts.csv"
        self.messages_file = "messages.csv"
        self.friends_file = "friends.csv"
        self.requests_file = "friend_requests.csv"

        # create files if not exist
        if not Path(self.users_file).exists():
            with open(self.users_file, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "username",
                        "password",
                        "first_name",
                        "last_name",
                        "city",
                        "gender",
                        "age"
                    ]
                )
                writer.writeheader()

        if not Path(self.posts_file).exists():
            with open(self.posts_file, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "username",
                        "text",
                        "date"
                    ]
                )
                writer.writeheader()

        if not Path(self.messages_file).exists():
            with open(self.messages_file, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "sender",
                        "receiver",
                        "message",
                        "date"
                    ]
                )
                writer.writeheader()

        if not Path(self.friends_file).exists():
            with open(self.friends_file, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "user1",
                        "user2"
                    ]
                )
                writer.writeheader()

        if not Path(self.requests_file).exists():
            with open(self.requests_file, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "sender",
                        "receiver"
                    ]
                )
                writer.writeheader()

        self.users = self.load_users()
        self.posts = self.load_posts()
        self.messages = self.load_messages()

        self.friends = self.load_friends()
        self.friend_requests = self.load_requests()

        if "admin" not in self.users:
            self.users["admin"] = {
                "password": "admin",
                "first_name": "admin",
                "last_name": "user",
                "city": "ny",
                "gender": "male",
                "age": "1"
            }

            self.save_users()

        self.run()

    

    def load_friends(self):
        friends = set()

        with open(self.friends_file, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                friends.add(
                    frozenset([
                        row["user1"],
                        row["user2"]
                    ])
                )

        return friends

    def save_friends(self):
        with open(self.friends_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["user1", "user2"]
            )

            writer.writeheader()

            for fr in self.friends:
                u1, u2 = list(fr)

                writer.writerow({
                    "user1": u1,
                    "user2": u2
                })

    def load_requests(self):
        with open(self.requests_file, "r", newline="") as f:
            return list(csv.DictReader(f))

    def save_requests(self):
        with open(self.requests_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["sender", "receiver"]
            )

            writer.writeheader()
            writer.writerows(self.friend_requests)

    

    def load_users(self):
        users = {}

        with open(self.users_file, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                users[row["username"]] = {
                    "password": row["password"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "city": row["city"],
                    "gender": row["gender"],
                    "age": row["age"]
                }

        return users

    def save_users(self):
        with open(self.users_file, "w", newline="") as f:
            fieldnames = [
                "username",
                "password",
                "first_name",
                "last_name",
                "city",
                "gender",
                "age"
            ]

            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for u, data in self.users.items():
                writer.writerow({
                    "username": u,
                    **data
                })

    def load_posts(self):
        posts = []

        with open(self.posts_file, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                row["date"] = datetime.datetime.fromisoformat(
                    row["date"]
                )

                posts.append(row)

        return posts

    def save_posts(self):
        with open(self.posts_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "username",
                    "text",
                    "date"
                ]
            )

            writer.writeheader()

            for p in self.posts:
                writer.writerow({
                    "username": p["username"],
                    "text": p["text"],
                    "date": p["date"].isoformat()
                })

    def load_messages(self):
        with open(self.messages_file, "r", newline="") as f:
            return list(csv.DictReader(f))

    def save_messages(self):
        with open(self.messages_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["sender", "receiver", "message", "date"]
            )
            writer.writeheader()
            writer.writerows(self.messages)

    

    def run(self):
        while True:
            print("\n1) Login")
            print("2) Sign up")
            print("3) Exit")

            choice = input(">> ").strip()

            if choice == "1":
                self.login()

            elif choice == "2":
                self.signup()

            elif choice == "3":
                self.save_users()
                self.save_posts()
                self.save_messages()
                self.save_friends()
                self.save_requests()
                break

    

    def user_menu(self, user):
        while True:
            print("\n1) Post")
            print("2) View posts")
            print("3) Send message")
            print("4) View messages")
            print("5) Friend requests")
            print("6) Send friend request")
            print("7) Logout")

            choice = input(">> ").strip()

            if choice == "1":
                self.create_post(user)

            elif choice == "2":
                self.view_posts()

            elif choice == "3":
                self.send_message(user)

            elif choice == "4":
                self.view_messages(user)

            elif choice == "5":
                self.handle_requests(user)

            elif choice == "6":
                self.send_friend_request(user)

            elif choice == "7":
                break

    

    def send_friend_request(self, user):
        target = input("send request to: ").lower().strip()

        if target not in self.users:
            print("user not found")
            return

        if target == user:
            print("cannot add yourself")
            return

        if frozenset([user, target]) in self.friends:
            print("already friends")
            return

        self.friend_requests.append({
            "sender": user,
            "receiver": target
        })

        self.save_requests()
        print("request sent")

    def handle_requests(self, user):
        pending = [r for r in self.friend_requests if r["receiver"] == user]

        if not pending:
            print("no requests")
            return

        for i, r in enumerate(pending):
            print(f"{i}) from {r['sender']}")

        idx = input("accept index: ").strip()

        if idx == "":
            return

        try:
            idx = int(idx)
            req = pending[idx]

            self.friends.add(frozenset([req["sender"], req["receiver"]]))
            self.friend_requests.remove(req)

            self.save_friends()
            self.save_requests()

            print("friend added")

        except:
            print("invalid")

    

    def send_message(self, sender):
        friend_list = [
            list(f - {sender})[0]
            for f in self.friends
            if sender in f
        ]

        if not friend_list:
            print("you have no friends")
            return

        for i, f in enumerate(friend_list):
            print(f"{i}) {f}")

        try:
            idx = int(input("choose friend: "))
            receiver = friend_list[idx]
        except:
            print("invalid")
            return

        msg = input("message: ")

        self.messages.append({
            "sender": sender,
            "receiver": receiver,
            "message": msg,
            "date": datetime.datetime.now().isoformat()
        })

        self.save_messages()
        print("sent!")

    

    def create_post(self, user):
        text = input("text: ")

        self.posts.append({
            "username": user,
            "text": text,
            "date": datetime.datetime.now()
        })

        self.save_posts()
        print("Posted!")

    def view_posts(self):
        for p in sorted(self.posts, key=lambda x: x["date"], reverse=True):
            print(f"{p['username']}: {p['text']} ({p['date']})")

    

    def signup(self):
        username = input("username: ").lower().strip()

        if username in self.users:
            print("User exists")
            return

        self.users[username] = {
            "password": input("password: "),
            "first_name": input("first name: "),
            "last_name": input("last name: "),
            "city": input("city: "),
            "gender": input("gender: "),
            "age": input("age: ")
        }

        self.save_users()
        print("Account created!")

    def login(self):
        username = input("username: ").lower().strip()
        password = input("password: ")

        if username in self.users and self.users[username]["password"] == password:
            print(f"Welcome {username}")
            self.user_menu(username)
        else:
            print("Invalid login")


if __name__ == "__main__":
    SocialMediaApp()