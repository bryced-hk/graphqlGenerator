from flask import Flask, redirect
from flask_graphql import GraphQLView
from database import db_session
from schema import schema

app = Flask(__name__)

# Adds the path to the graphql playground
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        context={'session': db_session}
    )
)

# redirects to the graphql playground
@app.route('/')
def index():
    return redirect('/graphql')


if __name__ == '__main__':
    app.run(debug=True)
