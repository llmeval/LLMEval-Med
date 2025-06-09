from transformers import pipeline, AutoTokenizer
import torch
import json
import os
from tqdm import tqdm
import subprocess

# Model path
model_name = "<model path>"

# Set CUDA environment variables
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:500"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

def get_free_gpu():
    # Use nvidia-smi to get memory usage of all GPUs
    result = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.free,memory.total', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE)
    gpus = result.stdout.decode().strip().split('\n')

    # Find the GPU with the most free memory
    max_free_memory = -1
    selected_gpu = -1
    for gpu in gpus:
        gpu_info = gpu.split(', ')
        gpu_index = int(gpu_info[0])
        memory_free = int(gpu_info[1])
        memory_total = int(gpu_info[2])

        if memory_free > max_free_memory:
            max_free_memory = memory_free
            selected_gpu = gpu_index

    return selected_gpu

selected_gpu = get_free_gpu()
print(f"Using GPU {selected_gpu} for processing.")

# Use transformers pipeline for text generation
model = pipeline("text-generation", model=model_name, tokenizer=tokenizer, device=selected_gpu)

def clear_cuda_cache():
    """ Clear unused GPU memory """
    torch.cuda.empty_cache()

def getresponse(prompt, history):
    prompt =  history + prompt
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    prompt = model.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    outputs = model(
        prompt,
        max_new_tokens=2048,
        eos_token_id=model.tokenizer.eos_token_id,
        do_sample=True
    )

    response = outputs[0]["generated_text"][len(prompt):]
    return response

def load_json(filepath):
    """
    Load data from a JSON file.

    Parameters:
    filepath (str): Path to the JSON file.

    Returns:
    dict: Loaded JSON data.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_jsonl(file_path, data, ensure_ascii=False):
    """
    Save data in JSONL format.

    Parameters:
    file_path (str): Output file path.
    data (list): List of data to save.
    ensure_ascii (bool): Whether to ensure ASCII encoding.
    """
    with open(file_path, "w") as out_fp:
        for item in data:
            out_fp.write(json.dumps(item, ensure_ascii=False) + "\n")

def add_object_to_json_file(obj, filepath):
    """
    Add an object to a JSON file.

    Parameters:
    obj (dict): The object to add.
    filepath (str): Path to the JSON file.
    """
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []
    data.append(obj)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def check_circular_reference(obj, seen=None):
    """
    Check if an object has circular references.

    Parameters:
    obj (any): The object to check.
    seen (set): Set of objects already seen.

    Returns:
    bool: Returns True if circular reference exists, False otherwise.
    """
    if seen is None:
        seen = set()

    if id(obj) in seen:
        return True

    seen.add(id(obj))

    if isinstance(obj, dict):
        for value in obj.values():
            if check_circular_reference(value, seen):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if check_circular_reference(item, seen):
                return True

    seen.remove(id(obj))
    return False

# Folder paths
inputs_dir = '<Input data set path>' # You might want to replace this placeholder text too
outputs_dir = '<Output result path>' # You might want to replace this placeholder text too

# Verify output folder exists, create if not
if not os.path.exists(outputs_dir):
    os.makedirs(outputs_dir)

# List to store input file paths
inp_paths = []
out_paths = []

clear_cuda_cache()

filename = 'dataset.json'
inp_path = os.path.join(inputs_dir, filename)
file_base = os.path.splitext(filename)[0]
out_path = os.path.join(outputs_dir, f"{file_base}_output.json")
inp_paths.append(inp_path)
out_paths.append(out_path)

if __name__ == '__main__':
    for inp_path, out_path in zip(inp_paths, out_paths):
        queries_list = load_json(inp_path)
        output_data = {}

        for key in tqdm(queries_list, desc="Processing query types"):
            resp_history = {}
            reqtosave = {}
            reqall = []
            output_data[key] = []
            for req in tqdm(queries_list[key], desc="Progress"):
                question = req["problem"]
                groupCode = req["groupCode"]
                round = req["round"]
                if round > 1:
                    history = resp_history.get(str(groupCode), "")
                else:
                    history = ""
                resp = getresponse(question, history)
                reqtosave = req
                resp_history[str(groupCode)] = resp_history.get(str(groupCode), "") + "答:" + resp + "\n" + "问:" # "答:" is Answer, "问:" is Question
                keystr = f"model_answer" 
                reqtosave[keystr] = resp
                output_data[key].append(reqtosave)

        # Save output data
        with open(out_path, 'w', encoding='utf-8') as out_file:
            json.dump(output_data, out_file, ensure_ascii=False, indent=4)

        # Clear CUDA cache, only once at the end of each round
        clear_cuda_cache()
