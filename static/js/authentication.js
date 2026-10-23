import {
    submitCreateAcc, submitLoginAcc,
    createForm, loginForm,
    createUsername, createEmail, createPassword, createPasswordConfirm, loginIdentifier, loginPassword,
    createUsernameWarning, createEmailWarning, createPasswordWarning, createPasswordConfirmWarning,
    regexUsername, regexEmail, regexPassword,
} from './variables.js'

const BASE_URL = 'http://127.0.0.1:8000'

// Create User
export async function createAccount(event) {
    event.preventDefault()
    submitCreateAcc.disabled = true

    try {
        [createUsernameWarning, createEmailWarning, createPasswordWarning, createPasswordConfirmWarning].forEach(warning => warning.classList.add('hidden'))
        for (const info of [createUsername, createEmail, createPassword]) {
            if (!fieldCheck(info.type, info.value)) {
                alert(`${info.type} DOES NOT FOLLOW THE CONVENTIONS`)
                fieldWarning(info.type)
                return
            }
        }
        if (createPassword.value !== createPasswordConfirm.value) {
            alert('PASSWORDS MUST MATCH')
            fieldWarning('passwordConfirmError')
            return
        }

        const [userExists, emailExists] = await Promise.all([
            checkAccExists(createUsername.value),
            checkAccExists(createEmail.value)
        ])
        if (userExists || emailExists) {
            alert(userExists ? 'USERNAME IS TAKEN.' : 'EMAIL IS ALREADY REGISTERED.')
            return
        }

        await createUser({
                username: createUsername.value,
                email: createEmail.value,
                password: createPassword.value,
            })

        alert('ACCOUNT CREATED SUCCESSFULLY!')
        createForm.classList.add('hidden')
        createForm.reset()

    } catch (error) {
        console.error(error)
        alert('Something went wrong. Please try again.')
    } finally {
        submitCreateAcc.disabled = false
    }
}

function fieldCheck(fieldType, value) {
    if (fieldType === 'text') {
        return regexUsername.test(value)
    } else if (fieldType === 'email') {
        return regexEmail.test(value)
    } else return regexPassword.test(value)
}

function fieldWarning(fieldType) {
    if (fieldType === 'text') {
        createUsernameWarning.classList.remove('hidden')
    } else if (fieldType === 'email') {
        createEmailWarning.classList.remove('hidden')
    } else if (fieldType === 'passwordConfirmError') {
        createPasswordConfirmWarning.classList.remove('hidden')
    } else createPasswordWarning.classList.remove('hidden')
}

async function checkAccExists(identifier) {
    const params = new URLSearchParams({identifier})
    const response = await fetch(`${BASE_URL}/signup/users?${params.toString()}`)
    if (!response.ok) throw new Error(`Check account failed: ${response.status}`)
    return await response.json()
}

async function createUser(userInfo) {
    const response = await fetch(`${BASE_URL}/signup/users`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userInfo)
    })
    if (!response.ok) throw new Error(`Create account failed: ${response.status}`)
    return await response.json()
}