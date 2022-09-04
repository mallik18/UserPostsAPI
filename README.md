(https://github.com/mallik18/UserPostsAPI/interrogate_badge.svg?branch=main)

# UserPostsAPI

Developing an API


## API includes:
- Authentication
- CRUD Operations
- Validation
- Documentation

## Tech Stack:

	Language: Python

	Framework: FastAPI	

	Database:
		SQL - PostgreSQL
		ORM(Object Relation Mapping) - SQLAlchemy
		Database Migration tools     - Alembic
	
	API Testing:
		POSTMAN
	Others:
		NGINX
		SSL
		Dockers
		CI/CD: Github Workflow
	
	Deployment:
		- Ubuntu
		- Heroku - Free	


## API URL Endpoints:
	POSTS:
		- GET= /posts/  	    : Get Posts
		- POST= /posts/		    : Create Posts
		- GET= /posts/{id}	    : Get Post
		- PUT= /posts/{id}	    : Update Post
		- DELETE= /posts/{id}	: Delete Post

	Users:
		- POST= /users/		    : Create User
		- GET= /users/{id}	    : Get User

	Authentication:
		- POST= /login/		    : Login and Authentication

	Vote:
		- POST= /vote/		    : Vote on post

	Default:
		- GET= /			    : main page

	Docs:
		- /redoc or /docs	    : Documentation
