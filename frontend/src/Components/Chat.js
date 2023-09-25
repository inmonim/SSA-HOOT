import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../App.css";

function Chat() {

  let { client_id } = useParams();

  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [receivedMessage, setReceivedMessage] = useState([]);

  useEffect(() => {
    const newSocket = new WebSocket(`${socket_url}`);

    newSocket.onopen = () => {
      console.log("WebSocket connected");
    };

    newSocket.onmessage = (event) => {
      const message = event.data;
      setReceivedMessage((prevMessages) => [...prevMessages, message]);
    };

    newSocket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [client_id]);

  useEffect(() => {
    console.log(`receivedMessage: ${receivedMessage}`);
  }, [receivedMessage])

  const sendMessage = () => {
    if (socket && message) {
      socket.send(message);
    }
  };

  return (
    <div className="Chat">
      <h1>WebSocket Chat (Client {client_id})</h1>
      <div>
        <p>Received Message: {receivedMessage}</p>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chat;