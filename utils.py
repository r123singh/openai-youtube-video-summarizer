from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import re

MODEL_ID = "gpt-4o-mini"

def extract_video_id(url):
    """Extract Youtube video Id from the URL

    Args:
        link (str): _description_
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Youtube URL")


def get_transcript(video_id):
    """
    Fetches the Transcript for the given Youtube URL
    Args:
        link (_type_): _description_
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine transcript into a single string
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        raise RuntimeError(f"Could not the retrieve the Transcript: {e}")


def extract_summary(client, text):
    """Summarize the video transcription

    Args:
        client (_type_): _description_
        text (_type_): _description_
    """
    try:    
        response = client.chat.completions.create(
            model = MODEL_ID,
            temperature = 0,
            messages = [
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")
        

def extract_questions(client, text):
    response = client.chat.completions.create(
        model= MODEL_ID,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a questions generator designed to analyze a youtube video transcription, understand its content, and create a list of authentic, non-redundant questions. Your task is to identify key themes, ideas, facts, and implications in the text, crafting diverse questions that include factual, analytical, exploratory, reflective, and scenario-based types. Ensure all questions are meaningful, distinct, and encourage deeper thinking without repeating structure or content. Present the questions as a numbered list, each concise and directly tied to the transcription."
            },
            {
                "role": "user",
                "content": f"Craft questions for this transcript text: {text}"
            }
        ]
    )
    return response.choices[0].message.content.strip()


def process_retrieve_questions_task(client, url):
    video_id = extract_video_id(url)
    transcript = get_transcript(video_id)
    questions = extract_questions(client, transcript)
    return questions

def process_retrieve_summary_task(client, url):
    video_id = extract_video_id(url)
    transcription = get_transcript(video_id)
    summary = extract_summary(client, transcription)
    return summary