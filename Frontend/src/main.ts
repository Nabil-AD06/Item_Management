import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import keycloak from "./services/keycloak";

keycloak
  .init({
    onLoad: "login-required",
    checkLoginIframe: false,
  })
  .then(async(authenticated) => {
    if (!authenticated) return;
    // console.log(keycloak.token);
    // console.log(keycloak.tokenParsed);
    const response = await fetch("http://localhost:8000/api/test/", {
      headers: {
        Authorization: `Bearer ${keycloak.token}`,
      },
    });

    // console.log(await response.json());
    const app = createApp(App);

    app.use(router);

    app.mount("#app");
    setInterval(
      () => keycloak.updateToken(30).catch(() => keycloak.logout()),
      60000,
    );
  });
