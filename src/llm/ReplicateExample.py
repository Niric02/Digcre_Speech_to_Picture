import replicate

input = {
    "top_p": 0.9,
    "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
    "min_tokens": 0,
    "temperature": 0.6,
    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    "presence_penalty": 1.15
}

for event in replicate.stream(
    "meta/meta-llama-3-70b-instruct",
    input=input
):
    print(event, end="")
#=> "Let's break this problem down step by step.\n\nStep 1: S...