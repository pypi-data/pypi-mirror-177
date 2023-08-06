from django.urls import path

from ..views import GraphQLView

urlpatterns = [
    path(r"^graphql/batch", GraphQLView.as_view(batch=True)),
    path(r"^graphql", GraphQLView.as_view(graphiql=True)),
]
