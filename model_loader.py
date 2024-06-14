from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from a .env file
load_dotenv()

model_name = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama_v1.1")

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")
    exit(1)

try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        device_map="auto",
        # device="cuda",
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

async def generate_response(prompt, stream=False):
    """
    Generates a response to the given prompt using the language model.

    Args:
        prompt (str): The input text prompt.
        stream (bool): Whether to stream the response in chunks (default is False).

    Yields:
        str: Chunks of the generated response if streaming is enabled.
        str: The complete generated response if streaming is disabled.

    This function encodes the input prompt into input IDs, generates a response from the model,
    and decodes the output IDs back into text. If streaming is enabled, it yields chunks of the
    response in real-time. Otherwise, it yields the complete response.
    """
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    max_length = 50

    if stream:
        for i in range(max_length):
            output = model.generate(input_ids, max_length=len(input_ids[0]) + i + 1, do_sample=True)
            decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
            yield decoded_output[len(prompt):]
            await asyncio.sleep(0.1)
            if len(decoded_output) >= max_length:
                break
        yield 'end'
    else:
        output = model.generate(input_ids, max_length=max_length, do_sample=True)
        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        yield decoded_output

def generate_text(prompt):
    """
    Generates a response to the given prompt synchronously.

    Args:
        prompt (str): The input text prompt.

    Returns:
        str: The complete generated response.

    This function sets up an event loop to run the asynchronous collect_response function,
    and returns the collected response.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(collect_response(prompt))

async def collect_response(prompt):
    """
    Collects the complete response to the given prompt.

    Args:
        prompt (str): The input text prompt.

    Returns:
        str: The complete generated response.

    This function collects the response from the generate_response function asynchronously,
    concatenating chunks of the response if streaming is disabled.
    """
    response = ""
    async for part in generate_response(prompt, stream=False):
        response += part
    return response
