from django.urls import path
from graphene_django.views import GraphQLView
from api.schema import schema
#from api.schemas.users.schema import user_schema
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    #only a single url to access GraphQL
    #path("graphql/users",csrf_exempt(GraphQLView.as_view(graphiql=True,schema=user_schema))),
    path("graphql",csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),                           
   
]   