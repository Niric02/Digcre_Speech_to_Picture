import replicate

input = {
    "top_p": 0.9,
    "prompt": "So maybe it does it now. So it's supposed to stop, take a recording for 60 seconds and then send that recording to the model and then it should go back. Yes. To create an image. Okay. Exactly. Okay. Is this Discord? So you are recording on Discord? Yes. Discord send it to this? No, no, no. That's this one here. That's that. Okay. Oh, I hate it. It doesn't work. But your name here is like flashing like this. Yeah, that's the recording. Okay.",
    "min_tokens": 0,
    "temperature": 0.6,
    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are an Interface between a speech to text model and an Image generation model. Generate a prompt from the input to create a scene for a DND Campaign. Just give the prompt<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    "presence_penalty": 1.15
}

for event in replicate.stream(
    "meta/meta-llama-3-70b-instruct",
    input=input
):
    print(event, end="")
#=> "Let's break this problem down step by step.\n\nStep 1: S...