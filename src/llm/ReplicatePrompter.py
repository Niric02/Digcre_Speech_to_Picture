import replicate

class ReplicatePrompter:

    def __init__(self,client,logger):
        self.client = client
        self.logger = logger

    def set_context(self,context):
        prompt_template = (f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                            f"{context}"
                            f" <|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{{prompt}}<|eot_id|><|start_header_id|>prompter<|end_header_id|>\n\n")

    def create_input(self,prompt,prompt_template):
        return {
                "top_p": 0.9,
                "prompt": prompt,
                "min_tokens": 0,
                "temperature": 0.6,
                "prompt_template": prompt_template,
                "presence_penalty": 1.15
                }

    def run(self, prompt,context):
        output = ""

        for event in self.client.stream(
                "meta/meta-llama-3-70b-instruct",
                input = self.create_input(prompt),
        ):
            output += str(event)

        self.logger.info(output)
        return output
