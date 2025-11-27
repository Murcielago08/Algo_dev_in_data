from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL !"

    @strawberry.field
    def user(self) -> User:
        return User(id=1, name="Alice", email="alice@example.com")

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        """
        Exemple simple de mutation.
        Normalement, il faudrait sauvegarder dans une base de données.
        """
        return User(id=2, name=name, email=email)

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
