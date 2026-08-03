// -----------------------------
// Show / Hide Password
// -----------------------------
const togglePassword = document.getElementById("togglePassword");

if (togglePassword) {

    togglePassword.addEventListener("click", () => {

        const password = document.getElementById("password");

        password.type =
            password.type === "password"
                ? "text"
                : "password";

    });

}


// -----------------------------
// Login
// -----------------------------
const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const email = document.getElementById("email").value;

        const password = document.getElementById("password").value;

        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

        try {

            const response = await fetch(
                `${API_BASE_URL}/auth/login`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {

                document.getElementById("errorMessage").innerText =
                    data.detail;

                return;

            }

            saveToken(data.access_token);

            const apiKeyResponse = await fetch(
                `${API_BASE_URL}/api-key/generate`,
                {
                    method: "POST",
                    headers: authHeaders()
                }
            );

            const apiKeyData = await apiKeyResponse.json();

            saveApiKey(apiKeyData.api_key);

            window.location.href = "dashboard.html";

        }
        catch (error) {

            console.error(error);

            document.getElementById("errorMessage").innerText =
                "Unable to connect to server.";

        }

    });

}



// -----------------------------
// Signup
// -----------------------------
const signupForm = document.getElementById("signupForm");

if (signupForm) {

    signupForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const body = {

            full_name:
                document.getElementById("full_name").value,

            email:
                document.getElementById("email").value,

            password:
                document.getElementById("password").value

        };

        try {

            const response = await fetch(

                `${API_BASE_URL}/auth/signup`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify(body)

                }

            );

            const data = await response.json();

            if (!response.ok) {

                document.getElementById("errorMessage").innerText =
                    data.detail;

                return;

            }

            alert("Account created successfully.");

            window.location.href = "login.html";

        }
        catch (error) {

            console.error(error);

            document.getElementById("errorMessage").innerText =
                "Unable to connect to server.";

        }

    });

}