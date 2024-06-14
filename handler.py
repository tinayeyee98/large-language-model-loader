from http.server import BaseHTTPRequestHandler
import json
import time
import asyncio
from model_loader import generate_text, generate_response, model_name

class ChatRequestHandler(BaseHTTPRequestHandler):
    """
    Request handler for the chat completions API. This class handles POST requests to generate
    responses using a language model and supports server-sent events (SSE) for streaming responses.
    """

    async def handle_sse(self, user_input):
        """
        Handles server-sent events (SSE) for streaming responses.

        Args:
            user_input (str): The input prompt from the user.

        This method sets up the response headers for SSE, generates the response in a streaming
        manner using the generate_response function, and sends each part of the response to the
        client as an SSE event.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        async for response in generate_response(user_input, stream=True):
            completion_data = self.build_completion_data(response, user_input)
            self.wfile.write(f"data: {json.dumps(completion_data)}\n\n".encode("utf-8"))
            self.wfile.flush()
            if response == 'end':
                self.close_connection = True

    def do_POST(self):
        """
        Handles POST requests to the /v1/chat/completions endpoint.

        This method reads the input data from the request, extracts the user input, and generates
        a response using the generate_text function. If the stream flag is set, it handles the
        request as an SSE. Otherwise, it sends the generated response back as a standard HTTP
        response.

        Raises:
            ValueError: If the input data is not valid JSON.
            Exception: If any other error occurs during processing.
        """
        if self.path == "/v1/chat/completions":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                messages = data.get("messages", [])
                stream = data.get("stream", False)
                
                user_input = self.extract_user_input(messages)

                if stream:
                    asyncio.run(self.handle_sse(user_input))
                else:
                    response = generate_text(user_input)
                    self.respond_with_completion(response, user_input)
            except ValueError:
                self.send_error(400, "Invalid JSON data")
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Not Found")

    def extract_user_input(self, messages):
        """
        Extracts the user input from the list of messages.

        Args:
            messages (list): A list of message dictionaries.

        Returns:
            str: The user input content if found, otherwise an empty string.
        """
        for message in messages:
            if message["role"] == "user":
                return message["content"]
        return ""

    def build_completion_data(self, response, user_input):
        """
        Builds the completion data dictionary for the response.

        Args:
            response (str): The generated response content.
            user_input (str): The input prompt from the user.

        Returns:
            dict: A dictionary containing the completion data.
        """
        return {
            "id": model_name,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model_name,
            "system_fingerprint": "fp_44709d6fcb",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "logprobs": None,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_input.split()),
                "completion_tokens": len(response.split()),
                "total_tokens": len(user_input.split()) + len(response.split())
            }
        }

    def respond_with_completion(self, response, user_input):
        """
        Sends the completion data as an HTTP response.

        Args:
            response (str): The generated response content.
            user_input (str): The input prompt from the user.

        If the response is successfully generated, this method sends the completion data as a JSON
        response with a 200 status code. Otherwise, it sends a 400 error.
        """
        if response:
            completion_data = self.build_completion_data(response, user_input)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(completion_data).encode("utf-8"))
        else:
            self.send_error(400, "Failed to generate response")
