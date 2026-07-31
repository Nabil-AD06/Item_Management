<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import request from "@/components/requests/request.vue";
import { ref } from "vue";

const activeTab = ref("");
</script>

<template>
  <div class="layout">
    <Sidebar />
    <div class="content" :class="{ blur: activeTab === 'request' }">
      <Header />

      <main>
        <div class="toolbar">
          <button @click="activeTab = 'request'">
            <span class="plus">+</span>
            New Request
          </button>
        </div>
        <RouterView />
      </main>
    </div>
    <div
      v-if="activeTab === 'request'"
      class="modal-overlay"
      @click.self="activeTab = ''"
    >
      <div class="modal">
        <request />
      </div>
    </div>
  </div>
</template>

<style scoped>
.blur {
  filter: blur(5px);
  pointer-events: none;
  user-select: none;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;

}

.modal {
  width: 90%;
  max-width: 1590px;
  max-height: 93vh;
  overflow-y: auto;
  background: white;
  border-radius: 19px;
  padding: 15px;
  margin-left: 170px;
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

.req-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.plus {
  font-size: 22px;
  font-weight: bold;
}

.toolbar button {
  padding: 24px;
  border: none;
  border-radius: 18px;
  background: rgb(233, 223, 223);
  color: #374151;
  font-size: 19px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s;
  margin-right: 30px;
}

.toolbar button:hover {
  background: #d71920;
  color: white;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}
</style>
