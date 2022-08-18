## WORKFLOW:
- Pull
- Create short-lived branch
- Commit changes
- Push changes
- Merge request
- Code review
- Merge

##### Task 1:
- [x] Created **pre-commit**, **prepare-commit-msg**, **commit-msg hooks** in directory *.\szymon-urzedowski\hooks*
- [x] Created symlinks to those hooks in *.\szymon-urzedowski\.git\hooks*
- [x] Same procedure for **COMMIT_EDITMSG** file, so changes in hook's code is not necessary, creating symlink to *.\szymon-urzedowski\.git* is enough
- [x] Lots of working and not-working commits later I think everything works thanks to trial-and-error method.
- [ ] Can't solve the server-sided hook problem, everywhere I check Im informed that I need to be GitLab server administrator, and Im stuck.
- [x] Edited **README** with what I think workflow means and a quick recap of todays work with some styling fun.
- [x] Changed repository settings to protect main branch, no one is allowed to push directly.