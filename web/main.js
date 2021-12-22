import Room from './room.js'
import * as page from './page-elements.js'

let isHost = false
let roomCode = ''
let room;
let players = []

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer());
    room = new Room(websocket, onServerOpen, onServerMessage)
});

function onServerOpen() {
    const params = new URLSearchParams(window.location.search);
    if (params.has("room")) room.join(params.get('room'))
    page.room.input.addEventListener('input', onRoomCode)
    page.room.button.addEventListener('click', onRoomButton)
    page.name.input.addEventListener('input', onNameUpdate)
    page.quizControls.info.addEventListener('click', room.quiz.info)
    page.quizControls.start.addEventListener('click', room.quiz.start)
    page.quizControls.end.addEventListener('click', room.quiz.end)
    page.quizControls.pause.addEventListener('click', room.quiz.pause)
    page.quizControls.unpause.addEventListener('click', room.quiz.unpause)
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
            page.name.label.hidden = false
            break;
        case 'room joined':
            isHost = false
            updateRoomCode(event.data)
            page.room.button.remove()
            page.room.input.disabled = true
            page.room.label.hidden = false
            page.name.label.hidden = false
            page.name.input.value = event.player
            addPlayer(event.player, false)
            break;
        case 'name updated':
            page.name.input.value = event.data
            updatePlayerBox(event.data)
            break;
        case 'room info':
            updateRoomCode(event.data.room.code)
            if (isHost) updatePlayerList(event.data.players)
            break;
        case 'submit answer':
            const inputElement = document.querySelector(`#${event.player}`)
            inputElement.value = event.data;
            break;
    }
}

function updatePlayerList(playerList) {
    players = players.reduce((acc, player) => {
        if (!playerList.includes(player.name)) player.remove()
        else acc.push(player)
        return acc
    }, [])
    const playerNames = players.map(player => player.name)
    const playersToAdd = playerList.filter(playerName => !playerNames.includes(playerName))
    playersToAdd.forEach(playerName => addPlayer(playerName))
}

function updatePlayerBox(playerName) {
    players.forEach(player => player.remove())
    addPlayer(playerName, false)
}

function updateRoomCode(code) {
    roomCode = code
    page.room.input.value = roomCode
}

function onRoomCode(event) {
    page.room.button.textContent = event.target.value ? 'Join Room' : 'Create Room'
}

function onRoomButton() {
    if (page.room.input.value) room.join(page.room.input.value, page.name.input.value)
    else room.create()
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

function onNameUpdate(event) {
    if (!roomCode) return
    room.updateName(event.target.value)
}

function addPlayer(playerName, readOnly = true) {
    const player = {
        div: document.createElement('div'),
        label: document.createElement('label'),
        input: document.createElement('input'),
        correct: document.createElement('button'),
        name: playerName,
        remove() { this.div.remove() }
    }
    player.div.className = 'player-div'
    player.div.id = `${playerName}-div`
    player.label.textContent = `${playerName}: `
    player.input.id = playerName
    player.input.placeholder = "What's the answer?"
    player.input.disabled = readOnly
    player.input.addEventListener('input', ({ target }) => room.answer(target.value))
    player.correct.id = `${playerName}-answer`
    player.correct.textContent = 'Correct'
    player.correct.addEventListener('click', () => room.answerResponse('correct', player.input.value, playerName))
    player.div.appendChild(player.label)
    player.div.appendChild(player.input)
    if (isHost) player.div.appendChild(player.correct)
    page.quizInputs.div.appendChild(player.div)
    players.push(player)
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
