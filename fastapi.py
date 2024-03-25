from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your actual database connection details
DATABASE_URL = "postgres://nitheshkumar:ljQpJBpiFl3oCjjMk8tgDpAGenzu3ZBV@dpg-co06icmct0pc73dp7a10-a/first_db_s5r7"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_and_insert/")
async def create_and_insert(db: Session = Depends(get_db)):
    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    # Insert data
    item1 = Item(id=1, name="Item 1")
    item2 = Item(id=2, name="Item 2")
    db.add_all([item1, item2])
    db.commit()

    return {"message": "Table created and data inserted successfully."}
  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
