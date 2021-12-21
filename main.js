import Server from './server.js'
import * as page from './page-elements.js'

let isHost = false
let roomCode = ''
let server;

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer());
    server = new Server(websocket, onServerOpen, onServerMessage)
});

function onServerOpen() {
    const params = new URLSearchParams(window.location.search);
    if (params.has("room")) server.joinRoom(params.get('room'))
    page.room.input.addEventListener('input', onRoomCode)
    page.room.button.addEventListener('click', onRoomButton)
    page.quizControls.info.addEventListener('click', server.quiz.info)
    page.quizControls.start.addEventListener('click', server.quiz.start)
    page.quizControls.end.addEventListener('click', server.quiz.end)
    page.quizControls.pause.addEventListener('click', server.quiz.pause)
    page.quizControls.unpause.addEventListener('click', server.quiz.unpause)
}

function onServerMessage({ data }) {
    const event = JSON.parse(data)
    switch (event.type) {
        case 'room created':
            isHost = true
            updateRoomCode(event.data)
            updateRoomButton()
            page.quizControls.buttons.style.display = 'grid'
            page.quizControls.title.style.display = 'unset'
            page.title.textContent += ' (Host)'
            break;
        case 'room joined':
            isHost = false
            updateRoomCode(event.data)
            page.room.button.remove()
            page.room.input.disabled = true
            page.room.label.hidden = false
            addInput()
            break;
        case 'room info':
            updateRoomCode(event.data.room.code)
            break;
        case 'player_joined':
            addInput(event.data)
            break;
        case 'player_left':
            const playerDiv = document.querySelector(`#${event.data}-div`)
            if (playerDiv) playerDiv.remove()
            break;
        case 'submit answer':
            const inputElement = document.querySelector(`#${event.player}`)
            inputElement.value = event.data;
            break;
    }
}

function updateRoomCode(code) {
    roomCode = code
    page.room.input.value = roomCode
}

function onRoomCode(event) {
    page.room.button.textContent = event.target.value ? 'Join Room' : 'Create Room'
}

function onRoomButton() {
    if (page.room.input.value) server.joinRoom(page.room.input.value)
    else server.createRoom()
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
    playerInput.addEventListener('input', event => {
        const inputValue = event.target.value
        server.submitAnswer(inputValue)
    })
    playerDiv.appendChild(playerLabel)
    playerDiv.appendChild(playerInput)
    page.quizInputs.div.appendChild(playerDiv)
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