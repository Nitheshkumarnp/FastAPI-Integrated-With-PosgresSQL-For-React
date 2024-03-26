from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None

@app.get("/details")
async def get_all_details():
    conn = get_db_connection()
    if not conn:
        return {"message": "Failed to connect to database"}

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print("Error fetching data:", e)
        return {"message": "Error fetching data"}
    finally:
        conn.close()
      
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
