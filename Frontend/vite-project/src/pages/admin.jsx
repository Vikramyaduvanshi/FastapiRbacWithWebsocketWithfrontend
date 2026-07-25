import { useEffect, useRef, useState } from "react";

export function Admin() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const wsRef = useRef(null);
    const messagesEndRef = useRef(null); 

    // Auto-scroll to the bottom when messages update
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // IMPORTANT:
        // withCredentials true is needed if cookies are used for JWT
        const ws = new WebSocket("ws://localhost:8000/chat/ws");
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("WebSocket connected");
            addMessage({ text: "System: Connected to server", type: "system" });
        };

        ws.onmessage = (event) => {
            addMessage({ text: event.data, type: "incoming" });
        };

        ws.onclose = () => {
            addMessage({ text: "System: Disconnected from server", type: "system" });
        };

        return () => {
            ws.close();
        };
    }, []);

    const addMessage = (msgObj) => {
        // Store messages as objects containing the text and type
        setMessages((prev) => [...prev, msgObj]);
    };

    const sendMessage = () => {
        if (!input.trim()) return;

        if (wsRef.current?.readyState === 1) {
            wsRef.current.send(input);
            addMessage({ text: input, type: "outgoing" }); // Show your own message locally
            setInput("");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    };

    return (
        <div style={styles.fullscreenContainer}>
            {/* Header */}
            <header style={styles.header}>
                <div style={styles.statusContainer}>
                    <div style={styles.statusDot}></div>
                    <h2 style={styles.title}>Trading WebSocket Chat</h2>
                </div>
                <span style={styles.badge}>Admin Console</span>
            </header>

            {/* Chat Messages Feed */}
            <div style={styles.chatFeed}>
                {messages.map((m, i) => {
                    if (m.type === "system") {
                        return (
                            <div key={i} style={styles.systemMsg}>
                                {m.text}
                            </div>
                        );
                    }
                    return (
                        <div 
                            key={i} 
                            style={{
                                ...styles.msgWrapper,
                                justifyContent: m.type === "outgoing" ? "flex-end" : "flex-start"
                            }}
                        >
                            <div style={{
                                ...styles.msgBubble,
                                ...(m.type === "outgoing" ? styles.outgoingBubble : styles.incomingBubble)
                            }}>
                                {m.text}
                            </div>
                        </div>
                    );
                })}
                <div ref={messagesEndRef} />
            </div>

            {/* Footer Input Area */}
            <footer style={styles.footer}>
                <div style={styles.inputWrapper}>
                    <input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type a trading command or message..."
                        style={styles.input}
                    />
                    <button onClick={sendMessage} style={styles.btn}>
                        Send
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </footer>
        </div>
    );
}

// Sleek Slate/Indigo Styling Framework
const styles = {
    fullscreenContainer: {
        display: "flex",
        flexDirection: "column",
        width: "100vw",
        height: "100vh",
        backgroundColor: "#0f172a", // Slate 900
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        overflow: "hidden",
        boxSizing: "border-box"
    },

    header: {
        display: "flex",
        alignItems: "center",
        justifyContent: "between",
        justifyContent: "space-between",
        padding: "16px 24px",
        backgroundColor: "#1e293b", // Slate 800
        borderBottom: "1px solid #334155", // Slate 700
    },

    statusContainer: {
        display: "flex",
        alignItems: "center",
        gap: "10px"
    },

    statusDot: {
        width: "8px",
        height: "8px",
        backgroundColor: "#10b981", // Emerald 500 (Live Indicator)
        borderRadius: "50%",
        boxShadow: "0 0 8px #10b981"
    },

    title: {
        margin: 0,
        fontSize: "1.1rem",
        fontWeight: "600",
        color: "#f8fafc" // Slate 50
    },

    badge: {
        fontSize: "0.75rem",
        backgroundColor: "#3b82f6", // Blue 500
        color: "white",
        padding: "4px 8px",
        borderRadius: "4px",
        fontWeight: "bold",
        textTransform: "uppercase",
        letterSpacing: "0.05em"
    },

    chatFeed: {
        flex: 1,
        padding: "24px",
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        backgroundColor: "#0f172a",
    },

    systemMsg: {
        alignSelf: "center",
        fontSize: "0.8rem",
        color: "#94a3b8", // Slate 400
        backgroundColor: "#1e293b",
        padding: "4px 12px",
        borderRadius: "12px",
        margin: "8px 0",
        fontStyle: "italic",
        border: "1px solid #334155"
    },

    msgWrapper: {
        display: "flex",
        width: "100%",
    },

    msgBubble: {
        maxWidth: "70%",
        padding: "12px 16px",
        borderRadius: "12px",
        fontSize: "0.95rem",
        lineHeight: "1.4",
        wordBreak: "break-word",
        boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)"
    },

    incomingBubble: {
        backgroundColor: "#1e293b", // Slate 800
        color: "#f1f5f9", // Slate 100
        borderBottomLeftRadius: "2px",
        border: "1px solid #334155"
    },

    outgoingBubble: {
        backgroundColor: "#2563eb", // Blue 600
        color: "#ffffff",
        borderBottomRightRadius: "2px"
    },

    footer: {
        padding: "16px 24px",
        backgroundColor: "#1e293b",
        borderTop: "1px solid #334155",
    },

    inputWrapper: {
        display: "flex",
        maxWidth: "1200px",
        margin: "0 auto",
        gap: "12px",
        width: "100%"
    },

    input: {
        flex: 1,
        padding: "14px 16px",
        backgroundColor: "#0f172a",
        border: "1px solid #475569", // Slate 600
        borderRadius: "8px",
        color: "#f8fafc",
        fontSize: "0.95rem",
        outline: "none",
        transition: "border-color 0.2s",
    },

    btn: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        padding: "0 24px",
        backgroundColor: "#2563eb",
        color: "white",
        border: "none",
        borderRadius: "8px",
        fontSize: "0.95rem",
        fontWeight: "500",
        cursor: "pointer",
        transition: "background-color 0.2s",
    }
};