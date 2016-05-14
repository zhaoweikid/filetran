fileserver.py is a simple http server for file upload/download

start server:

python fileserver.py -p 8080 -d /tmp/


client put file:

put anyfile to /tmp/anyfile:
curl -T anyfile http://127.0.0.1:8080/

put anyfile to /tmp/dir1/anyfile:
curl -T anyfile http://127.0.0.1:8080/dir1/

put anyfile to /tmp/dir1/file1:
curl -T anyfile http://127.0.0.1:8080/dir1/file1

client get file:

curl http://127.0.0.1:8080/dir1/file1 -o file1

or 

wget http://127.0.0.1:8080/dir1/file1



