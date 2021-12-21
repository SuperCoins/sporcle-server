import { createRoom as createRoomMessage, joinRoom as joinRoomMessage, quizEvents, quizInput } from './events.js'
import * as page from './page-elements.js'

let isHost = false
let roomCode = ''

let websocket;

window.addEventListener("DOMContentLoaded", () => {
    websocket = new WebSocket(getWebSocketServer());
    websocket.addEventListener('open', event => {
        console.log('[open] ', event.data)
        readUrlParams()
        onRoomCode()
        onRoomButton()
        addButtons()
        handleMessage()
    })
});

function readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has("room")) joinRoom(params.get('room'))
}

function updateRoomCode(code) {
    roomCode = code
    page.room.input.value = roomCode
}

function onRoomCode() {
    page.room.input.addEventListener('input', event => {
        const inputValue = event.target.value
        page.room.button.textContent = inputValue ? 'Join Room' : 'Create Room'
    })
}

function onRoomButton() {
    page.room.button.addEventListener('click', () => {
        if (page.room.input.value) joinRoom(page.room.input.value)
        else createRoom()
    })
}

function removeRoomButton() {
    page.room.button.remove()
    page.room.input.disabled = true
    page.room.label.hidden = false
}

function updateRoomButton() {
    page.room.input.disabled = true
    page.room.label.hidden = false
    page.connect.tag.id = 'room-button'
    page.connect.tag.href = `?room=${roomCode}`
    page.connect.tag.target = '_blank'
    page.connect.button.textContent = 'Connect to Room'
    page.connect.tag.appendChild(page.connect.button)
    page.room.button.replaceWith(page.connect.tag)
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
        page.title.textContent += ' (Host)'
    }
}

function updateHostView() {
    page.quizControls.buttons.style.display = 'grid'
    page.quizControls.title.style.display = 'unset'
}

function handleMessage() {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data)
        console.log('[message] ', event)
        switch (event.type) {
            case 'room created':
                isHost = true
                updateRoomCode(event.data)
                updateRoomButton()
                updateHostView()
                updateTitle()
                break;
            case 'room joined':
                isHost = false
                updateRoomCode(event.data)
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
    quizEvents.forEach(quizEvent => {
        const node = document.createElement('button')
        node.id = quizEvent.type
        node.appendChild(document.createTextNode(quizEvent.pretty))
        addButtonEvents(node, quizEvent)
        page.quizControls.buttons.append(node)
    });
}

function addButtonEvents(element, { type, data }) {
    element.addEventListener('click', () => {
        sendMessage({ type, data })
    });
}

function addInput(name = '') {
    const playerNumber = page.quizInputs.div.childElementCount + 1
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
    page.quizInputs.div.appendChild(playerDiv)
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