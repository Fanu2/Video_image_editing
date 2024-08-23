import os
import subprocess
import sys

# Project path and virtual environment path
project_path = '/home/jasvir/PycharmProjects/HuggingFaceInteractions'
venv_path = os.path.join(project_path, 'venv')

# Define the scripts to be created
scripts = {
    'text_generation.py': """\
from transformers import pipeline

def generate_text(prompt):
    generator = pipeline('text-generation', model='gpt-2')
    results = generator(prompt, max_length=50, num_return_sequences=1)
    return results[0]['generated_text']

# Example usage
print(generate_text('Once upon a time'))
""",
    'sentiment_analysis.py': """\
from transformers import pipeline

def analyze_sentiment(text):
    sentiment_analyzer = pipeline('sentiment-analysis')
    result = sentiment_analyzer(text)
    return result

# Example usage
print(analyze_sentiment('I love using Hugging Face models!'))
""",
    'text_translation.py': """\
from transformers import pipeline

def translate_text(text, target_language='fr'):
    translator = pipeline('translation_en_to_fr' if target_language == 'fr' else 'translation_en_to_de')
    result = translator(text)
    return result[0]['translation_text']

# Example usage
print(translate_text('Hello, how are you?', 'fr'))
""",
    'question_answering.py': """\
from transformers import pipeline

def answer_question(question, context):
    qa = pipeline('question-answering')
    result = qa(question=question, context=context)
    return result['answer']

# Example usage
context = 'Hugging Face is a company specializing in Natural Language Processing.'
print(answer_question('What does Hugging Face specialize in?', context))
""",
    'summarization.py': """\
from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline('summarization')
    result = summarizer(text)
    return result[0]['summary_text']

# Example usage
text = 'Hugging Face is a company specializing in Natural Language Processing. They offer various models for text generation, translation, and more.'
print(summarize_text(text))
""",
    'text_classification.py': """\
from transformers import pipeline

def classify_text(text):
    classifier = pipeline('text-classification')
    result = classifier(text)
    return result

# Example usage
print(classify_text('I feel great today!'))
""",
    'ner.py': """\
from transformers import pipeline

def named_entity_recognition(text):
    ner = pipeline('ner')
    result = ner(text)
    return result

# Example usage
text = 'Hugging Face is based in New York City.'
print(named_entity_recognition(text))
""",
    'paraphrase_detection.py': """\
from transformers import pipeline

def detect_paraphrase(text1, text2):
    model_name = 'bert-base-uncased'
    model = pipeline('text-classification', model=model_name)
    result = model([text1, text2])
    return result

# Example usage
text1 = 'Hugging Face is a company specializing in NLP.'
text2 = 'Hugging Face focuses on natural language processing.'
print(detect_paraphrase(text1, text2))
""",
    'fill_mask.py': """\
from transformers import pipeline

def fill_mask(text):
    fill_masker = pipeline('fill-mask', model='bert-base-uncased')
    result = fill_masker(text)
    return result

# Example usage
print(fill_mask('Hugging Face is a [MASK] company.'))
""",
    'text_to_speech.py': """\
from transformers import pipeline

def text_to_speech(text):
    tts = pipeline('text-to-speech')
    audio = tts(text)
    with open('output.wav', 'wb') as f:
        f.write(audio)
    return 'output.wav'

# Example usage
print(text_to_speech('Hello, this is a text-to-speech example.'))
""",
    'image_captioning.py': """\
from transformers import pipeline

def generate_caption(image_path):
    image_captioner = pipeline('image-captioning')
    result = image_captioner(image_path)
    return result[0]['caption']

# Example usage
print(generate_caption('example_image.jpg'))
""",
    'text_summarization_long.py': """\
from transformers import pipeline

def summarize_long_text(text):
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    result = summarizer(text, max_length=150, min_length=50, length_penalty=2.0)
    return result[0]['summary_text']

# Example usage
text = 'Hugging Face provides state-of-the-art Natural Language Processing tools and technologies. They are pioneers in open-source machine learning and have various models available for developers and researchers.'
print(summarize_long_text(text))
""",
    'translation_multiple_languages.py': """\
from transformers import pipeline

def translate_multiple_languages(text, target_language='fr'):
    translation_pipeline = pipeline(f'translation_en_to_{target_language}')
    result = translation_pipeline(text)
    return result[0]['translation_text']

# Example usage
print(translate_multiple_languages('Good morning!', 'es'))
""",
    'text_generation_with_context.py': """\
from transformers import pipeline

def generate_text_with_context(prompt, context):
    generator = pipeline('text-generation', model='gpt-2')
    result = generator(prompt + context, max_length=100)
    return result[0]['generated_text']

# Example usage
print(generate_text_with_context('Once upon a time', ' in a land far away'))
""",
    'summarization_with_highlights.py': """\
from transformers import pipeline

def summarize_with_highlights(text):
    summarizer = pipeline('summarization')
    result = summarizer(text, min_length=30, max_length=80)
    summary = result[0]['summary_text']
    return summary

# Example usage
text = 'Hugging Face is known for its impressive suite of Natural Language Processing models. The company continues to lead in open-source AI development and provides various tools for machine learning.'
print(summarize_with_highlights(text))
""",
    'text_to_image.py': """\
from transformers import pipeline

def text_to_image(text):
    text2img = pipeline('text-to-image')
    img = text2img(text)
    img.save('output_image.png')
    return 'output_image.png'

# Example usage
print(text_to_image('A beautiful sunset over the mountains.'))
""",
    'translation_and_summarization.py': """\
from transformers import pipeline

def translate_and_summarize(text, target_language='fr'):
    translator = pipeline(f'translation_en_to_{target_language}')
    summarizer = pipeline('summarization')
    translated_text = translator(text)[0]['translation_text']
    summary = summarizer(translated_text)
    return summary[0]['summary_text']

# Example usage
text = 'Hugging Face has revolutionized Natural Language Processing with their state-of-the-art models and technologies.'
print(translate_and_summarize(text, 'es'))
""",
    'generate_story.py': """\
from transformers import pipeline

def generate_story(prompt):
    story_generator = pipeline('text-generation', model='gpt-2')
    result = story_generator(prompt, max_length=200)
    return result[0]['generated_text']

# Example usage
print(generate_story('A brave knight sets out on a quest to find a hidden treasure.'))
""",
    'text_to_image_with_style.py': """\
from transformers import pipeline

def text_to_image_with_style(text, style):
    text2img = pipeline('text-to-image')
    img = text2img(text, style=style)
    img.save('output_styled_image.png')
    return 'output_styled_image.png'

# Example usage
print(text_to_image_with_style('A futuristic cityscape', 'cyberpunk'))
""",
    'contextual_text_generation.py': """\
from transformers import pipeline

def contextual_text_generation(prompt, context):
    generator = pipeline('text-generation', model='gpt-3')
    result = generator(prompt + context, max_length=150)
    return result[0]['generated_text']

# Example usage
print(contextual_text_generation('In a world where', ' technology advances rapidly, society changes dramatically.'))
""",
    'multiple_translations.py': """\
from transformers import pipeline

def translate_texts(texts, target_language='fr'):
    translator = pipeline(f'translation_en_to_{target_language}')
    translations = [translator(text)[0]['translation_text'] for text in texts]
    return translations

# Example usage
texts = ['Hello, how are you?', 'What is your name?']
print(translate_texts(texts, 'de'))
""",
    'generate_caption_for_image.py': """\
from transformers import pipeline

def generate_caption(image_path):
    caption_generator = pipeline('image-captioning')
    result = caption_generator(image_path)
    return result[0]['caption']

# Example usage
print(generate_caption('example_image.jpg'))
""",
    'entity_recognition.py': """\
from transformers import pipeline

def recognize_entities(text):
    ner_pipeline = pipeline('ner')
    result = ner_pipeline(text)
    return result

# Example usage
print(recognize_entities('Hugging Face is based in New York City.'))
""",
    'style_transfer.py': """\
from transformers import pipeline

def style_transfer(text, style):
    style_transfer_pipeline = pipeline('style-transfer')
    result = style_transfer_pipeline(text, style=style)
    return result[0]['text']

# Example usage
print(style_transfer('The quick brown fox jumps over the lazy dog.', 'poetic'))
"""
}

# Create the project directory if it doesn't exist
os.makedirs(project_path, exist_ok=True)

# Create the virtual environment
subprocess.check_call([sys.executable, '-m', 'venv', venv_path])

# Activate the virtual environment and install dependencies
activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')

# Create a requirements file with the needed packages
requirements = """
transformers
torch
"""

with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
    f.write(requirements)

subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])

# Create the scripts in the project directory
for filename, content in scripts.items():
    with open(os.path.join(project_path, filename), 'w') as file:
        file.write(content)

print("Project setup complete with 20 scripts.")
