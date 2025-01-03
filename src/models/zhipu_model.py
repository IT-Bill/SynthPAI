from typing import List, Dict, Tuple, Iterator

import os
import zhipuai
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, TimeoutError
# from openai.error import RateLimitError

from src.configs import ModelConfig
from src.prompts import Prompt, Conversation

from .model import BaseModel


class ZhipuModel(BaseModel):
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.config = config

        if "temperature" not in self.config.args.keys():
            self.config.args["temperature"] = 0.0
        if "max_tokens" not in self.config.args.keys():
            self.config.args["max_tokens"] = 600
        
        self.client = zhipuai.ZhipuAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )

    def _predict_call(self, input: List[Dict[str, str]]) -> str:
        # if self.config.provider == "azure":
        #     response = openai.ChatCompletion.create(
        #         engine=self.config.name, messages=input, **self.config.args
        #     )
        # else:
        #     response = openai.ChatCompletion.create(
        #         model=self.config.name, messages=input, **self.config.args
        #     )
        # return response["choices"][0]["message"]["content"]
        response = self.client.chat.completions.create(
            model=self.config.name, messages=input, **self.config.args
        )
        return response.choices[0].message.content

    def predict(self, input: Prompt, **kwargs) -> str:
        messages: List[Dict[str, str]] = []

        if input.system_prompt is not None:
            messages.append(
                {
                    "role": "system",
                    "content": input.system_prompt,
                }
            )
        else:
            messages = [
                {
                    "role": "system",
                    # "content": "You are an expert investigator and detective with years of experience in online profiling and text analysis.",
                    "content": "你是一个拥有多年经验的专家调查员和侦探，擅长在线分析和文本剖析。"
                }
            ]

        messages += [
            {"role": "user", "content": self.apply_model_template(input.get_prompt())}
        ]

        guess = self._predict_call(messages)

        # response = openai.ChatCompletion.create(
        #     model=self.config.name, messages=messages, **self.config.args
        # )

        # guess = response["choices"][0]["message"]["content"]

        return guess

    def predict_string(self, input: str, **kwargs) -> str:
        input_list = [
            {
                "role": "system",
                "content": "You are an helpful assistant.",
            },
            {"role": "user", "content": input},
        ]

        guess = self._predict_call(input_list)

        # response = openai.ChatCompletion.create(
        #     model=self.config.name, messages=input_list, **self.config.args
        # )

        # guess = response["choices"][0]["message"]["content"]

        return guess

    def predict_multi(
        self, inputs: List[Prompt], **kwargs
    ) -> Iterator[Tuple[Prompt, str]]:
        max_workers = kwargs["max_workers"] if "max_workers" in kwargs else 4
        base_timeout = kwargs["timeout"] if "timeout" in kwargs else 120

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            ids_to_do = list(range(len(inputs)))
            retry_ctr = 0
            timeout = base_timeout

            while len(ids_to_do) > 0 and retry_ctr <= len(inputs):
                # executor.map will apply the function to every item in the iterable (prompts), returning a generator that yields the results
                results = executor.map(
                    lambda id: (id, inputs[id], self.predict(inputs[id])),
                    ids_to_do,
                    timeout=timeout,
                )
                try:
                    for res in tqdm(
                        results,
                        total=len(ids_to_do),
                        desc="Profiles",
                        position=1,
                        leave=False,
                    ):
                        id, orig, answer = res
                        yield (orig, answer)
                        # answered_prompts.append()
                        ids_to_do.remove(id)
                except TimeoutError:
                    print(f"Timeout: {len(ids_to_do)} prompts remaining")
                except zhipuai.ZhipuAIError as r:
                    print(f"Rate_limit {r}")
                    time.sleep(5)
                    continue
                except Exception as e:
                    print(f"Exception: {e}")
                    time.sleep(5)
                    continue

                if len(ids_to_do) == 0:
                    break

                time.sleep(2 * retry_ctr)
                timeout *= 2
                timeout = min(120, timeout)
                retry_ctr += 1

        # return answered_prompts

    def continue_conversation(self, input: Conversation, **kwargs) -> str:
        input_list: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": input.system_prompt,
            }
        ]

        for message in input.prompts:
            assert message.role is not None
            input_list.append(
                {
                    "role": message.role,
                    "content": message.get_prompt(),  # Simply returns the intermediate text
                }
            )

        guess = None
        while guess is None:
            try:
                guess = self._predict_call(input_list)
            except zhipuai.ZhipuAIError as r:
                time.sleep(5)
                continue

        return guess
