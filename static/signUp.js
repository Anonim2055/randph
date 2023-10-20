    function validateForm() {
        var pass = document.getElementById("pass").value;
        var confirmPass = document.getElementById("confirmPass").value;
        var passwordMismatch = document.getElementById("passwordMismatch");

        if (pass !== confirmPass) {
            passwordMismatch.style.display = "inline"; // Показать звездочку
            return false; // Остановить отправку формы
        }

        passwordMismatch.style.display = "none"; // Скрыть звездочку, если пароли совпадают
        return true; // Разрешить отправку формы
    }