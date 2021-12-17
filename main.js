import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".board");
  createBoard(board);
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://172.20.199.6:8001/");
  sendMoves(board, websocket);
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    // do something with event
    console.log(event)
  });
  websocket.addEventListener("open", ({ data }) => {
    // do something with event
    console.log(data)
  });
});

function sendMoves(board, websocket) {
  // When clicking a column, send a "play" event for a move in that column.
  board.addEventListener("click", ({ target }) => {
    const column = target.dataset.column;
    // Ignore clicks outside a column.
    if (column === undefined) {
      return;
    }
    const event = {
      type: "play",
      column: parseInt(column, 10),
    };
    websocket.send(JSON.stringify(event));
  });
}