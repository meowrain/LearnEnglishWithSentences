import json
import requests
from dotenv import load_dotenv
import os
# 加载.env文件中的环境变量
load_dotenv()
def getGptResponse(word,callback):
    url = os.getenv("openai_baseurl")
    openai_apiKey = os.getenv("openai_apiKey")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_apiKey}'
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"You are a translator, I will give you all the words and their Chinese meanings, please give all the example sentences and example sentence translations of these words,Pinyin is not required"
            },
            {
                "role": "user",
                "content": word
            }
        ],
        "stream": True
    }

    response = requests.post(url, headers=headers, json=data,stream=True)
    buffer = ""
    # Iterate through the stream of events
    for line in response.iter_lines(decode_unicode=True):
        if line.startswith("data:"):
            # Extract the JSON content from the line
            json_content = line[len("data:"):]
            buffer += json_content.strip()

            # If the buffer contains valid JSON, parse and process it
            if buffer.endswith("}"):
                try:
                    chunk_data = json.loads(buffer)
                    if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                        chunk_message = chunk_data['choices'][0].get('delta', {}).get('content', '')
                        callback(chunk_message)
                    else:
                        print("Chunk does not contain expected data:", chunk_data)
                except json.JSONDecodeError:
                    print("Error parsing JSON content:", buffer)
                
                buffer = ""  # Reset the buffer
