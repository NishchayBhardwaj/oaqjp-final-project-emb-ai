import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = { "raw_document": { "text": text_to_analyze } }

    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_json = response.json()

            # Extract the emotions and their scores
            emotions = response_json.get("emotion_predictions", [])
            emotion_scores = {
                "anger": 0,
                "disgust": 0,
                "fear": 0,
                "joy": 0,
                "sadness": 0
            }

            # Update scores for relevant emotions
            for emotion in emotions:
                if emotion['emotion'] in emotion_scores:
                    emotion_scores[emotion['emotion']] = emotion['score']

            # Find the dominant emotion
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            # Return the required output format
            return {
                'anger': emotion_scores['anger'],
                'disgust': emotion_scores['disgust'],
                'fear': emotion_scores['fear'],
                'joy': emotion_scores['joy'],
                'sadness': emotion_scores['sadness'],
                'dominant_emotion': dominant_emotion
            }
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
