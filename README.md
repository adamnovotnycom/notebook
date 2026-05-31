# Notebook
Creates standard Python docker container using [Apple Container](https://github.com/apple/container) to run scripts and connect to VS Code

## Build Container
```bash
container system start

container build -t notebook .
```

## Python REPL
```bash
container run -it --name notebook -p 0.0.0.0:8888:8888 -v ./:/mnt/app/ notebook python
```

## Python script
```bash
container run --name notebook -p 0.0.0.0:8888:8888 -v ./:/mnt/app/ notebook python /mnt/app/example.py
```

## Notebook
```bash
container run -it --name notebook -p 0.0.0.0:8888:8888 -v ./:/mnt/app/ notebook jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root --no-browser --NotebookApp.allow_origin='*'
```

1. copy server URL with token (e.g. `http://127.0.0.1:8888/?token={some_token}`) and paste as Existing Server in VSCode
1. See docs on how to [connect to a remote Jupyter server](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server)

## Stop
```
container stop notebook && container rm notebook

container system stop
```