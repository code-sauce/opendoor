# opendoor
opendoor sample repo

# TODO Later
* add unit tests
* add pagination (bonus points)
* refactor the filtering function to not repeat some boilerplate code like
if x then x = int(x) else None
could be a lambda/nested function
* add a database support. wasn't quite sure about what is really meant
by a "datastore". we do have models, so the logic is decoupled with how the data persists.
we can add a DB layer (SQLAlchemy etc.) should we choose to. But currently, we are storing in memory on app-start.
* add integration tests

