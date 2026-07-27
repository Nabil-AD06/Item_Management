<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";


</script>

<template>
  <div class="layout">
    <Sidebar />
  
  <div class="content">
    <Header />
    <main>
        <RouterView />
      </main>
  </div>
  </div>
</template>

<style scoped>
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
</style>
