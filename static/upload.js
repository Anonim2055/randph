        function showLoading() {
            document.getElementById("loading").style.display = "block";
            document.querySelector('form').style.display = "none";
        }
                function MyD() {
            window.location.href = "/user_photos/2";
        }
        function logout() {
            window.location.href = "/logout";
        }
        function home() {
        window.location.href = "/";
        }
                function enableUploadButton() {
            var fileInput = document.querySelector('input[name="file"]');
            var uploadButton = document.getElementById('uploadButton');

            if (fileInput.files.length > 0) {
                uploadButton.removeAttribute('disabled');
            } else {
                uploadButton.setAttribute('disabled', 'disabled');
            }
        }