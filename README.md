# GeoZoneBoulder

## Team Member(s): 
Bazz Y. Khurshid

## Overview
GeoZone Boulder is a RESTful API that simplifies building planning by automating the cross-referencing of property maps with municipal zoning rules. When a user submits an address, the API performs a real-time spatial intersection between property lot boundaries and municipal zoning polygons to return legal land-use rules (zoning code, description, and purpose).

## Tech Stack
* Web Framework: FastAPI (Python)
* Database: PostgreSQL with the PostGIS extension
* Cache: Google Cloud Memorystore (Redis)
* Containerization & Orchestration: Docker, Google Kubernetes Engine (GKE)

## Directions 
The instructions state that the README must have directions on how to run the code. I took this to mean directions on a local deployment, since a cloud deployment would be me directing how to use google cloud to build the VPC, Cloud SQL PostGIS instance, and a Memorystore Redis instance. If you would like to see the cloud deployed version, please go to 

http://34.31.23.171/docs

OR (insert a valid boulder address in the url below)

http://34.31.23.171/api/v1/zoning?address=INSERT_BOULDER_ADDRESS


### Local Deployment Instructions (On Windows, Have Docker Desktop running)

1. Clone the repository:
   ```powershell
   git clone https://github.com/JosephKhurshid/GeoZoneBoulder.git
   cd GeoZoneBoulder
   ```

2. Start the services:
   Docker Desktop must be running. Below will spin up the FastAPI application, PostGIS database, and Redis cache.
   ```powershell
   docker-compose up --build -d
   ```

3. Ingest the Data:
   using Python container to run ingest.py, populating PostGIS database with Boulder GeoJSON data.
   ```powershell
   docker run --rm -v ${PWD}:/app --network="host" geozoneboulder-api python ingest.py
   ```
   Note: main.py and ingest.py have several lines that say either #cloud or #local. If they say #cloud, make sure they are commented out. And if they say #local, make sure they are not commented 

4. Access the API:
   Go to `http://localhost:8000/docs` in the web browser to test the endpoints with Swagger UI.

