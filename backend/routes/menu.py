from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

from models.menu import MenuItem, MenuItemCreate, MenuItemUpdate, MenuCategory

router = APIRouter()

# Get database connection
def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

# Get all menu items
@router.get("/menu", response_model=List[MenuItem])
async def get_menu_items(category: Optional[str] = None):
    db = get_database()
    
    # Build query filter
    query = {"is_active": True}
    if category:
        query["category"] = category
    
    # Get items from database
    items = await db.menu_items.find(query).sort("name", 1).to_list(1000)
    
    # Convert to MenuItem objects
    menu_items = []
    for item in items:
        # Remove MongoDB's _id field
        if "_id" in item:
            del item["_id"]
        menu_items.append(MenuItem(**item))
    
    return menu_items

# Get menu organized by categories
@router.get("/menu/categories", response_model=List[MenuCategory])
async def get_menu_by_categories():
    db = get_database()
    
    # Define categories
    categories = [
        {"id": "apericena", "label": "Apericena", "icon": "🍢"},
        {"id": "bevande", "label": "Bevande", "icon": "🥤"},
        {"id": "vini", "label": "Vini e Bollicine", "icon": "🍷"},
        {"id": "mixology", "label": "Mixology", "icon": "🍸"},
        {"id": "gin", "label": "I Nostri Gin", "icon": "🍃"}
    ]
    
    result = []
    for category in categories:
        # Get items for this category
        items = await db.menu_items.find({
            "category": category["id"],
            "is_active": True
        }).sort("name", 1).to_list(1000)
        
        # Convert to MenuItem objects
        menu_items = []
        for item in items:
            if "_id" in item:
                del item["_id"]
            menu_items.append(MenuItem(**item))
        
        # Create category object
        category_obj = MenuCategory(
            id=category["id"],
            label=category["label"],
            icon=category["icon"],
            items=menu_items
        )
        result.append(category_obj)
    
    return result

# Get single menu item
@router.get("/menu/{item_id}", response_model=MenuItem)
async def get_menu_item(item_id: str):
    db = get_database()
    
    item = await db.menu_items.find_one({"id": item_id, "is_active": True})
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    if "_id" in item:
        del item["_id"]
    
    return MenuItem(**item)

