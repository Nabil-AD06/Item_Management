<#import "template.ftl" as layout>

<@layout.registrationLayout displayInfo=false displayMessage=true; section>

    <#if section = "header">
        Welcome Back

    <#elseif section = "form">

        <div class="login-page">
            <div class="content">

                <form id="kc-form-login"
                      action="${url.loginAction}"
                      method="post"
                      class="login-card">

                    <div class="card-header">
                        <img src="${url.resourcesPath}/img/logo.jpg"
                             class="logo"
                             alt="Yazaki Logo">

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
                            value="${(login.username!'')}"
                            placeholder="Enter your email"
                            autocomplete="username"
                            required
                            autofocus />
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
                            required />
                    </div>

                    <input
                        class="login-button"
                        type="submit"
                        value="Sign In">

                </form>

            </div>
        </div>

    </#if>

</@layout.registrationLayout>