## Start Command
HOST_IP=$(hostname -I | awk '{print $1}') NO_PROXY=localhost LLM_ENDPOINT_PORT=8008 LLM_MODEL_ID="llama3.2:1b" docker compose up

### Check which model are running:
curl http://localhost:11434/api/tags

### query the model and get a streaming resposne
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Hello, how are you?"
}'