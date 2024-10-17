from youtube_transcript_api import YouTubeTranscriptApi

# Replace with your YouTube video ID
video_id = 'oGBmEK_FwXQ'

# Fetch the transcript
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Save the transcript to a text file
    with open('youtube_transcript.txt', 'w', encoding='utf-8') as f:
        for entry in transcript:
            f.write(f"{entry['start']} - {entry['duration']}: {entry['text']}\n")

    print("Transcript saved successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
