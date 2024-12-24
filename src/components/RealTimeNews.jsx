import { useState, useEffect } from "react";
import axios from "axios"; // For making HTTP requests

const RealTimeNews = () => {
  const [news, setNews] = useState([]);
  const [error, setError] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0); // State to track the current news card index
  const [isNewsVisible, setIsNewsVisible] = useState(false); // To toggle visibility of news

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get("http://localhost:7070/real-time-news", {
          params: {
            query: "farming", // Change query as needed
            page_size: 5, // Number of articles to fetch
          },
        });
        setNews(response.data.news);
      } catch (err) {
        setError("Error fetching news",err);
      }
    };

    fetchNews();
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  const handleNextCard = () => {
    if (currentIndex < news.length - 1) {
      setCurrentIndex(currentIndex + 1); // Move to the next news card
    } else {
      setCurrentIndex(0); // Loop back to the first news card
    }
  };

  return (
    <div className="news-dashboard">
      <h2>Real-Time News</h2>

      {/* News Box - Clickable */}
      <div 
        className="news-box" 
        onClick={() => setIsNewsVisible(!isNewsVisible)} // Toggle news visibility
      >
        <h3>{isNewsVisible ? "Hide News" : "Show News"}</h3>
      </div>

      {/* Display the news card horizontally */}
      {isNewsVisible && news.length > 0 && (
        <div className="news-container">
          <div className="news-card">
            <h3>{news[currentIndex].title}</h3>
            <p>{news[currentIndex].description}</p>
            <p><strong>Source:</strong> {news[currentIndex].source}</p>
            <p><strong>Published At:</strong> {new Date(news[currentIndex].published_at).toLocaleString()}</p>
            <a href={news[currentIndex].url} target="_blank" rel="noopener noreferrer">Read more</a>
          </div>
        </div>
      )}

      {/* Button to switch to the next card */}
      {isNewsVisible && (
        <button className="next-btn" onClick={handleNextCard}>
          Next News
        </button>
      )}
    </div>
  );
};

export default RealTimeNews;
