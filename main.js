import {quizEvents, quizInput} from './events.js'

let websocket;

window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  websocket = new WebSocket("ws://localhost:8080/");
  addButtons()
  addNewPlayerEvent()
  addInput()
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
  const controlButtonsDiv = document.querySelector("#control-buttons");
  quizEvents.forEach(quizEvent => {
    const node = document.createElement('button')
    node.id = quizEvent.type
    node.appendChild(document.createTextNode(quizEvent.pretty))
    addButtonEvents(node, quizEvent)
    controlButtonsDiv.append(node)
  });
}

function addButtonEvents(element, {type, data}) {
  element.addEventListener('click', () => {
    sendMessage({type, data})
  });
}

function addInput() {
  const inputDiv = document.querySelector('#inputs')
  const playerNumber = inputDiv.childElementCount + 1
  const playerDiv = document.createElement('div')
  playerDiv.className = 'player-input'
  const playerLabel = document.createElement('label')
  playerLabel.appendChild(document.createTextNode(`Player ${playerNumber}: `))
  const playerInput = document.createElement('input')
  playerInput.id = `player-${playerNumber}`;
  playerInput.placeholder = "What's the answer?"
  addInputEvent(playerInput)
  playerDiv.appendChild(playerLabel)
  playerDiv.appendChild(playerInput)
  inputDiv.appendChild(playerDiv)
}

function addInputEvent(node) {
  node.addEventListener('input', event => {
    const inputValue = event.target.value
    const message = {
      type: quizInput.type,
      data: quizInput.data(inputValue),
      player: node.id,
    }
    sendMessage(message)
  })
}

function addNewPlayerEvent() {
  const element = document.querySelector('#add-player')
  element.addEventListener('click', () => {
    addInput()
  });
}

function sendMessage(message) {
  const messageString = JSON.stringify(message)
  websocket.send(messageString)
  console.log('(sent) ', message)
}