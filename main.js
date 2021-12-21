import { createRoom as createRoomMessage, joinRoom as joinRoomMessage, quizEvents, quizInput } from './events.js'

let isHost = false
let roomCode = ''

let websocket;

window.addEventListener("DOMContentLoaded", () => {
    websocket = new WebSocket(getWebSocketServer());
    readUrlParams()
    onOpen()
    onRoomCode()
    onRoomButton()
    addButtons()
    handleMessage()
});

function readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has("room")) joinRoom(params.get('room'))
}

function updateRoomCode(code) {
    roomCode = code
    const roomCodeInput = document.querySelector('#room-code')
    roomCodeInput.value = roomCode
}

function onOpen() {
    websocket.addEventListener("open", ({ data }) => {
        console.log('[open] ', data)
    });
}

function onRoomCode() {
    const roomCodeInput = document.querySelector('#room-code')
    const roomButton = document.querySelector('#room-button')
    roomCodeInput.addEventListener('input', event => {
        const inputValue = event.target.value
        roomButton.textContent = inputValue ? 'Join Room' : 'Create Room'
    })
}

function onRoomButton() {
    const roomButton = document.querySelector('#room-button')
    const roomCodeInput = document.querySelector('#room-code')
    roomButton.addEventListener('click', () => {
        if (roomCodeInput.value) joinRoom(roomCodeInput.value)
        else createRoom()
    })
}

function removeRoomButton() {
    const roomButton = document.querySelector('#room-button')
    roomButton.remove()
    const roomCodeInput = document.querySelector('#room-code')
    roomCodeInput.disabled = true
    const roomCodeLabel = document.querySelector('#room-label')
    roomCodeLabel.hidden = false
}

function createRoom() {
    const message = {
        type: createRoomMessage.type
    }
    sendMessage(message)
}

function joinRoom(roomCode) {
    const message = {
        type: joinRoomMessage.type,
        data: joinRoomMessage.data(roomCode)
    }
    sendMessage(message)
}

function updateTitle() {
    if (isHost) {
        const title = document.querySelector('#title')
        title.textContent += ' (Host)'
    }
}

function updateHostView() {
    const buttons = document.querySelector('#control-buttons')
    buttons.style.display = 'grid'
    const title = document.querySelector('#control-title')
    title.style.display = 'unset'
}

function handleMessage() {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data)
        console.log('[message] ', event)
        switch (event.type) {
            case 'room created':
                isHost = true
                removeRoomButton()
                updateHostView()
                updateTitle()
                break;
            case 'room joined':
                isHost = false
                removeRoomButton()
                addInput()
                break;
            case 'room info':
                updateRoomCode(event.data.room.code)
                break;
            case 'player_joined':
                addInput(event.data)
                break;
            case 'player_left':
                removeInput(event.data)
                break;
            case 'answer':
                updateAnswer(event.data, event.player)
                break;
        }
    });
}

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

function addButtonEvents(element, { type, data }) {
    element.addEventListener('click', () => {
        sendMessage({ type, data })
    });
}

function addInput(name = '') {
    const inputDiv = document.querySelector('#inputs')
    const playerNumber = inputDiv.childElementCount + 1
    const playerIdentifier = name || `player-${playerNumber}`
    const playerDiv = document.createElement('div')
    playerDiv.className = 'player-input'
    playerDiv.id = `${playerIdentifier}-div`
    const playerLabel = document.createElement('label')
    playerLabel.appendChild(document.createTextNode(`${playerIdentifier}: `))
    const playerInput = document.createElement('input')
    playerInput.id = playerIdentifier
    playerInput.placeholder = "What's the answer?"
    playerInput.disabled = isHost
    addInputEvent(playerInput)
    playerDiv.appendChild(playerLabel)
    playerDiv.appendChild(playerInput)
    inputDiv.appendChild(playerDiv)
}

function removeInput(name = '') {
    const playerDiv = document.querySelector(`#${name}-div`)
    if (playerDiv) playerDiv.remove()
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

function updateAnswer(answer, player) {
    const inputElement = document.querySelector(`#${player}`)
    inputElement.value = answer;
}

function sendMessage(message) {
    const messageString = JSON.stringify(message)
    websocket.send(messageString)
    console.log('(sent) ', message)
}

function getWebSocketServer() {
    if (window.location.host === "supercoins.github.io") {
        return "wss://sporcle-together.herokuapp.com/";
    } else if (window.location.host === "localhost:8000") {
        return "ws://localhost:8080/";
    } else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}