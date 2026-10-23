// Buttons
export const createButton = document.getElementById('createButton')
export const submitCreateAcc = document.getElementById('submitCreateAcc')
export const loginButton = document.getElementById('loginButton')
export const submitLoginAcc = document.getElementById('submitLoginAcc')

// Forms
export const createForm = document.getElementById('createForm')
export const loginForm = document.getElementById('loginForm')

// Input Fields
export const createUsername = document.getElementById('createUsername')
export const createEmail = document.getElementById('createEmail')
export const createPassword = document.getElementById('createPassword')
export const createPasswordConfirm = document.getElementById('createPasswordConfirm')
export const loginIdentifier = document.getElementById('loginIdentifier')
export const loginPassword = document.getElementById('loginPassword')

// Warning
export const createUsernameWarning = document.getElementById('createUsernameWarning')
export const createEmailWarning = document.getElementById('createEmailWarning')
export const createPasswordWarning = document.getElementById('createPasswordWarning')
export const createPasswordConfirmWarning = document.getElementById('createPasswordConfirmWarning')

// Regex
export const regexUsername = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{3,30}$/
export const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
export const regexPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/