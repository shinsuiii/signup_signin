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
        // Ensures fields are correctly filled.
        const validUser = fieldCheck('text', createUsername.value)
        const validEmail = fieldCheck('email', createEmail.value)
        const validPass = fieldCheck('password', createPassword.value)
        const passMatches = createPassword.value === createPasswordConfirm.value
        createUsernameWarning.classList.toggle('hidden', validUser)
        createEmailWarning.classList.toggle('hidden', validEmail)
        createPasswordWarning.classList.toggle('hidden', validPass)
        createPasswordConfirmWarning.classList.toggle('hidden', passMatches)
        if (!(validUser && validEmail && validPass && passMatches)) return
        
        const [userExists, emailExists] = await Promise.all([
            checkAccExists(createUsername.value),
            checkAccExists(createEmail.value)
        ])
        if (userExists || emailExists) {
            alert(userExists ? 'USERNAME IS TAKEN.' : 'EMAIL IS ALREADY REGISTERED.')
            return
        }

        await createUser({
                username: createUsername.value.trim(),
                email: createEmail.value.trim().toLowerCase(),
                password: createPassword.value.trim(),
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
    const response = await fetch(`${BASE_URL}/users/signup?${params.toString()}`)

    if (response.status === 422) {
        alert('Check account failed, ensure proper credentials are met.')
    }
    if (!response.ok) {
        throw new Error(`Check account failed: ${response.status}`)
    }

    return await response.json()
}

async function createUser(userInfo) {
    const response = await fetch(`${BASE_URL}/users/signup`, {
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
        if (!loginIdentifier.value || !loginPassword.value) {
            alert('Empty fields; please fill up your credentials.')
            return
        }
                
        const result = await loginUser({
            identifier: loginIdentifier.value.includes('@') ? loginIdentifier.value.trim().toLowerCase() : loginIdentifier.value.trim(),
            password: loginPassword.value.trim()
        })
        if (!result) return

        const jwtToken = result.token
        localStorage.setItem('accessToken', jwtToken)
        
        alert('ACCOUNT LOGIN SUCCESSFUL!')
        loginForm.classList.add('hidden')
        loginForm.reset()
    } catch(error) {
        console.error(error)
        alert('Something went wrong. Please try again.')
    } finally {
        submitLoginAcc.disabled = false
    }
}

async function loginUser(userInfo) {
    const response = await fetch(`${BASE_URL}/users/signin`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userInfo)
    })

    if (response.status === 401) {
        alert('Invalid credentials, please try again.')
        return null
    }
    
    if (response.status === 422) {
        alert('Login account failed, ensure proper credentials are met.')
        return null
    }
    if (!response.ok) {
        throw new Error(`Login account failed: ${response.status}`)
    }

    return await response.json()
}

