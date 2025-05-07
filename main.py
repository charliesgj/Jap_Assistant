#we want LLM to read the pic by its folder name and give response corresponding to each of the pic.
from pydantic import BaseModel, Field
from llm_factory import LLMFactory
import base64
import os
from tools import create_markdown_notes
import re

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


level = "N4"

class Japanesenotes(BaseModel):
      title: str = Field(description="The title or theme of the class")
      keypoints: list[str] = Field(description="The keypoints of the class")
      examples: list[str] = Field(description="The example sentences of the class")
      notes: list[str] = Field(description="things to remember and not yet covered")
      annotations: list[str] = Field(description="kanji annotations")

class JapaneseExample(BaseModel):
      base_contents: str = Field(description="The base contents of the class, japanese and corresponding Chinese translation")
      extended_contents: str = Field(description=f"good to know related knowledge points at this level {level}")
      possible_hard_vocabularies: list[str] = Field(description="possible hard words in the context and their meanings")
      annotations: list[str] = Field(description="kanji annotations")

llm = LLMFactory(provider="anthropic")


def process_single_japanese_screenshot(is_note:bool,original_file_path, original_file_name):
    content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": encode_image(original_file_path+"/"+original_file_name)
                }
            },
            {
                "type": "text",
                "text": "请分析这张日语学习截图，提取所有语法点、例句、读音和翻译信息。除了日语内容外均使用中文回答。"
            }
        ]
    messages = [
            {"role": "system", 
            "content": "You are a super helpful teacher that is fluent in Japanese and Chinese. \
            You are well-taught and familiar with different use cases of Japanese grammers and their corresponding Chinese translations.\
            You help students learn Japanese happily and effectively."},
            {"role": "user", "content": content},
        ]
    if is_note:
        note_completion = llm.create_completion(Japanesenotes, messages)
        create_markdown_notes(note_completion, f"notes/{level}",original_file_name[:-4]+".md")
    else:
        example_completion = llm.create_completion(JapaneseExample, messages)
        create_markdown_notes(example_completion, f"notes/{level}", original_file_name[:-4]+".md")

def process_batch_japanese_screenshots(original_folder_path):
    files = os.listdir(original_folder_path)
    lessons = {}
    for file in files:
         #将文件名分类存储方便对文档进行append
         match = re.match(r"(\d+)\.png", file)
         if match:
            file_name = match.group(1)
            if file_name not in lessons:
                lessons[file_name] = []
            lessons[file_name].append(file)
    for lesson in lessons:
        lessons[lesson].sort()
    
    for lesson in lessons.keys():
        for file in lessons[lesson]:
            num_of_files = len(lessons[lesson])
            if file.endswith(f".{num_of_files}.png") or file.endswith(f".{num_of_files-1}.png"):
                is_note = False
            else:
                is_note = True
            process_single_japanese_screenshot(is_note, original_folder_path, file)



