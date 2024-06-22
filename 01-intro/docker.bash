docker run --detach\
    --rm \
    --name elasticsearch \
    -m 4GB \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3

docker run --detach\
    --rm \
    --network=host \
    --volume ~/.zrok:/.zrok \
    --user "${UID}" \
    openziti/zrok share public \
        --headless \
        http://127.0.0.1:9200