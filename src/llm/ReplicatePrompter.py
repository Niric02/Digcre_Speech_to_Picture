import replicate

class ReplicatePrompter:

    def __init__(self,client,logger):
        self.client = client
        self.logger = logger.getChild('prompter')

    def create_input(self,prompt,prompt_template):
        return {
                "top_p": 0.9,
                "prompt": prompt,
                "min_tokens": 0,
                "temperature": 0.6,
                "prompt_template": prompt_template,
                "presence_penalty": 1.15
                }

    async def run(self, prompt,context):
        output = await self.client.async_run(
                "meta/meta-llama-3-70b-instruct",
                input = self.create_input(prompt,context),
        )
        prompt = "".join(output)
        self.logger.info(f"llm: {prompt}")
        return prompt
