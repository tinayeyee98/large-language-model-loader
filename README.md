# large-language-model-loader
This project is designed to streamline the process of loading, managing, and deploying large language models (LLMs) efficiently.
This project sets up an HTTP server that serves responses from a large language model using Python. The server accepts POST requests with a text prompt and returns a generated response from the model.

## Prerequisites
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.10 or later

## Setup
### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/tinayeyee98/large-language-model-loader.git
cd large-language-model-loader
```

### Step 2: Set Up Miniconda Environment
1. Install Miniconda: Follow the instructions on the Miniconda website to install Miniconda.

2. Create and Activate the Environment:

```bash
conda create --name lmserver python=3.8
conda activate lmserver
```

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a .env file in the root directory of the project and add the following environment variables:

```env
HOST=localhost
SERVER_PORT=5000
MODEL_NAME=TinyLlama/TinyLlama_v1.1
```
Replace TinyLlama/TinyLlama_v1.1 with the model you intend to use.

### Step 5: Run the Server

Start the server by running:
```bash
python server.py
```
The server will start running at http://localhost:5000.

## Usage
### Sending Requests
You can send POST requests to the server with a JSON payload containing a prompt. For example:
- JSON  request payload
```json
{
    "messages": [
        { 
            "role": "system", 
            "content": "You are a helpful assistant." 
        },
        {
            "role": "user", 
            "content": "Write your message here...."
        }
    ],
    "mode": "chat", 
    "max_tokens": "20"
  }
```
- Streaming request payload
You can also request streaming response by using `stream=True` flag.
```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ],
    "mode": "chat", 
    "stream": true
}
```

- Use curl or any HTTP client to send a request:
```bash
curl -X POST http://localhost:5000 -H "Content-Type: application/json" -d '{
    "messages": [
        { 
            "role": "system", 
            "content": "You are a helpful assistant." 
        },
        {
            "role": "user", 
            "content": "Hello!"
        }
    ],
    "mode": "chat", 
    "max_tokens": "20"
  }
}'
```

### Response
The server will respond openai Chat Completions API response format.
- JSON response
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "TinyLlama/TinyLlama_v1.1",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```
- Streaming response
```json
{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-3.5-turbo-0125", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}]}

{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-3.5-turbo-0125", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"content":"Hello"},"logprobs":null,"finish_reason":null}]}

....

{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-3.5-turbo-0125", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{},"logprobs":null,"finish_reason":"stop"}]}
```

## Files
- server.py: Main server file that starts the HTTP server.
- handlers.py: Contains the request handler logic for processing incoming requests.
- model_loader.py: Loads the language model and tokenizer, and provides functions to generate text responses.
- .env: Environment variables file (not included in the repository, needs to be created manually).

## Troubleshooting
- Ensure all dependencies are installed in the Conda environment.
- Verify that the environment variables in the .env file are set correctly.
- Check the console output for any error messages and resolve them accordingly.

## Contributing
Feel free to submit issues or pull requests if you find any bugs or want to add new features.