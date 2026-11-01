import {
    submitCreateAcc, submitLoginAcc,
    createForm, loginForm,
    createUsername, createEmail, createPassword, createPasswordConfirm, loginIdentifier, loginPassword,
    createUsernameWarning, createEmailWarning, createPasswordWarning, createPasswordConfirmWarning,
    regexUsername, regexEmail, regexPassword,
} from './variables.js'


const BASE_URL = ''

// Create User
export async function createAccount(event) {
    event.preventDefault()
    submitCreateAcc.disabled = true

    try {
        // Checks if any warnings are present in the DOM
        const warnings = [createUsernameWarning, createEmailWarning, createPasswordWarning, createPasswordConfirmWarning]
        const hasWarning = warnings.some(warning => !warning.classList.contains('hidden'))
        if (hasWarning) return
        
        // Checks if user exists in database
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

export function fieldCheck(fieldType, value) {
    if (fieldType === 'text') {
        return regexUsername.test(value)
    } else if (fieldType === 'email') {
        return regexEmail.test(value)
    } else return regexPassword.test(value)
}

async function checkAccExists(identifier) {
    const params = new URLSearchParams({identifier})
    const response = await fetch(`${BASE_URL}/signup/users?${params.toString()}`)

    if (response.status === 422) {
        alert('Check account failed, ensure proper credentials are met.')
    }
    if (!response.ok) {
        throw new Error(`Check account failed: ${response.status}`)
    }
    
    return await response.json()
}

async function createUser(userInfo) {
    const response = await fetch(`${BASE_URL}/signup/users`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userInfo)
    })

    if (response.status === 422) {
        alert('Create account failed, ensure proper credentials are met.')
    }
    if (!response.ok) {
        throw new Error(`Create account failed: ${response.status}`)
    }
    
    return await response.json()
}


// Login User
export async function loginAccount(event) {
    event.preventDefault()
    submitLoginAcc.disabled = true

    try {
        

    } catch(error) {
        console.error(error)
        alert('Something went wrong. Please try again.')
    } finally {
        submitLoginAcc.disabled = false
    }
}