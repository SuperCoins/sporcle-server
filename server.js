export default class Server {
    websocket;

    constructor(websocket, onOpen, onMessage) {
        this.websocket = websocket
        this.websocket.addEventListener('open', this.log)
        this.websocket.addEventListener('open', onOpen)
        this.websocket.addEventListener('message', this.log)
        this.websocket.addEventListener('message', onMessage)
    }

    log(event) {
        const type = `[${event.type}]`
        if (event.data) console.log(type, ' ', JSON.parse(event.data))
        else console.log(type)
    }

    createRoom() {
        this.sendMessage({ type: "create room" })
    }

    joinRoom(roomCode) {
        this.sendMessage({ type: "join room", data: roomCode })
    }

    submitAnswer(answer) {
        this.sendMessage({ type: "submit answer", data: answer })
    }

    get quiz() {
        return {
            info() { this.sendMessage({ type: "quiz info" }) },
            start() { this.sendMessage({ type: "quiz start" }) },
            end() { this.sendMessage({ type: "quiz end" }) },
            pause() { this.sendMessage({ type: "quiz pause" }) },
            unpause() { this.sendMessage({ type: "quiz unpause" }) },
        }
    }

    sendMessage(message) {
        const messageString = JSON.stringify(message)
        this.websocket.send(messageString)
        console.log('(sent) ', message)
    }
}

function log(eventType, event) {
    const type = `[${eventType}]`
    if (event.data) console.log(type, ' ', JSON.parse(event.data))
    else console.log(type)
}