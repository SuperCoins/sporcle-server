export default class Room {
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

    create() {
        this.message({ type: "create room" })
    }

    join(roomCode, name) {
        this.message({ type: "join room", data: roomCode, player: name })
    }

    updateName(name) {
        this.message({ type: "update name", data: name })
    }

    answer(answer) {
        this.message({ type: "submit answer", data: answer })
    }

    answerResponse(response, answer, player) {
        this.message({ type: "answer response", data: { answer, player, response } })
    }

    get quiz() {
        return {
            info: () => {
                this.message({
                    type: "quiz info",
                    data: {
                        "name": "Anything but Zimbabwe",
                        "gameID": 630868,
                        "gameTypeID": 0,
                        "gameTimeSeconds": 360,
                        "autoGo": false,
                    }
                })
            },
            start: () => { this.message({ type: "quiz start" }) },
            end: () => { this.message({ type: "quiz end" }) },
            pause: () => { this.message({ type: "quiz pause" }) },
            unpause: () => { this.message({ type: "quiz unpause" }) },
        }
    }

    message(message) {
        const messageString = JSON.stringify(message)
        this.websocket.send(messageString)
        console.log('(sent) ', message)
    }
}
