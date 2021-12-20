import {quizEvents, quizInput} from './events.js'

let websocket;

window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  websocket = new WebSocket("ws://localhost:8080/");
  addButtons()
  addInputEvents()
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

function addButtons() {
  const body = document.querySelector("#quiz-buttons");
  quizEvents.forEach(quizEvent => {
    const node = document.createElement('button')
    node.id = quizEvent.type
    node.appendChild(document.createTextNode(quizEvent.pretty))
    addButtonEvents(node, quizEvent)
    body.append(node)
  });
}

function addButtonEvents(element, {type, data}) {
  element.addEventListener('click', () => {
    sendMessage({type, data})
  });
}

function addInputEvents() {
  const input = document.querySelector('#quiz-input')
  input.addEventListener('input', event => {
    const message = event.target.value
    sendMessage({type: quizInput.type, data: quizInput.data(message)})
  })
}

function sendMessage(message) {
  const messageString = JSON.stringify(message)
  console.log('(sending) ', messageString)
  websocket.send(messageString)
}