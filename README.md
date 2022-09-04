## WORKFLOW:
- Pull
- Create short-lived branch
- Commit changes
- Push changes
- Merge request
- Code review
- Merge


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