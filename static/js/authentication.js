import {
    submitCreateAcc, submitLoginAcc,
    createUsername, createEmail, createPassword, loginIdentifier, loginPassword,
} from './variables.js'

export async function createAccount(event) {
    event.preventDefault()
    submitCreateAcc.disabled = true



    submitCreateAcc.disabled = false
}

async function checkAccExists(identifier) {
    
}