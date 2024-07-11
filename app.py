from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Example anime API base URL (replace with your chosen anime API)
ANIME_API_BASE_URL = "https://api.jikan.moe/v3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_anime', methods=['GET'])
def search_anime():
    anime_name = request.args.get('anime_name')
    if not anime_name:
        return jsonify({'error': 'Anime name not provided'}), 400
    
    # Example: Searching anime using Jikan API
    search_url = f"{ANIME_API_BASE_URL}/search/anime?q={anime_name}"
    response = requests.get(search_url)
    if response.status_code == 200:
        anime_data = response.json().get('results', [])
        return jsonify(anime_data)
    else:
        return jsonify({'error': 'Failed to fetch anime data'}), 500

@app.route('/get_stream_url', methods=['GET'])
def get_stream_url():
    anime_id = request.args.get('anime_id')
    if not anime_id:
        return jsonify({'error': 'Anime ID not provided'}), 400
    
    # Example: Fetching anime details and streaming URL using Jikan API
    anime_url = f"{ANIME_API_BASE_URL}/anime/{anime_id}/episodes"
    response = requests.get(anime_url)
    if response.status_code == 200:
        anime_episodes = response.json().get('episodes', [])
        # For simplicity, assuming first episode URL here
        if anime_episodes:
            stream_url = anime_episodes[0].get('video_url')
            if stream_url:
                return jsonify({'stream_url': stream_url})
            else:
                return jsonify({'error': 'Streaming URL not found'}), 404
        else:
            return jsonify({'error': 'No episodes found for the anime'}), 404
    else:
        return jsonify({'error': 'Failed to fetch anime details'}), 500

if __name__ == '__main__':
    app.run(debug=True)
