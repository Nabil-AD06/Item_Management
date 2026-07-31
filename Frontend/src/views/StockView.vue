<script setup lang="ts">
import Sidebar from "@/components/layout/Sidebar.vue";
</script>

<template>
  <div class="layout">
    <Sidebar />
    <main>
      <div class="blocs">
        <h1 Stock></h1>
        <h2>Manage and track all equipment in inventory</h2>
      </div>
      <div>
        <div>
          <p>Total Items</p>
          <p>{{}}</p>
        </div>
        <div>
          <p>Available</p>
          <p>{{}}</p>
        </div>
        <div>
            <p>In Use</p>
            <p>{{  }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.blocs{
    color: black;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}
</style>
