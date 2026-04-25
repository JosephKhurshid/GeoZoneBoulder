import geopandas as gpd
from sqlalchemy import create_engine
import time

DATABASE_URL = "postgresql+psycopg2://postgres:projectDTCGeography@db:5432/geozone"#psycogpg2 neede due to non string/numbers in geo data#local
# DATABASE_URL = "postgresql+psycopg2://postgres:projectDTCGeography@35.193.138.80:5432/geozone"#cloud
engine = create_engine(DATABASE_URL)

def ingest_data():
    print("ingesting zoning_districsts.geojson")
    zoning_gdf = gpd.read_file("Zoning_Districts.geojson")
    
    print("sending zoning info to postgis")
    zoning_gdf.to_postgis("zoning_districts", engine, if_exists="replace", index=True)
    print("completed sending zone info to postgis.")

    print("ingiesting  parcels.geojson. waiting a bit")
    start_time = time.time()
    parcels_gdf = gpd.read_file("Parcels.geojson")
    
    print("sending parcel info to postgis")
    parcels_gdf.to_postgis("parcels", engine, if_exists="replace", index=True)
    
    elapsed = round(time.time() - start_time, 2)
    print(f"completed sending parcel info to postgis. took {elapsed} seconds")

if __name__ == "__main__":
    ingest_data()