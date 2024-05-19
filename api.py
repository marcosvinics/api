from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyAnCTgML28HOlXrj05zy-IKOF-TlZ2cvhk'
CHANNEL_ID = 'UCBf6LAuCohAruHdZNCPH9Lg'  

@app.route('/latest_video', methods=['GET'])
def get_latest_video():
    url = f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={CHANNEL_ID}&maxResults=1&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        video_title = data['items'][0]['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return jsonify({video_title: video_url})
    else:
        return jsonify({'error': 'No videos found'}), 404

if __name__ == '__main__':
    app.run(debug=True)