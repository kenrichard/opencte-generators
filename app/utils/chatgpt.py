"""Module providing helpers for calling open ai"""

import os
from io import StringIO
import csv
import json
from openai import OpenAI
import tiktoken

from app.models.audit import audit_completion

DEFAULT_MODEL = "gpt-4-turbo-preview"
DEFAULT_MODEL_IMAGES = "dall-e-3"
DEFAULT_TEMPERATURE = 0.3

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_embedding(content, description, keys):
    """Function to get an embedding for a string"""
    model = "text-embedding-ada-002"
    response = client.embeddings.create(input=content, model=model)
    audit_completion(content, description, keys, model, response)
    return response.data[0].embedding


def token_count(content, model=DEFAULT_MODEL):
    """Function to count tokens for a given string"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(content))


def remove_backticks(input_string):
    """Function to remove the backticks"""
    return (
        input_string.replace("```csv", "")
        .replace("```plaintext", "")
        .replace("```json", "")
        .replace("```", "")
    )


def result_to_csv(content):
    """Function to create CSV list of rows"""
    without = remove_backticks(content)
    f = StringIO(without)
    reader = csv.reader(f, delimiter=",")
    return list(reader)


def result_to_json(content):
    try:
        without = remove_backticks(content)
        return json.loads(without)
    except json.decoder.JSONDecodeError as err:
        # It will sometimes use illegal escape characters
        content_retry = content.replace("\\'", "'")
        try:
            return json.loads(content_retry)
        except json.decoder.JSONDecodeError:
            print("\n\n== CONTENT ==")
            print(content)
            print("\n\n== ERROR ==")
            print(err)
            print("\n\nError processing openai response")
            raise RuntimeError("Error processing openai response")


def open_ai_submit_csv(prompt, description, keys={}, model=DEFAULT_MODEL):
    """Function to submit prompt to open ai"""
    if os.environ["OPENAI_API_KEY"] is None:
        raise ValueError("OPENAI_API_KEY Not Defined")
    print("Waiting for ChapGPT: " + description)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=DEFAULT_TEMPERATURE,
    )
    audit_completion(prompt, description, keys, model, completion)
    content = completion.choices[0].message.content
    return result_to_csv(content)


def open_ai_submit(prompt, description, keys={}, model=DEFAULT_MODEL):
    """Function to submit prompt to open ai"""
    if os.environ["OPENAI_API_KEY"] is None:
        raise ValueError("OPENAI_API_KEY Not Defined")
    print("Waiting for ChapGPT: " + description)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=DEFAULT_TEMPERATURE,
    )
    content = completion.choices[0].message.content
    audit_completion(prompt, description, keys, model, completion)
    return content


def open_ai_submit_json(prompt, description, keys={}, model=DEFAULT_MODEL):
    """Function to submit prompt to open ai"""
    if os.environ["OPENAI_API_KEY"] is None:
        raise ValueError("OPENAI_API_KEY Not Defined")
    print("Waiting for ChapGPT: " + description)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=DEFAULT_TEMPERATURE,
    )
    content = completion.choices[0].message.content
    audit_completion(prompt, description, keys, model, completion)
    return result_to_json(content)


def open_ai_submit_image(prompt, model=DEFAULT_MODEL_IMAGES):
    print("Waiting for ChapGPT...")
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url