# Create new menu item
@router.post("/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate):
    db = get_database()
    
    # Validate category
    valid_categories = ["apericena", "bevande", "vini", "mixology", "gin"]
    if item.category not in valid_categories:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    # Create menu item
    menu_item = MenuItem(**item.dict())
    
    # Insert into database
    result = await db.menu_items.insert_one(menu_item.dict())
    
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create menu item")
    
    return menu_item

# Update menu item
@router.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: str, item_update: MenuItemUpdate):
    db = get_database()
    
    # Check if item exists
    existing_item = await db.menu_items.find_one({"id": item_id, "is_active": True})
    if not existing_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Prepare update data
    update_data = {}
    for field, value in item_update.dict().items():
        if value is not None:
            update_data[field] = value
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Validate category if provided
    if "category" in update_data:
        valid_categories = ["apericena", "bevande", "vini", "mixology", "gin"]
        if update_data["category"] not in valid_categories:
            raise HTTPException(status_code=400, detail="Invalid category")
    
    # Update item
    result = await db.menu_items.update_one(
        {"id": item_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update menu item")
    
    # Return updated item
    updated_item = await db.menu_items.find_one({"id": item_id})
    if "_id" in updated_item:
        del updated_item["_id"]
    
    return MenuItem(**updated_item)

# Delete menu item (soft delete)
@router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: str):
    db = get_database()
    
    # Check if item exists
    existing_item = await db.menu_items.find_one({"id": item_id, "is_active": True})
    if not existing_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Soft delete by setting is_active to False
    result = await db.menu_items.update_one(
        {"id": item_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete menu item")
    
    return {"message": "Menu item deleted successfully"}

# Initialize database with sample data
@router.post("/menu/init")
async def initialize_menu():
    db = get_database()
    
    # Check if menu already exists
    existing_count = await db.menu_items.count_documents({"is_active": True})
    if existing_count > 0:
        return {"message": "Menu already initialized", "items_count": existing_count}
    
    # Sample menu data
    sample_items = [
        # Apericena
        {"name": "Bruschette Miste", "price": 6.00, "description": "Pane casereccio con pomodoro, olive e paté di olive", "category": "apericena"},
        {"name": "Tagliere di Salumi", "price": 12.00, "description": "Con prosciutto crudo, salame nostrano, formaggi e miele", "category": "apericena"},
        {"name": "Crostini Toscani", "price": 8.00, "description": "Fegatini di pollo, capperi e acciughe", "category": "apericena"},
        {"name": "Olive Ascolane", "price": 7.00, "description": "Olive ripiene fritte con carne e parmigiano", "category": "apericena"},
        {"name": "Antipasto della Casa", "price": 15.00, "description": "Selezione di specialità locali per 2 persone", "category": "apericena"},
        {"name": "Focaccia al Rosmarino", "price": 5.00, "description": "Focaccia calda con rosmarino e olio d'oliva", "category": "apericena"},
        
        # Bevande
        {"name": "Acqua Naturale", "price": 2.50, "description": "50cl", "category": "bevande"},
        {"name": "Acqua Frizzante", "price": 2.50, "description": "50cl", "category": "bevande"},
        {"name": "Coca Cola", "price": 3.50, "description": "33cl", "category": "bevande"},
        {"name": "Aranciata San Pellegrino", "price": 3.50, "description": "33cl", "category": "bevande"},
        {"name": "Succo di Frutta", "price": 3.00, "description": "Pesca, albicocca, pera", "category": "bevande"},
        {"name": "Tè Freddo", "price": 3.00, "description": "Limone o pesca", "category": "bevande"},
        
        # Vini
        {"name": "Prosecco DOCG", "price": 5.00, "description": "Valdobbiadene - Bicchiere", "category": "vini"},
        {"name": "Chianti Classico", "price": 6.00, "description": "Toscana DOCG - Bicchiere", "category": "vini"},
        {"name": "Vermentino", "price": 5.50, "description": "Sardegna DOC - Bicchiere", "category": "vini"},
        {"name": "Pinot Grigio", "price": 5.50, "description": "Alto Adige DOC - Bicchiere", "category": "vini"},
        {"name": "Franciacorta DOCG", "price": 8.00, "description": "Lombardia - Bicchiere", "category": "vini"},
        {"name": "Bottiglia Prosecco", "price": 25.00, "description": "Valdobbiadene DOCG - 75cl", "category": "vini"},
        
        # Mixology
        {"name": "NEGRONI RIVISITATO", "price": 8.00, "description": "Gin speziato, bitter alla liquirizia, vermouth rosso", "category": "mixology"},
        {"name": "SPRITZ APEROL", "price": 6.00, "description": "Classico spritz con prosecco, Aperol e soda", "category": "mixology"},
        {"name": "AMERICANO 9NOVE", "price": 7.00, "description": "Bitter Campari, vermouth rosso, soda e arancia", "category": "mixology"},
        {"name": "MOSCOW MULE", "price": 8.50, "description": "Vodka premium, ginger beer, lime e menta", "category": "mixology"},
        {"name": "BELLINI ORIGINALE", "price": 7.50, "description": "Prosecco e purè di pesca bianca", "category": "mixology"},
        {"name": "HUGO", "price": 6.50, "description": "Prosecco, sciroppo di sambuco, menta e lime", "category": "mixology"},
        
        # Gin
        {"name": "Hendrick's", "price": 8.00, "description": "Scozia - 41.4% - Con cetriolo e rosa | Tonica: Fever Tree", "category": "gin"},
        {"name": "Bombay Sapphire", "price": 7.00, "description": "Inghilterra - 40% - 10 botaniche | Tonica: Schweppes", "category": "gin"},
        {"name": "Tanqueray No. Ten", "price": 9.00, "description": "Inghilterra - 47.3% - Agrumi freschi | Tonica: Fever Tree", "category": "gin"},
        {"name": "Monkey 47", "price": 12.00, "description": "Germania - 47% - 47 botaniche | Tonica: 1724", "category": "gin"},
        {"name": "Gin Mare", "price": 10.00, "description": "Spagna - 42.7% - Mediterraneo | Tonica: Fever Tree Mediterranean", "category": "gin"},
        {"name": "Malfy Rosa", "price": 8.50, "description": "Italia - 41% - Pompelmo rosa | Tonica: Fever Tree", "category": "gin"}
    ]
    
    # Create MenuItem objects and insert them
    menu_items = []
    for item_data in sample_items:
        menu_item = MenuItem(**item_data)
        menu_items.append(menu_item.dict())
    
    # Insert all items
    result = await db.menu_items.insert_many(menu_items)
    
    return {"message": "Menu initialized successfully", "items_created": len(result.inserted_ids)}