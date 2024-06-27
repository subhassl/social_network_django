# Social Network Django App

This is a Django based social network application. It provides APIs for user authentication, search, and friend management functionalities.

## APIs

The following APIs are exposed by this application:

- Login: Authenticates a user and returns a token upon successful login.
- Signup: Creates a new user account.
- Search: Searches for users based on a keyword.
- Send Friend Request: Sends a friend request to another user.
- Accept Friend Request: Accepts a pending friend request.
- Reject Friend Request: Rejects a pending friend request.
- List Friends: Retrieves a list of the authenticated user's friends.
- List Pending Requests: Retrieves a list of pending friend requests sent to or received by the authenticated user.

Postman collections is available in the repository.

## Usage

This project utilizes a .env file to store sensitive configuration details like the secret key.

Steps to crate the .env file:

1. Create a file named .env in the root directory of the project (where manage.py resides).
2. Add your secret key to the .env file in the following format:

```
SECRET_KEY="your_secret_key_here"
```

### Command to start the Django server

```
$ docker-compose up --build
```

### Command to crearte superuser

```
$ docker-compose run web python manage.py createsuperuser
```
