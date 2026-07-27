<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import { User, Shield, Users } from "lucide-vue-next";
import { ref } from "vue";
import EditAdmin from "@/components/settings/EditAdmin.vue";
import SecuritySittings from "@/components/settings/SecuritySittings.vue";
import AddAdmin from "@/components/settings/AddAdmin.vue";

const activeTab = ref("") ;

const params = [
  { id: 1, label: "Profile", icon: User , value:"profile"},
  { id: 2, label: "Security", icon: Shield, value:"security" },
  { id: 3, label: "Administrators", icon: Users, value:"administrators" },
];



</script>

<template>
  <div class="layout">
    <Sidebar />

    <div class="content">
      <Header />
      <main>
        <div class="btn">
          <button
          v-for="i in params" 
          :key="i.id"
          :class="{active:activeTab===i.value}"
          @click="activeTab = i.value"
        >
          <component :is="i.icon" />
          <span> {{ i.label }} </span>
          </button>
        </div>
        <div v-if="activeTab==='profile'" class="contenent">
          <EditAdmin />
        </div>
        <div v-if="activeTab==='security'" class="contenent">
          <SecuritySittings />
        </div>
        <div v-if="activeTab==='administrators'" class="contenent">
          <addAdmin />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.contenent{
  color: black;
}

.layout {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.btn {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 40px;
}

.btn button {
  display: flex;
  align-items: center;
  gap: 30px;

  padding: 12px 24px;

  border: none;
  border-radius: 10px;

  background: rgb(233, 223, 223);
  color: #374151;

  font-size: 18px;
  font-weight: 500;

  cursor: pointer;
  transition: 0.3s;
}

.btn button:hover {
  background: #d71920;
  color: white;
}

.btn button.active {
  background-color: #D71920 ;
  color: white !important;
}

</style>
