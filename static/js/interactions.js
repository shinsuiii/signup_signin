import {
    createButton, createForm, loginButton, loginForm,
} from './variables.js'

import { 
    createAccount
} from './authentication.js'

export function interactions() {
    createButton.addEventListener('click', () => {
        if (createForm.classList.contains("hidden")) {
            createForm.classList.remove("hidden")
            loginForm.classList.add("hidden")
        } else createForm.classList.add("hidden")
    })
    loginButton.addEventListener('click', () => {
        if (loginForm.classList.contains("hidden")) {
            loginForm.classList.remove("hidden")
            createForm.classList.add("hidden")
        } else loginForm.classList.add("hidden")
    })
}

