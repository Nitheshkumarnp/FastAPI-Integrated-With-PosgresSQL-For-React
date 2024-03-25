import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Database connection details (replace with your actual values)
DB_HOST = "dpg-co06icmct0pc73dp7a10-a"
DB_NAME = "first_db_s5r7"
DB_USER = "nitheshkumar"
DB_PASSWORD = "ljQpJBpiFl3oCjjMk8tgDpAGenzu3ZBV"

# Create a FastAPI app
app = FastAPI()

# Define a Pydantic model for data validation and serialization
class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool = False

# Establish a database connection using a context manager for proper resource management
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        yield conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Create a route to retrieve all items from the database
@app.get("/items")
async def read_items():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
            return [Item(**item) for item in items]

# Create a route to retrieve a specific item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            return Item(**item)

# Create a route to create a new item
@app.post("/items")
async def create_item(item: Item):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO items (name, price, is_offer) VALUES (%s, %s, %s)",
                (item.name, item.price, item.is_offer),
            )
            conn.commit()
            return {"message": "Item created successfully"}

# Create a route to update an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE items SET name = %s, price = %s, is_offer = %s WHERE id = %s",
                (item.name, item.price, item.is_offer, item_id),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            return {"message": "Item updated successfully"}

# Create a route to delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            return {"message": "Item deleted successfully"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
