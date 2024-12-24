import Carousel from "react-bootstrap/Carousel";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS for styling

function Home() {
  // Slides data for the carousel
  const slides = [
    {
      text: "First slide",
      src: "/src/assets/homenew.jpeg",
      label: "Harvest Analytics",
      description: "Predicting Prices of Commodities ",
    },
    {
      text: "Second slide",
      src: "/src/assets/homeui3.jpeg",
      label: "Your Smart Agricultural Assistant - Krishi Chat",
      description: "Krishi Chat is an interactive, farmer-focused chatbot designed to provide real-time assistance and guidance. It serves as a bridge between farmers and agricultural knowledge, offering insights into crop management, market trends, and tailored solutions to agricultural challenges. ",
    },
    {
      text: "Third slide",
      src: "/src/assets/homeui2.jpg",
      label: "Smart Crop Insights: Grow What Thrives",
      description:
        "The Crop Recommendation feature empowers farmers by analyzing soil conditions, climatic factors, and regional suitability to suggest the most profitable and sustainable crops to cultivate. With data-driven insights, it ensures optimal resource utilization and maximizes agricultural output.",


    },
  ];

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        overflow: "hidden",
      }}
    >
      {/* Fullscreen Carousel */}
      <Carousel style={{ height: "100%", width: "100%" }}>
        {slides.map((slide, index) => (
          <Carousel.Item key={index} style={{ height: "100%" }}>
            {/* Fullscreen Image */}
            <img
              className="d-block w-100"
              src={slide.src}
              alt={slide.text}
              style={{
                height: "100vh", // Full viewport height
                width: "100vw", // Full viewport width
                objectFit: "cover", // Ensures the image covers the entire viewport
              }}
            />
            {/* Caption */}
            <Carousel.Caption>
              <h3>{slide.label}</h3>
              <p>{slide.description}</p>
            </Carousel.Caption>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
}

export default Home;