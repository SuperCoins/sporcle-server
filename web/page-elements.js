export const title = document.querySelector('#title')

export const room = {
    input: document.querySelector('#room-code'),
    button: document.querySelector('#room-button'),
    buttonControl: document.querySelector('#room-button-control'),
    connectControl: document.querySelector('#connect-room-control'),
    connectTag: document.querySelector('#connect-room-tag'),
    label: document.querySelector('#room-label')
}

export const name = {
    input: document.querySelector('#name-input'),
    label: document.querySelector('#name-label')
}

export const quizControls = {
    panel: document.querySelector('#quiz-control-panel'),
    title: document.querySelector('#quiz-title'),
    info: document.querySelector('#quiz-info'),
    start: document.querySelector('#quiz-start'),
    end: document.querySelector('#quiz-end'),
    pause: document.querySelector('#quiz-pause'),
    unpause: document.querySelector('#quiz-unpause'),
}

export const playerInputs = {
    title: document.querySelector('#inputs-title'),
    div: document.querySelector('#inputs-container')
}

export const players = {
    div: document.querySelectorAll('.player-div'),
    input: document.querySelectorAll('.player-div input'),
}

export const createPlayer = (playerName, room, hostControls = false) => {
    const player = {
        field: document.createElement('div'),
        fieldLabel: document.createElement('div'),
        label: document.createElement('label'),
        fieldBody: document.createElement('div'),
        fieldBodyField: document.createElement('div'),
        inputControl: document.createElement('div'),
        input: document.createElement('input'),
        admin: {
            correctControl: document.createElement('div'),
            correctButton: document.createElement('button')
        },
        name: playerName,
        remove() { this.field.remove() }
    }
    player.field.className = 'field is-horizontal'
    player.fieldLabel.className = 'field-label is-normal'
    player.label.className = 'label'
    player.label.textContent = playerName
    player.fieldBody.className = 'field-body'
    player.fieldBodyField.className = 'field'
    player.inputControl.className = 'control'
    player.input.type = 'text'
    player.input.className = 'input'
    player.input.id = playerName
    player.input.placeholder = hostControls ? "Awaiting player" : "What's the answer?"
    player.input.addEventListener('input', ({ target }) => room.answer(target.value))
    player.field.appendChild(player.fieldLabel)
    player.fieldLabel.appendChild(player.label)
    player.field.appendChild(player.fieldBody)
    player.fieldBody.appendChild(player.fieldBodyField)
    player.fieldBodyField.appendChild(player.inputControl)
    player.inputControl.appendChild(player.input)
    if (hostControls) {
        player.fieldBodyField.className += ' has-addons'
        player.inputControl.className += ' is-expanded'
        player.input.disabled = true
        player.admin.correctControl.className = 'control'
        player.admin.correctButton.className = 'button is-success'
        player.admin.correctButton.innerText = 'Correct'
        player.admin.correctButton.id = `${playerName}-answer`
        player.admin.correctButton.addEventListener('click', () => room.answerResponse('correct', player.input.value, playerName))
        player.fieldBodyField.appendChild(player.admin.correctControl)
        player.admin.correctControl.appendChild(player.admin.correctButton)
    }
    playerInputs.div.appendChild(player.field)
    return player
}
