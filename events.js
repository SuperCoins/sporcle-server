const quiz_loaded = {
    type: "quiz_loaded",
    pretty: "Load the quiz",
};
const quiz_start = {
    type: "quiz_start",
    pretty: "Start the quiz",
};
const quiz_end = {
    type: "quiz_end",
    pretty: "End the quiz",
};
const quiz_pause = {
    type: "quiz_pause",
    pretty: "Pause the quiz",
};
const quiz_unpause = {
    type: "quiz_unpause",
    pretty: "Unpause the quiz",
};

export const quizEvents = [
    quiz_loaded,
    quiz_start,
    quiz_end,
    quiz_pause,
    quiz_unpause,
];

export const quizInput = {
    type: "answer",
    pretty: "What's the answer?",
    data(input) {
        return input;
    }
}

export const createRoom = {
    type: "create room"
}

export const joinRoom = {
    type: "join room",
    data(roomCode) {
        return roomCode
    }
}