<template>
  <aside>
    <img src="../../assets/home-logo.png" />
    <h2>IT ASSET MANAGEMENT SYSTEM</h2>
    <nav>
      <RouterLink v-for="i in Items" :key="i.path" :to="i.path">
        <component :is="i.icon" />
        <span>{{ i.name }}</span>
      </RouterLink>
    </nav>
    <div class="logout">
      <RouterLink to="/Settings">
        <Settings />
        <span>Settings</span>
      </RouterLink>

      <button @click="logout">
        <LogOut />
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import keycloak from "@/services/keycloak";

const logout = () => {
  keycloak.logout();
};

import {
  LayoutDashboard,
  Boxes,
  History,
  Settings,
  LogOut,
  Sidebar,
} from "lucide-vue-next";

const Items = [
  { name: "Dashboard", path: "/Home", icon: LayoutDashboard },
  { name: "Stock", path: "/Stock", icon: Boxes },
  { name: "History", path: "/History", icon: History },
];

const logItem = [
  { name: "Settings", path: "/Settings", icon: Settings },
  { name: "LogOut", path: "/login", icon: LogOut },
];
</script>

<style>
img {
  width: 240px;
}

aside {
  width: 250px;
  height: 100vh;
  background-color: #1d2634;
  padding-left: 8px;
  display: flex;
  flex-direction: column;
}

.logout button {
  display: flex;
  align-items: center;
  gap: 13px;

  width: 100%;
  height: 50px;
  margin-left: 8px;
  border: none;
  background: transparent;

  color: white;
  font-size: 140%;

  cursor: pointer;
}

.logout button:hover {
  background-color: #d71920;
  border-radius: 8px;
  margin-right: 10px;
  margin-left: -4px;
}

.logout {
  color: white;
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: auto;
}
.logout a {
  display: flex;
  align-items: center;
  gap: 13px;
  color: white;
  height: 50px;
  padding: 0 20px;
  border-radius: 10px;
  transition: 0.3s;
  text-decoration: none;
  font-size: 140%;
}

nav a:hover {
  background-color: #d71920;
  border-radius: 8px;
  height: 50px;
  margin-right: 10px;
}

nav a.router-link-active {
  background-color: #d71920;
  color: white;
  border-radius: 8px;
  padding: 8px;
  margin-right: 10px;
}

h2 {
  color: white;
  /* text-align: center; */
  font-size: 22px;
  padding: 0 20px;
  margin-top: 20px;
}

nav {
  display: flex;
  flex-direction: column;
  margin-top: 40px;
  gap: 30px;
  flex: 1;
}

nav a {
  display: flex;
  align-items: center;
  gap: 13px;
  color: white;
  height: 50px;
  padding: 0 20px;
  border-radius: 10px;
  transition: 0.3s;
  text-decoration: none;
  font-size: 140%;
}

.logout a:hover {
  background-color: #d71920;
  border-radius: 8px;
  height: 50px;
  margin-right: 10px;
}

.logout a.router-link-active {
  background-color: #d71920;
  color: white;
  border-radius: 8px;
  padding: 8px;
  margin-right: 10px;
}
</style>
