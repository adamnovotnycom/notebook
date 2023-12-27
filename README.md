# Notebook
Creates standard docker container to connect to VS Code

## Connect to Jupyter server using VS Code
1. ```docker-compose -f docker-compose.yml up notebook```
1. in separate terminal:
        
        docker exec -it notebook jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root --no-browser --NotebookApp.allow_origin='*'.

1. copy server URL with token (e.g. `http://127.0.0.1:8888/?token={some_token}`) and paste as Existing Server in VSCode
1. See docs on how to[connect to a remote Jupyter server](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server)

## Execute Jupyter notebook in Docker and save output

        docker exec -it notebook bash -c 'papermill yfinance.ipynb yfinance_papermill.ipynb -k python'

