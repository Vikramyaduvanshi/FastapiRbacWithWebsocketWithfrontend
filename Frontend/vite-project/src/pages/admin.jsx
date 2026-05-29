import { useEffect, useRef, useState } from "react";

export  function Admin() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const wsRef = useRef(null);

    useEffect(() => {

        // IMPORTANT:
        // withCredentials true is needed if cookies are used for JWT
        const ws = new WebSocket("ws://localhost:8000/chat/ws");

        wsRef.current = ws;

        ws.onopen = () => {
            console.log("WebSocket connected");
            addMessage("System: Connected");
        };

        ws.onmessage = (event) => {
            addMessage(event.data);
        };

        ws.onclose = () => {
            addMessage("System: Disconnected");
        };

        return () => {
            ws.close();
        };

    }, []);

    const addMessage = (msg) => {
        setMessages((prev) => [...prev, msg]);
    };

    const sendMessage = () => {
        if (!input.trim()) return;

        if (wsRef.current?.readyState === 1) {
            wsRef.current.send(input);
            setInput("");
        }
    };

    return (
        <div style={styles.container}>

            <h2>Trading WebSocket Chat</h2>

            <div style={styles.box}>
                {messages.map((m, i) => (
                    <div key={i} style={styles.msg}>
                        {m}
                    </div>
                ))}
            </div>

            <div style={styles.inputBox}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter message..."
                    style={styles.input}
                />

                <button onClick={sendMessage} style={styles.btn}>
                    Send
                </button>
            </div>

        </div>
    );
}

const styles = {
    container: {
        width: "100%",
        maxWidth: "600px",
        margin: "auto",
        padding: "20px",
        fontFamily: "Arial"
    },

    box: {
        height: "400px",
        overflowY: "auto",
        border: "1px solid #ccc",
        padding: "10px",
        borderRadius: "8px",
        marginBottom: "10px",
        background: "#0f172a",
        color: "white"
    },

    msg: {
        padding: "5px 0",
        borderBottom: "1px solid #1e293b"
    },

    inputBox: {
        display: "flex",
        gap: "10px"
    },

    input: {
        flex: 1,
        padding: "10px",
        borderRadius: "6px",
        border: "1px solid #ccc"
    },

    btn: {
        padding: "10px 15px",
        background: "#2563eb",
        color: "white",
        border: "none",
        borderRadius: "6px",
        cursor: "pointer"
    }
};