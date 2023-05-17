import streamlit as st
import time
import sounddevice as sd
from scipy.io.wavfile import write
import os
import boto3
import re
import urllib.request
import json
from dotenv import load_dotenv

def record_audio(duration, filename):
    fs = 44100  # Sample rate
    recordings_folder = "Interactions/Recordings"
    
    # Start recording
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    
    with st.spinner("Recording..."):
        # Display a progress bar while recording
        progress_bar = st.progress(0)
        for i in range((duration-1)*10):
            time.sleep(0.1)
            progress = (i + 1) / ((duration-1)*10)
            progress_bar.progress(progress)
            
    st.success("Recording complete!")
    
    # Save the recorded data as a WAV file in the "Recordings" folder
    if not os.path.exists(recordings_folder):
        os.makedirs(recordings_folder)
    write(os.path.join(recordings_folder, filename), fs, myrecording)

    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path to your .env file
    dotenv_path = os.path.join(current_dir, "..", ".env")

    # Load environment variables from the .env file
    load_dotenv(dotenv_path)
    
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    s3 = boto3.resource(
        's3',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name='eu-west-3'
    )

    bucket_name = 'interaction-recordings'
    file_path = f'{recordings_folder}/{filename}'
    object_key = f'Recordings/{filename}'

    s3.Bucket(bucket_name).upload_file(file_path, object_key)
    
    # Amazon Transcribe
    
    transcribe = boto3.client(
        'transcribe',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name='eu-west-3'
    )


    # remove all non-alphanumeric characters, except periods, underscores, and hyphens
    clean_filename = re.sub('[^0-9a-zA-Z._-]', '', filename)
    job_name = f'Transcribe-{clean_filename}'
    job_uri = f's3://{bucket_name}/{object_key}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )

    with st.spinner("Transcription in progress..."):
        
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            data = json.loads(response.read())
            transcript = data['results']['transcripts'][0]['transcript']

    return transcript