from fastapi import FastAPI
import posts
import users


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
async def index():
    return {'message': 'Hello World'}
