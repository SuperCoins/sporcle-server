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
    if (params.has("host")) updateHostStatus(true)
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
            updateRoomCode(event.data)
            updateHostStatus(true)
            break;
        case 'room joined':
            updateRoomCode(event.data)
            updateHostStatus(false)
            page.room.button.remove()
            page.room.input.disabled = true
            page.name.input.value = event.player
            players.push(page.createPlayer(event.player, room, false))
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
    playersToAdd.forEach(playerName => players.push(page.createPlayer(playerName, room, true)))
}

function updatePlayerBox(playerName) {
    players.forEach(player => player.remove())
    players.push(page.createPlayer(playerName, room, false))
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

function onNameUpdate(event) {
    if (!roomCode) return
    room.updateName(event.target.value)
}

function updateHostStatus(newIsHost) {
    isHost = newIsHost
    if (isHost) {
        page.room.input.disabled = true
        page.name.input.value = 'HOST'
        page.name.input.disabled = true
        page.room.buttonControl.hidden = true
        page.room.connectControl.hidden = false
        page.room.connectTag.href = `?room=${roomCode}`
        page.quizControls.panel.hidden = false
    }
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
