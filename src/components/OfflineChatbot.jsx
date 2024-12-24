import { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false); // Control chatbot visibility
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // Handle user sending a message
  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user's message to chat
    setMessages((prev) => [...prev, { sender: "user", text: input }]);

    try {
      const response = await axios.post("http://localhost:4040/query", {
        message: input,
      });

      // Add chatbot's response to chat
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: response.data.response },
      ]);
    } catch (error) {
      console.error("Error communicating with the chatbot:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error connecting to the chatbot." },
      ]);
    }
    

    // Clear input field
    setInput("");
  };

  return (
    <div>
      {/* Chatbot Toggle Button */}
      <div
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          cursor: "pointer",
        }}
        onClick={() => setIsOpen(!isOpen)}
      >
        <img
          src="src\assets\logoChatbot.png" // Replace with your chatbot logo path
          alt="Chatbot Logo"
          style={{ width: "50px", height: "50px" , borderRadius: "2px" , padding: "5px"}}
        />
      </div>

      {/* Chatbot UI */}
      {isOpen && (
        <div
          style={{
            position: "fixed",
            bottom: "80px",
            right: "20px",
            width: "300px",
            height: "400px",
            backgroundColor: "#fff",
            border: "1px solid #ccc",
            borderRadius: "10px",
            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.2)",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              flex: 1,
              padding: "10px",
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  textAlign: msg.sender === "user" ? "right" : "left",
                  margin: "10px 0",
                }}
              >
                <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong>{" "}
                {msg.text}
              </div>
            ))}
          </div>
          <div
            style={{
              display: "flex",
              padding: "10px",
              borderTop: "1px solid #ccc",
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              style={{
                flex: 1,
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
                marginRight: "10px",
              }}
            />
            <button
              onClick={handleSendMessage}
              style={{
                padding: "10px 20px",
                backgroundColor: "#50C878",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
