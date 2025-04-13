function togglePassword() {
    const passwordInput = document.getElementById('yourPassword')
    const icon = document.getElementById('eyeIcon')
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text'
        icon.classList.remove('bi-eye')
        icon.classList.add('bi-eye-slash')
    } else {
        passwordInput.type = 'password'
        icon.classList.remove('bi-eye-slash')
        icon.classList.add('bi-eye')
    }
}