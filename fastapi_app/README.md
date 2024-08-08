# fastapi_group_project
 Simple fastapi app
 
CL - means Commend line

Use the 'Dockerfile' so that the program can run in a Docker container. Remember to run container before steps below.

## To migrate SQLALchemy models to postgresql database :

1. Make sure you are in the 'fastapi_group_project' folder,
2. If you are not, just confirmed by ENTER buttom after type in CL : cd fastapi_group_project 
3. Type in CL : alembic init alembic
4.  Confirme by ENTER buttom
5. Look at 'alembic.ini' file and in line 63 change:

    sqlalchemy.url = postgresql+psycopg2://postgres:secret_password@localhost:5432/databasename

    secret_password  -  change for your password to your database
    databasename -  change for name of your database

6. Next, Look at 'env.py' file  and :

    -> add import :

        from fastapi_app.src.database.models import Base

    -> In line 21  change 'target_metadata' variable:

            from : target_metadata = None
            to :   target_metadata = Base.metadata

7. Now, we can start migration by typing in CL : alembic revision --autogenerate -m 'test'
8. Remeber to confirme by ENTER buttom
9. In this moment we send tables to db by typing in CL : alembic upgrade head


## DO IT TO RUN:

1. Create '.env' file in 'fastapi_app' folder.
2. Next, in CL write : poetry shell
3. Confirme by ENTER buttom
4. Next , in CL write : poetry install
5. Confirme by ENTER buttom
6. Then go to 'fastapi_group_project\fastapi_app' and  to create tables in db type in CL: alembic upgrade head
7. Confirme by ENTER buttom
8. Type in CL cd..
9. Confirme by ENTER buttom
10. To enter the correct folder in CL type : cd fastapi_app
11. Confirme by ENTER buttom
12. To run API server type in CL: uvicorn main:app --host localhost --port 8000 --reload
13. Confirme by ENTER buttom
14. Open a web browser and go to: http://localhost:8000/docs.

## MANUAL

To read documentation about this aplication take a look to the file "fastapi_group_project\docs\_build\html\index.html".