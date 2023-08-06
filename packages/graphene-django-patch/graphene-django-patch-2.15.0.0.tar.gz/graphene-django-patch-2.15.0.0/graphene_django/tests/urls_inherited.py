from django.urls import path

from ..views import GraphQLView
from .schema_view import schema


class CustomGraphQLView(GraphQLView):
    schema = schema
    graphiql = True
    pretty = True


urlpatterns = [path(r"^graphql/inherited/$", CustomGraphQLView.as_view())]
