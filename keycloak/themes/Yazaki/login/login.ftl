<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yazaki - IT Asset Management</title>

    <link rel="stylesheet" href="${url.resourcesPath}/css/login.css">
</head>

<body>

<div class="login-page">
    <div class="content">

        <form id="kc-form-login"
              action="${url.loginAction}"
              method="post"
              class="login-card">

            <div class="card-header">
                <img src="${url.resourcesPath}/img/logo.jpg"
                     alt="Yazaki Logo"
                     class="logo">

                <h1>Welcome Back</h1>
            </div>
            <#if message?has_content>
                <div class="error-message">
                    ${kcSanitize(message.summary)?no_esc}
                </div>
            </#if>
            <div class="form-group">
                <div class="label-card">
                    <label for="username">Email</label>
                </div>

                <input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Enter your email"
                    autocomplete="username"
                    required
                    autofocus
                />
            </div>

            <div class="form-group">
                <div class="label-card">
                    <label for="password">Password</label>
                </div>

                <input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Enter your password"
                    autocomplete="current-password"
                    required
                />
            </div>

            <div class="forgot-password">
                <#if realm.resetPasswordAllowed>
                    <a href="${url.loginResetCredentialsUrl}">
                        Forgot Password ?
                    </a>
                </#if>
            </div>

            <input
                class="login-button"
                type="submit"
                value="Sign In">

        </form>

    </div>
</div>
<script>
document.getElementById("kc-form-login").addEventListener("submit", function () {
    document.querySelector(".login-button").disabled = true;
});
</script>
</body>
</html>