document.addEventListener("DOMContentLoaded", () => {
    const socket = new WebSocket("ws://localhost:8766")
    socket.addEventListener("open", (event) => {
        console.log("Socket opened")
    });

    const container = document.getElementById("pos")
    socket.addEventListener("message", (event) => {
        container.innerText = event.data
    });
    socket.addEventListener("close", () => {
        console.log("Socket closed")
    })
})