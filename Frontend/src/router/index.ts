import { createRouter , createWebHistory} from "vue-router" ;
import LoginView from "../views/LoginView.vue";

const routes = [
    {path: "/" , redirect:"/login"},
    {path: "/login", component: LoginView},

];
export const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;