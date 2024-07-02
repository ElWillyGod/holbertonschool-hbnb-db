# Integration tests
---

## How to use
  Run runall.py to run all automatic tests. The default url is
http://127.0.0.1:5000/, but you can change it if you provide it as an argument.
Example: ./runall.py http://127.0.0.1:8000/
  You can also do the same but individually with each test, or make manual
tests using the testingShell.py.
  The testing shell provides a way to use the testlib.py with a command line
interface. You can use it by running it directly (i.e. ./testingShell.py).
You see all commands using "help" and exit using "exit/quit".

## Why
  Automatic tests can be used to see if any changes to fix something breaks
something else. It's also a way to enforce requirements if done right.
In our case we didn't have enough workforce to do tests _before_ or during
development of the app.

## Problems
  If requirements shift, both the application and the checker must be updated.
This normally makes the automatic checks outdated as application changes
normally has priorities over tests.
