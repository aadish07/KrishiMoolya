from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your News API key (replace with your actual API key)
API_KEY = "ade15208349440759c397f57935b64f1"  # your actual News API key
BASE_URL = "https://newsapi.org/v2/everything"

@app.route('/real-time-news', methods=['GET'])
def get_real_time_news():
    # Get the search query (e.g., "farming", "crop prices")
    query = request.args.get('query', 'farming')  # Default to 'farming' if no query is provided

    # Get the number of articles to fetch (e.g., top 5)
    page_size = int(request.args.get('page_size', 5))  # Default to 5 articles

    # Make request to News API
    try:
        response = requests.get(
            BASE_URL,
            params={
                'apiKey': API_KEY,        # API Key
                'q': query,               # Search term (real-time news related to 'query')
                'language': 'en',         # Filter by English language
                'pageSize': page_size,    # Limit the number of articles
                'sortBy': 'publishedAt'   # Sort by most recent articles
            }
        )

        if response.status_code == 200:
            data = response.json()
            # Check if there are news articles
            if 'articles' not in data or not data['articles']:
                return jsonify({'error': 'No real-time news found'}), 404

            # Process the articles
            articles = [
                {
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'published_at': article['publishedAt'],
                    'source': article['source']['name'],
                }
                for article in data['articles']
            ]
            return jsonify({'news': articles})

        else:
            # Return error message with status code
            return jsonify({'error': f"Unable to fetch real-time news. Status Code: {response.status_code}"}), 500

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return jsonify({'error': f'An error occurred while fetching real-time news: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7070)
