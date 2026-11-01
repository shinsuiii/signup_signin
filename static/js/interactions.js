import {
    createForm, loginForm,
    createButton, loginButton,
    createPassword, createPasswordConfirm,
    createPasswordConfirmWarning,
} from './variables.js'

import { 
    createAccount, loginAccount,
    fieldCheck,
} from './authentication.js'

export function interactions() {
    // Open forms buttons
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

    // Create user fields client-side validation
    createForm.querySelectorAll('input:not(.ignore)').forEach(createField => {
        const warning = document.getElementById(`${createField.id}Warning`)

        createField.addEventListener('blur', () => {
            const valid = fieldCheck(createField.type, createField.value)
            warning.classList.toggle('hidden', valid)
            if (createField.type === 'password') {
                const matchingPassword = createPassword.value === createPasswordConfirm.value ? true : false
                createPasswordConfirmWarning.classList.toggle('hidden', matchingPassword)
            }
        })
    })
    createPasswordConfirm.addEventListener('blur', () => {
        const matchingPassword = createPassword.value === createPasswordConfirm.value ? true : false
        createPasswordConfirmWarning.classList.toggle('hidden', matchingPassword)
    })

    createForm.addEventListener('submit', createAccount)
    loginForm.addEventListener('submit', loginAccount)
}

