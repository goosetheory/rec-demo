docker build -f Dockerfile.db -t local_db_image .
docker run -p 5432:5432 --name local_db_container local_db_image
