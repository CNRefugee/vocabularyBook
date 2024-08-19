import os
import json
import random

class VocabularyNote:
    def __init__(self, word, pronunciation, translation, part_of_speech, definition, examples, related_words, date_added):
        self.word = word
        self.pronunciation = pronunciation
        self.translation = translation
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.examples = examples
        self.related_words = related_words
        self.date_added = date_added

    def to_markdown(self):
        related_links = "\n".join([f"- [{word}]({word}.md)" for word in self.related_words])
        examples_list = "\n".join([f"{idx}. {example}" for idx, example in enumerate(self.examples, 1)])
        part_of_speech_list = "\n".join([f"- {pos}" for pos in self.part_of_speech])
        definition_list = "\n".join([f"{idx}. **{pos}**: {defi}" for idx, (pos, defi) in enumerate(self.definition.items(), 1)])

        content = f"""
# {self.word}
### Pronunciation
{self.pronunciation}
### Definition
{definition_list}
### Translation
{self.translation}
### Examples
{examples_list}
### Part of Speech
{part_of_speech_list}
### Related Words
{related_links}
### Date Added
{self.date_added}
"""
        return content.strip()

    def save_to_file(self, directory="vocabulary"):
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{self.word}.md")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.to_markdown())

def load_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [VocabularyNote(**vocab) for vocab in data]

def generate_vocabulary_notes(metadata_file="metadata.json"):
    vocabulary_notes = load_metadata(metadata_file)
    for note in vocabulary_notes:
        note.save_to_file()
    generate_index_page(vocabulary_notes)


def generate_index_page(vocabulary_notes, directory="index", num_words=10):
    os.makedirs(directory, exist_ok=True)

    # 按日期排序词汇
    vocabulary_notes.sort(key=lambda x: x.date_added)

    index_content = "# Vocabulary Index\n\n"
    current_date = ""

    for note in vocabulary_notes:
        if note.date_added != current_date:
            current_date = note.date_added
            index_content += f"### {current_date}\n\n"

        index_content += f"- [{note.word}](../vocabulary/{note.word}.md)\n"

    file_path = os.path.join(directory, "index.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(index_content)

if __name__ == "__main__":
    generate_vocabulary_notes()
