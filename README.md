
## FileTran

a simple http server for file upload/download


### server start on port 8080 and root directory /tmp/:

```console
python fileserver.py -p 8080 -d /tmp/
```

### client put file:

put anyfile to /tmp/anyfile:
```console
curl -T anyfile http://127.0.0.1:8080/
```
put anyfile to /tmp/dir1/anyfile:
```console
curl -T anyfile http://127.0.0.1:8080/dir1/
```
put anyfile to /tmp/dir1/file1:
```console
curl -T anyfile http://127.0.0.1:8080/dir1/file1
```

### client get file:
```console
curl http://127.0.0.1:8080/dir1/file1 -o file1
```

or 
```console
wget http://127.0.0.1:8080/dir1/file1
```


