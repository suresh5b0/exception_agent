pip install -r requirements.txt

python mcp_server.py

uvicorn api:app --reload --port 9000
