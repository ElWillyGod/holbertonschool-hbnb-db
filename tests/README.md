# Integration tests
---

## Important
  The automatic tests are defined for _this_ application. They might not work
on other applications under similar requirements.

## How to use
  Run "runall.py" to run all automatic tests. The default URL is
'http://127.0.0.1:5000/', but you can change it if you provide it as an
argument. Example: './runall.py http://127.0.0.1:8000/'. You can also use
'flask' and 'gunicorn' as URLs, as they are matched in "testlib.py".

  You can also run tests individually instead of running all tests, or make
manual tests using the "testingShell.py".

  The testing shell provides a way to use the "testlib.py" with a command line
interface. You can use it by running it directly (i.e. './testingShell.py').
From the lib you can only call methods. There is also some built-ins. Methods
that return something are printed in a pretty way. You can see most of the
commands using 'help' and exit using 'exit'/'quit'. You can also see the help
command text inside "shell_help.txt".

## Why
  Automatic tests can be used to see if any changes to fix something breaks
something else. It's also a way to enforce requirements if done right.
In our case we didn't have enough workforce to do tests _before_ or during
development of the app, so it mostly works to debug and show off.

## Problems
  If requirements shift, both the application and the checker must be updated.
This normally makes the automatic checks outdated as application updates
have priority over tests.
