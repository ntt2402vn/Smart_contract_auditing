import json
import openai
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

openai.api_key = ""  

# Load the JSON dataset
with open("smart_contract_dataset_5.json", "r") as f:
    dataset = json.load(f)

# Total number of items to process
num_samples = len(dataset)  

def process_item(i):
    contract = dataset[i]["input"]
    vuln_output = dataset[i]["output"]

    prompt = f"""
    You are a smart contract security expert.

    Your task is to analyze a Solidity smart contract that has been scanned for vulnerabilities. You will be given:
    1. The full Solidity smart contract source code.
    2. A list of vulnerabilities, categorized by type.

    Here is the Solidity contract:
    {contract}

    Here is the list of vulnerabilities:
    {vuln_output}

    For each line or function identified in the vulnerabilities above, please provide a detailed explanation of the issue and its potential impact. You should explain the vulnerability based on the actual source code at that specific line or function.
    
    For each vulnerability in the list of vulnerabilities, please provide the following details for **all lines/functions** within that type of vulnerability (each lines/functions must be seperate):

    1. [Function/Line]: (Include the code for the identified function/line base on the source code. If it is a function, then only provide the name of the function)

    [Explanation]: Provide a **short and concise** explanation of why this line or function causes the identified vulnerability base on the source code.

    For example:

    [Arithmetic (Integer Overflow and Underflow) - Line 350]:

    =>[Function/Line]: grant = (now - lastAccess) / 72 minutes;

    =>[Explanation]: This line involves a subtraction operation where the result is divided by a constant, which could lead to overflow or underflow if the values involved are not validated before the calculation. Overflow or underflow occurs when the result exceeds the maximum or minimum value the data type can store, potentially causing unintended behavior.

    Repeat this for each vulnerability type and provide similar descriptions for each.
    NOTE: If a vulnerablity type has 2 lines, then there should be 2 **seperated** section for each line.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert coder."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0
        )
        explanation = response["choices"][0]["message"]["content"]
        return {"input": dataset[i]["input"], "output": explanation}
    except Exception as e:
        return {"input": dataset[i]["input"], "output": f"Error: {str(e)}"}

total_samples = len(dataset)  

if __name__ == "__main__":
    with Pool(processes=10) as pool:
        results = list(tqdm(pool.imap(process_item, range(total_samples)), total=total_samples))

    with open("ordered_explanations_output_5.json", "w") as out_file:
        json.dump(results, out_file, indent=2)
