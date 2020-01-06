import sys, getopt, os, shutil, time
import pymysql.cursors

from jinja2 import Environment, FileSystemLoader

# In order for this to work, the name of the table needs to be given
# as a command line argument.

# Used to map DB datatype to sqlalchemy datatype
def get_datatype(rawDataType):
    if "int" in rawDataType:
        return "Integer"
    
    elif "varchar" in rawDataType:
        return "String"

    elif "datetime" in rawDataType:
        return "DateTime"
    
    elif "tinyint" in rawDataType:
        return "Boolean"

# Used to map DB datatype to graphql datatype
def get_gtype(rawDataType):
    if "int" in rawDataType:
        return "Int"

    elif "varchar" in rawDataType:
        return "String"

    elif "datetime" in rawDataType:
        return "DateTime"
    
    elif "tinyint" in rawDataType:
        return "Boolean"

if len(sys.argv) < 1:
    print("You must give this file exactly 1 command line argument")
    print("The 1 argument must be the name of a table")
    print("python addTable.py <tableName>")
    sys.exit(1)

else:
    # Connect to database
    connection = pymysql.connect(host=os.environ['DB_HOST'],
                                port=os.environ['DB_PORT'],
                                user=os.environ['DB_USERNAME'],
                                password=os.environ['DB_PASSWORD'],
                                db=os.environ['DB_NAME'],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        # Grabs the command line arguments
        args = getopt.getopt(sys.argv, "")

    except getopt.GetoptError as err:
        print(err)
        print("python addTable.py <tableName>")
        sys.exit(2)
    
    try:
        with connection.cursor() as cursor:
            # Runs DESCRIBE <tablename>; to get schema of table
            sql = "DESCRIBE " + str(args[1][1])
            cursor.execute(sql)

            fields = []
            primaryKey = None

            # Maps table schema into a list of objects
            for row in cursor:
                if (row['Key'] == "PRI"):
                    primaryKey = row['Field']


                name = row['Field']
                datatype = get_datatype(row['Type'])
                gtype = get_gtype(row['Type'])

                fields.append({'name': name, 'datatype': datatype, 'gtype':gtype })

            if (primaryKey == None):
                print("Table must contain a primary key")
                sys.exit(3)

            # loads all templates from the templates folder
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)

            # gets the specified template from the environment
            modelTemplate = env.get_template('model.jinja')
            schemaTemplate = env.get_template('schema.jinja')

            # Defining different names used in the templates
            tableName = str(args[1][1])
            className = str(args[1][1]).capitalize()
            objName = str(args[1][1])


            # rendering the templates with data
            modelOutput = modelTemplate.render(primaryKey=primaryKey,
                                     tableName=tableName, 
                                     className=className, 
                                     objName=objName, 
                                     fields=fields)
            
            # rendering the templates with data
            schemaOutput = schemaTemplate.render(primaryKey=primaryKey,
                                     tableName=tableName, 
                                     className=className, 
                                     objName=objName, 
                                     fields=fields)

            # verifies the models/<tablename> folder exists
            # will error out if non-existent
            if not os.path.exists("models/" + tableName):
                os.makedirs("models/" + tableName)

            # Creates file and writes data to file
            modelPath = 'models/' + tableName + '/model.py'
            model = open(modelPath, 'w+')
            model.write(modelOutput)
            model.close

            # Creates file and writes data to file
            schemaPath = 'models/' + tableName + '/schema.py'
            schema = open(schemaPath, 'w+')
            schema.write(schemaOutput)
            schema.close
            
            # Creates init file to allow for modules
            initPath = 'models/' + tableName + '/__init__.py'
            init = open(initPath, 'w')
            init.close

            # Gets all files/folders in the models folder
            sqlTypes = os.listdir('models/')
            print(sqlTypes)
            schemaTypes = []

            # removed any files ending in .py
            for t in sqlTypes:
                if t.endswith('.py'):
                    sqlTypes.remove(t)
            

            # using the folder names, creates schemaTypes to generate master schema 
            for t in sqlTypes:
                name = t
                query = t.capitalize() + "Queries"
                mutation = t.capitalize() + "Mutations"
                gqlDef = t.capitalize() + "_gql"

                schemaTypes.append({"name": name, "query": query, "mutation": mutation, "gqlDef": gqlDef})

            # Get masterSchema template and render it with data
            masterSchemaTemplate = env.get_template('masterSchema.jinja')
            masterSchemaOutput = masterSchemaTemplate.render(types=schemaTypes)
            
            # Creates/updates master schema file
            masterSchemaPath = 'connections/schema.py'
            masterSchema = open(masterSchemaPath, 'w+')
            masterSchema.write(masterSchemaOutput)
            masterSchema.close

            # removes previous module information because a new module has been added
            shutil.rmtree('build')
            shutil.rmtree('dist')
            shutil.rmtree('graphqlGenerator.egg-info')

            time.sleep(3)

            # rebuilds modules structure
            os.system('python setup.py install')

    finally:
        connection.close()
