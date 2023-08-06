# pkgexampledatabases

A RexBytes example package that shows you how to,

1) Create and address an sqlite3 database inside your python package.
2) Create and address an sqlite3 database at anyother location on a filesystem.
   Access to a users home directory is used as the example.


The following config files are used to describe two sqlite databases.

1) /pkgexampledatabases/data/config/packagedb.json
   This is the json description file for the database that is constructed inside your package.

2) /pkgexampledatabases/data/config/userdb.json
   This is the json desctiption file for the database that is constructed inside a users home directory.


You can have as many database entries in the above files as you like.
It is convenient to describe your databases in json format and let your package create the
end user databases.
