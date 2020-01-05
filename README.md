# graphqlGenerator
This program will generate a graphql api based on mysql database tables

To run this application first clone the repo.

Then go to the venv/bin/ directory and run: 
``` source activate```
This will enable the virtual environment to setup for running python applications

The next step is to install the projects dependencies. Go to venv/graphqlGenerator/ and run: 
```pip install -r requirements.txt```

Now that we have our dependencies installed we must setup the python module structure by running: 
```python setup.py install```

We can now run 
```python connections/app.py```
and the applications will start up.

To add tables to the graphql schema, inside of the /venv/graphqlGenerator/ folder run
```python addTable.py <tableName>```

This will create the sqlAlchemy base class, graphql schema, and rebuild the module structure. After this step restart the application.

If there is an error with the newly added table, remove the build/ dist/ and graphqlGenerator.egg-info/ folders
```rm -rf build/ dist/ graphqlGenerator.egg-info/```

and re-run 
```python setup.py install```

the application should now start and the new table will show in graphql.
