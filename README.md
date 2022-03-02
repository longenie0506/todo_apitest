# Python Entrance Test - Todo API test

### Library & Framework requirements: 
- Django  
- Django model  
- JWT  
- MySQL  

### Setup:
Host: localhost  
Port: 8000,5432  


After cloning github repo, remember to access into the root directory:

```
cd todo_apitest
```

Run docker image, It will take some time to install dependencies:

```
docker-compose up
```

Initialize DB migration:

```
docker-compose run web python manage.py migrate
```

### Description
All of the descriptions are provided in postman/ including screenshot and API detail. Thanks a lot for reviewing my task.
