# mongodb
1. [MongoDB Run in a Docker Container](#MongoDB-Run-in-a-Docker-Container)

### MongoDB Run in a Docker Container
1. pull image
```bash
docker pull mongo
```
2. create network
```bash
docker network create mongo_network
```
3. run container

```bash
docker run \
  --name mongodb \
  --restart=unless-stopped \
  --detach \
  --privileged \
  --network mongo_network \
  --env MONGO_INITDB_ROOT_USERNAME=admin \
  --env MONGO_INITDB_ROOT_PASSWORD=password \
  --env MONGO_INITDB_DATABASE=test_database \
  --volume mongo_data:/data/db \
  --publish 27017:27017 \
  mongo
```