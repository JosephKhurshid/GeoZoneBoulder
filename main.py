from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis
import json
import asyncpg
import os

app = FastAPI(title="GeoZone Boulder API", description="Automated Boulder Zoning Service")

# redis_client = redis.Redis.from_url("redis://redis:6379/0", decode_responses=True)#local
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")#cloud
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)#cloud

class ZoningResponse(BaseModel):
    address: str
    zoning_code: str
    zoning_description: str
    zoning_purpose: str
    source: str 

async def query_postgis_zoning(address: str):
    # conn = await asyncpg.connect("postgresql://postgres:projectDTCGeography@db:5432/geozone")#local
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:projectDTCGeography@db:5432/geozone") #cloud
    conn = await asyncpg.connect(DATABASE_URL)#cloud
    
    try:
        query = """
            SELECT 
                z."ZONING" as zoning_code,
                z."ZNDESC" as zoning_description,
                z."ZONINGDISTPURPOSE" as zoning_purpose
            FROM parcels p
            JOIN zoning_districts z 
            ON ST_Intersects(p.geometry, z.geometry)
            WHERE p."SITEADDRESS" ILIKE $1
            LIMIT 1;
        """
        
        search_term = f"%{address.strip()}%"
        row = await conn.fetchrow(query, search_term)
        
        if row:
            return {
                "address": address,
                "zoning_code": row['zoning_code'],
                "zoning_description": row['zoning_description'],
                "zoning_purpose": row['zoning_purpose'],
                "source": "PostGIS Database"
            }
        return None
        
    finally:
        await conn.close()

@app.get("/api/v1/zoning")
async def get_zoning_rules(address: str):
    #gets address, checks redis cache, queries postGis on cache miss, returns json
    cache_key = f"zoning:{address.lower()}"
    cached_result = await redis_client.get(cache_key)

    if cached_result:
        result = json.loads(cached_result)
        result['source'] = "Redis Cache" 
        return result

    db_result = await query_postgis_zoning(address)    
    
    if not db_result:
        raise HTTPException(status_code=404, detail="address not found or outside boundaries")

    await redis_client.setex(
        name=cache_key,
        time=86400, 
        value=json.dumps(db_result)
    )

    return db_result