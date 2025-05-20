# Docker
```
sudo docker build
docker --version                                # to check version

docker images                                   # to check built images

docker build -t Dockerfile                      # bulding docker file

docker ps                                       # Checking containers

docker stop                                     # To kill the container

docker build -t items-grpc:1.0 -fDockerFile_2 . # Building an image from specific docker file

docker run -p 50051:50051 -d items-grpc:1.0     # Running that image

```

# ----------curl
curl http://localhost:5000/items                                                                   # to check the list of items

curl -X POST -H ²Content-Type: application/json" -d '{"name":"Laptop"}' http:/localhost:5000/items # To add an item

# -----------grpc
pip install grpcio-tools

# -----------Protobuf
    # Didn't worked
docker run -v $(pwd):/env -w /env grpc/python:latest python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/items.proto 

docker pull grpc/python

docker run -v $(pwd):/env -w /env test python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./items.proto 

    # Worked
python -m grpc_tools.protoc -I. --python_out=./src --grpc_python_out=./src ./items.proto

docker build -t items-grpc:1.0 .

docker run -d -p 50051:50051 items-grpc:1.0

# -----------REST testing
#!/bin/bash

#Configuration

ENDPOINT="http://localhost:5000/items/1"

TOTAL_REQUESTS=100

echo "Testing REST API with curl..."

START_TIME=$(date +%s.%N)

for ((i=1; i<=TOTAL_REQUESTS; i++)); do     curl -s -o /dev/null "$ENDPOINT"  # Silent mode, discard output
     echo -n "."  # Progress indicator
done

END_TIME=$(date +%s.%N)

#Calculate

TOTAL_TIME=$(echo "$END_TIME - $START_TIME" | bc)

AVG_TIME=$(echo "scale=6; $TOTAL_TIME / $TOTAL_REQUESTS" | bc)

echo -e "\n\nREST Results:"

echo "Total time for $TOTAL_REQUESTS calls: $TOTAL_TIME seconds"

echo "Average time per call: $AVG_TIME seconds"

# ------------Reflection
pip install grpcio-reflection

docker run --network host fullstorydev/grpcurl -plaintext localhost:50051 list


# ------------Interceptor
{ # in server.py
if __name__ == '__main__':
    serve()
}
