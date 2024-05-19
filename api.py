from flask import Flask, jsonify, Response, request
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyAnCTgML28HOlXrj05zy-IKOF-TlZ2cvhk'
CHANNEL_ID = 'UCBf6LAuCohAruHdZNCPH9Lg' 
MAX_RESULTS_PER_PAGE = 5 

def get_all_playlists():
    playlists = []
    next_page_token = None
    while True:
        url = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={CHANNEL_ID}&maxResults={MAX_RESULTS_PER_PAGE}&key={API_KEY}'
        if next_page_token:
            url += f'&pageToken={next_page_token}'
        response = requests.get(url)
        data = response.json()
        if 'items' in data:
            for item in data['items']:
                playlists.append(item)
        if 'nextPageToken' in data:
            next_page_token = data['nextPageToken']
        else:
            break
    return playlists

@app.route('/latest_video', methods=['GET'])
def get_latest_video():
    url = f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={CHANNEL_ID}&maxResults=1&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        video_title = data['items'][0]['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return Response(f'{video_title}: {video_url}', mimetype='text/plain')
    else:
        return Response('No videos found', mimetype='text/plain'), 404

@app.route('/playlists', methods=['GET'])
def get_playlists():
    playlist_name = request.args.get('name')
    if playlist_name:
        playlist_name = playlist_name.lower()  
        all_playlists = get_all_playlists()
        matched_playlists = []
        for playlist in all_playlists:
            item_name = playlist['snippet']['title'].lower()  
            if playlist_name in item_name:  
                playlist_id = playlist['id']
                playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
                matched_playlists.append(f'{item_name}: {playlist_url}')
        if matched_playlists:
            return Response("\n".join(matched_playlists), mimetype='text/plain')
        else:
            suggestions = difflib.get_close_matches(playlist_name, [playlist['snippet']['title'].lower() for playlist in all_playlists])
            return Response(f'Playlist not found. Suggestions: {", ".join(suggestions)}', mimetype='text/plain'), 404
    else:
        all_playlists = get_all_playlists()
        playlists = []
        for playlist in all_playlists:
            playlist_id = playlist['id']
            playlist_title = playlist['snippet']['title']
            playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
            playlists.append(f'{playlist_title}: {playlist_url}')
        return Response("\n".join(playlists), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
