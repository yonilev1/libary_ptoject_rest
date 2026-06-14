from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes
import uvicorn
from logs import logger
from database import db_connection

app = FastAPI()
app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)




if __name__ == "__main__":
    db_connection.create_tables()
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False)