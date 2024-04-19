import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You are capable of summerize any kind of video whether it is an educational or comedy or even it is a news or movies. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 to 500 words. If the video does not contain transcription then you have to generate by your own. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text
##initialize our streamlit app

st.set_page_config(page_title="You Tube se padhai  📝🎥🔍📚", layout="centered", initial_sidebar_state="expanded")
#abou the author
if st.button("About the author"):
    # Display information about the author or code description
    st.write("# About the Author")
    st.write("This Streamlit app is created by Rishi Ranjan.")
    st.write("""
    Date-->  19/04/2024
        🌟 **About Me:**
        https://www.linkedin.com/in/rishi-rih/

🚀 Hey there! I'm Rishi, a passionate 2nd year Computer Science & Engineering Undergraduate with a keen interest in the vast world of technology. Currently specializing in AI and Machine Learning, I'm on a perpetual quest for knowledge and thrive on learning new skills.

💻 My journey in the tech realm revolves around programming, problem-solving, and staying on the cutting edge of emerging technologies. With a strong foundation in Computer Science, I'm driven by the exciting intersection of innovation and research.

🔍 Amidst the digital landscape, I find myself delving into the realms of Blockchain, crafting Android Applications, and ML projects.
 JAVA and Python . 
My GitHub profile (https://github.com/RiH-137) showcases my ongoing commitment to refining my craft and contributing to the tech community.

🏎️ Outside the digital realm, I'm a fervent Formula 1 enthusiast, experiencing the thrill of high-speed pursuits. When I'm not immersed in code or cheering for my favorite F1 team, you might find me strategizing moves on the chessboard.

📧 Feel free to reach out if you're as passionate about technology as I am. You can connect with me at 101rishidsr@gmail.com.

Let's build, innovate, and explore the limitless possibilities of technology together! 🌐✨
        
    
    """)
    if st.button("close"):
        pass






st.header("You Tube is padhai-- Transcript to Detailed Notes Converter 📝🎥🔍📚")
st.write("Only able to work with those videos which have transcript available")



youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    if "youtube.com" not in youtube_link:
        st.error("Please enter a valid YouTube video link")
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    
if st.button("Get Detailed Notes"):
    if not youtube_link:
        st.error("Please enter a valid YouTube video link")
    if youtube_link:
        transcript_text=extract_transcript_details(youtube_link)

        transcript_text!=extract_transcript_details(youtube_link)
        st.error("Enter the valid youtube video link that contains the transcript.")
    else:
        st.error("It is not an educational video. Please enter a valid educational video link")

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)




