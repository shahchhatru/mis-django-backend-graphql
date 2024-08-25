This is version 2 of our Routine MIS for the department of Electronics and Computer Engineering.

start the database
```
docker-compose up -d
```

Activate your virtual environment and install requirements.txt file dependenices. Use poetry or pipenv or any other virtual environment manager.


Navigate to mis folder . The folder where there is manage.py file.

```
python manage.py runserver 
```

OR 

```
python manage.py runserver custom_port_number

```

To upload the data.dump file from your host system to the PostgreSQL container and then restore the database, follow these steps:

Copy the Dump File from Host to Container:
Restore the Database inside the Container:
Step-by-Step Guide
Assuming the target PostgreSQL container ID is target_container_id, and the dump file is located in the root folder on your host system:

1. Copy the Dump File from Host to Container

```sh
docker cp /path/to/local/data.dump target_container_id:/tmp/data.dump
```
Replace /path/to/local/data.dump with the actual path to the data.dump file on your host system.

2. Restore the Database inside the Container

```sh
docker exec -i target_container_id pg_restore -U postgres -d misdb /tmp/data.dump
```
This will restore the database using the data.dump file copied to the /tmp directory inside the PostgreSQL container.

Complete Command Sequence
Copy Dump File to Container:


```sh
docker cp /path/to/local/data.dump target_container_id:/tmp/data.dump
```
Restore the Database:


```sh
docker exec -i target_container_id pg_restore -U postgres -d misdb /tmp/data.dump
```
Example Commands
If your data.dump file is in the root folder on your host system and the target container ID is 123456789abc:

Copy Dump File to Container:

```sh
docker cp /root/data.dump 123456789abc:/tmp/data.dump
```
Restore the Database:

```sh
docker exec -i 123456789abc pg_restore -U postgres -d misdb /tmp/data.dump
```
These commands will ensure that the data.dump file is uploaded to the PostgreSQL container and the database is restored accordingly.


To dump data from postgres to our host:
1. Dump Data from the Source Database
Use pg_dump to export the data from the source PostgreSQL container. Replace your_db_name, your_db_user, and source_container_id with appropriate values.

Run the following command to dump the data from the source PostgreSQL container to a file on your host system:

```sh
docker exec -t 289546647cd2 pg_dump -U postgres -d misdb -F c -f /tmp/data.dump
```

Copy dump file from container to host system 
```sh
docker cp 289546647cd2:/tmp/data.dump /path/to/local/directory/data.dump

```


1. Delete Migration Files:
Navigate to each app's migrations directory.
Remove all files except for __init__.py. You can do this manually or use the command line.
Command Line (Linux/MacOS/WSL):

```bash
Copy code
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

2. Ignore migrations and cache files while uploading 
Remove Existing Files from Git Tracking:

If these files have already been tracked by Git, remove them using:
```bash
Copy code
git rm -r --cached .
git add .
git commit -m "Update .gitignore to exclude migrations, Pipfile, and cache files"
```
Push Changes:
Push the changes to your remote repository:

```bash
Copy code
git push origin <your-branch>
```
This configuration ensures that migrations, Pipfile, Pipfile.lock, and Python cache files are ignored by Git moving forward.


Edit the following line in your settings.py to match your database configurations.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'misdb',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',  # or 'dev-db' if using Docker networking
        'PORT': '5434',
    }
}
```








