export const title = document.querySelector('#title')

export const room = {
    input: document.querySelector('#room-code'),
    button: document.querySelector('#room-button'),
    label: document.querySelector('#room-label')
}

export const connect = {
    tag: document.createElement('a'),
    button: document.createElement('button'),
}

export const quizControls = {
    title: document.querySelector('#control-title'),
    loaded: document.querySelector('#quiz-loaded'),
    start: document.querySelector('#quiz-start'),
    end: document.querySelector('#quiz-end'),
    pause: document.querySelector('#quiz-pause'),
    unpause: document.querySelector('#quiz-unpause'),
    buttons: document.querySelector('#control-buttons'),
}

export const quizInputs = {
    title: document.querySelector('#input-title'),
    div: document.querySelector('#inputs')
}