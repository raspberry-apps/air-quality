sudo docker build --tag=air_quality .
sudo docker run --net=host --device=/dev/ttyUSB0 air_quality
