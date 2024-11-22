import replicate

class ReplicatePrompter:

    prompt_template = ("<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                       "Your job is to take input from a speech to text model and create a prompt for a image generation model. Only Provide the prompt, no niceties required, make it so it is in an anime style. And feel free to be colorful in discrybing the scene"
                       " <|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>prompter<|end_header_id|>\n\n")

    def __init__(self,client):
        self.client = client

    def create_input(self,prompt):
        return {
                "top_p": 0.9,
                "prompt": prompt,
                "min_tokens": 0,
                "temperature": 0.6,
                "prompt_template": self.prompt_template,
                "presence_penalty": 1.15
                }

    def run(self, prompt):
        for event in self.client.stream(
                "meta/meta-llama-3-70b-instruct",
                input = self.create_input(prompt),
        ):
            print(str(event), end="")
