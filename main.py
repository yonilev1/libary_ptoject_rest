from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes
import uvicorn
from database import db_connection, db_initializer

app = FastAPI()
app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)

connect = db_connection.DbConnection()
init = db_initializer.DbInitializer(connect)
init.create_tables()



if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False)