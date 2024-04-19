import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai

load_dotenv()  # load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are YouTube video summarizer. You are capable of summarizing any kind of video whether it is educational or comedy or even if it is news or movies. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 to 500 words. If the video does not contain a transcription, then you have to generate it on your own. Please provide the summary of the text given here: """

# Getting the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[-1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        if transcript_text:
            transcript = ""
            for i in transcript_text:
                transcript += " " + i["text"]
            return transcript
        else:
            return None

    except Exception as e:
        raise e

# Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Initialize our Streamlit app
st.set_page_config(page_title="YouTube se padhai 📝🎥🔍📚", layout="centered", initial_sidebar_state="expanded")

# About the author
if st.button("About the author"):
    # Display information about the author or code description
    st.write("# About the Author")
    st.write("This Streamlit app is created by Rishi Ranjan.")
    st.write("""
    Date-->  19/04/2024
        🌟 **About Me:**
        https://www.linkedin.com/in/rishi-rih/

🚀 Hey there! I'm Rishi, a passionate 2nd year Computer Science & Engineering Undergraduate with a keen interest in the vast world of technology. Currently specializing in AI and Machine Learning, I'm on a perpetual quest for knowledge and thrive on learning new skills.

... (rest of the author's information)
    """)
    if st.button("close"):
        pass

st.header("YouTube se padhai -- Transcript to Detailed Notes Converter 📝🎥🔍📚")
st.write("Only able to work with those videos which have transcripts available")

youtube_link = st.text_input("Enter YouTube Video Link:")

if st.button("Get Detailed Notes"):
    if not youtube_link:
        st.error("Please enter a valid YouTube video link")
    else:
        transcript_text = extract_transcript_details(youtube_link)
        if not transcript_text:
            st.error("Transcript not available. Please enter a valid educational video link.")
        else:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
