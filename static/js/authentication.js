import {
    submitCreateAcc, submitLoginAcc,
    createUsername, createEmail, createPassword, loginIdentifier, loginPassword,
    regexUsername, regexEmail, regexPassword
} from './variables.js'

const BASE_URL = 'http://127.0.0.1:8000'

// Create User
export async function createAccount(event) {
    event.preventDefault()
    submitCreateAcc.disabled = true
    
    const userInfo = [createUsername, createEmail, createPassword]
    for (const info of userInfo) {
        if (!fieldCheck(info.type, info.value)) return
    }

    const [userExists, emailExists] = await Promise.all([
        checkAccExists(createUsername.value),
        checkAccExists(createEmail.value)
    ])
    if (!userExists && !emailExists) {
        await createUser({
            username: createUsername.value,
            email: createEmail.value,
            password: createPassword.value,
        })
        alert('ACCOUNT CREATED SUCCESSFULLY!')
    }

    submitCreateAcc.disabled = false
}

function fieldCheck(dataType, value) {
    if (dataType === 'text') {
        return regexUsername.test(value)
    } else if (dataType === 'email') {
        return regexEmail.test(value)
    } else {
        return regexPassword.test(value)
    }
}

async function checkAccExists(identifier) {
    const params = new URLSearchParams({identifier})
    const response = await fetch(`${BASE_URL}/signup/users${params.toString()}`)
    return await response.json()
}

async function createUser(userInfo) {
    const response = await fetch(`${BASE_URL}/signup/users`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userInfo)
    })
    return await response.json()
}