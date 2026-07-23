import { createRouter , createWebHistory} from "vue-router" ;
import LoginView from "../views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import HomeView from "@/views/HomeView.vue";

const routes = [
    {path: "/" , redirect:"/Home"},
    {path: "/login", component: LoginView},
    {path: "/register",component:RegisterView},
    {path: "/Home",component:HomeView},

];





export const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;