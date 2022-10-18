## This is one of the projects I worked on during my internship at Capgemini Engineering
- [x] It's a simple **REST Api** built using **FastAPI**, with documentation and covered in tests using **Pytest**.
- [x] To maintain this project I was using **GitLab**, and using it's CI/CD functionality created a simple **pipeline** and **githooks**.
- [x] It has integrated **PostgreSQL database, RabbitMQ communication and Redis cache**.
- [x] All dependencies are managed by **poetry**.
- [x] Whole app is operating using **docker**, running docker-compose will automatically download, install and run the app on localhost.


## WORKFLOW:
- Pull
- Create short-lived branch
- Commit changes
- Push changes
- Merge request
- Code review
- Merge

##### Task 10:
- [x] Added **RabbitMQ communication**

##### Task 9:
- [x] Added **Redis cache**

##### Task 8:
- [x] Added **PostgreSQL database**

##### Task 7:
- [x] Created **GitLab CI/CD pipeline**

##### Task 6:
- [x] Dockerized the whole project

##### Task 5:
- [x] Used **Poetry** to create **pyproject.toml** and **poetry.lock** in *.\szymon-urzedowski* with virtual environment dependencies

##### Task 4:
- [x] Created **test_main.py** in *.\szymon-urzedowski\fastapi\tests*
    - [x] Created unit tests for app and coverd 99%, for some cases applied parametrized tests
- [x] Fixed some bugs in searching
- [x] Used **python black** to format code in clearer way

##### Task 3:
- [x] Created **main.py** in directory *.\szymon-urzedowski\fastapi*
    - [x] API Users Service is an application to manage users identities. It allows to create, get, filter, update and delete users accounts.
    - [x] Added corresponding HTTP status responses

##### Task 2:
- [x] Created **OPENAPI_DOCUMENTATION.yaml** with documentation of future API

##### Task 1:
- [x] Created **pre-commit**, **prepare-commit-msg**, **commit-msg hooks** in directory *.\szymon-urzedowski\hooks*
    - [x] Fixed compatibility issues, now additional file is not needed!
- [x] Created symlinks to those hooks in *.\szymon-urzedowski\.git\hooks*
- [x] Same procedure for **COMMIT_EDITMSG** file, so changes in hook's code is not necessary, creating symlink to *.\szymon-urzedowski\.git* is enough
- [x] Lots of working and not-working commits later I think everything works thanks to trial-and-error method.
- [x] Can't solve the server-sided hook problem, everywhere I check Im informed that I need to be GitLab server administrator, and Im stuck.
    - [x] Created **pre-recive** hook that I can't test yet, idk if it works
- [x] Edited **README** with what I think workflow means and a quick recap of todays work with some styling fun.
- [x] Changed repository settings to protect main branch, no one is allowed to push directly.
