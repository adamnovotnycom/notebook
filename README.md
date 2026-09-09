# Notebook
Creates standard Python docker container using [Apple Container](https://github.com/apple/container) to run scripts and connect to VS Code

## Build Container
```bash
container system start

container build -t notebook .
```

## Python script - create container
```bash
container run -it --name notebook -p 0.0.0.0:8888:8888 -v ./:/mnt/app/ notebook python /mnt/app/scripts/example.py
```

## Python script - existing container
```bash
container stop notebook && container rm notebook && container run --name notebook -p 0.0.0.0:8888:8888 -v ./:/mnt/app/ notebook python /mnt/app/scripts/example.py
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

## Codex Commands
Inside codex/ folder
```
container build -t codex .
```

Start codex and login
```
container run --rm -it --name codex -v ".:/workspace" codex --search
```

Execute one-time command
```
container exec codex ls
```

Trigger a codex prompt
```
container exec -i codex \
sh -lc 'codex exec \
--model gpt-5.6-sol \
--skip-git-repo-check \
-c '\''model_reasoning_effort="medium"'\'' \
-c '\''web_search="live"'\'' \
- < /workspace/task.md'
```

End session, container is stopped and removed automatically in interactive session
```
container system stop
```