import {quizEvents} from './events.js'

window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8080/");
  addButtons(websocket)
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data)
    // do something with event
    console.log('[message] ', event)
  });
  websocket.addEventListener("open", ({ data }) => {
    // do something with event
    console.log('[open] ', data)
  });
});

function addButtons(websocket) {
  const body = document.querySelector("body");
  quizEvents.forEach(quizEvent => {
    const node = document.createElement('button')
    node.id = quizEvent.type
    node.appendChild(document.createTextNode(quizEvent.pretty))
    // (`<button id="${quizEvent.type}">${quizEvent.pretty}</button>`);
    buttonEvent(node, quizEvent, websocket)
    body.append(node)
  });
}

function buttonEvent(element, {type, data}, websocket) {
  element.addEventListener('click', () => {
    const event = JSON.stringify({type, data});
    console.log('(sending) ', event)
    websocket.send(event)
  });
}