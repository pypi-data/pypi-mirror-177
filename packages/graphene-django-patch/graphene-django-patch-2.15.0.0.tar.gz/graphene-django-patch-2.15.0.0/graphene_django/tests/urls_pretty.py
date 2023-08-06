from django.urls import path

from ..views import GraphQLView
from .schema_view import schema

urlpatterns = [path(r"^graphql", GraphQLView.as_view(schema=schema, pretty=True))]
