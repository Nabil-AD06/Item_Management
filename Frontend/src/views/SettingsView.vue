<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import { User, Shield, Users, Package } from "lucide-vue-next";
import { ref, onMounted } from "vue";
import EditAdmin from "@/components/settings/EditAdmin.vue";
import SecuritySittings from "@/components/settings/SecuritySittings.vue";
import AddAdmin from "@/components/settings/AddAdmin.vue";

const activeTab = ref("");
const based_on_stock = ref(false);

onMounted(() => {
  const savedSetting = localStorage.getItem("based_on_stock");

  if (savedSetting !== null) {
    based_on_stock.value = savedSetting === "true";
  }
});

const saveStockSetting = () => {
  localStorage.setItem("based_on_stock", String(based_on_stock.value));
};

const params = [
  { id: 1, label: "Profile", icon: User, value: "profile" },
  { id: 2, label: "Security", icon: Shield, value: "security" },
  { id: 3, label: "Administrators", icon: Users, value: "administrators" },
  { id: 4, label: "Stock", icon: Package, value: "stock" },
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
            :class="{ active: activeTab === i.value }"
            @click="activeTab = i.value"
          >
            <component :is="i.icon" />
            <span> {{ i.label }} </span>
          </button>
        </div>
        <div v-if="activeTab === 'profile'" class="contenent">
          <EditAdmin />
        </div>
        <div v-if="activeTab === 'security'" class="contenent">
          <SecuritySittings />
        </div>
        <div v-if="activeTab === 'administrators'" class="contenent">
          <addAdmin />
        </div>
        <div v-if="activeTab === 'stock'" class="contenent">
          <h2>Stock Settings</h2>

          <div class="setting">
            <label>
              <input
                v-model="based_on_stock"
                type="checkbox"
                @change="saveStockSetting"
              />

              Based on stock
            </label>

            <small>
              If enabled, equipment will be taken from stock when issued.
            </small>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.contenent {
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

.contenent {
  color: #1f2937;

  width: 100%;
  max-width: 750px;

  margin: 40px auto 0;
}
.contenent h2 {
  color: #111827;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 20px 0;
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
  background-color: #d71920;
  color: white !important;
}

/* =========================
   CUSTOM CHECKBOX - Based on stock
   ========================= */
.setting {
  width: 100%;
  max-width: 650px;
  margin: 0 auto; /* centre horizontalement */

  padding: 25px 30px;

  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;

  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);

  box-sizing: border-box;
}

/* Label */
.setting label {
  display: flex;
  align-items: center;

  gap: 12px;

  color: #1f2937;
  font-size: 16px;
  font-weight: 600;

  cursor: pointer;
}

/* Checkbox */
.setting input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;

  width: 22px;
  height: 22px;
  min-width: 22px;

  margin: 0;

  border: 2px solid #d1d5db;
  border-radius: 5px;

  background-color: #ffffff;

  cursor: pointer;
  position: relative;

  transition: all 0.2s ease;
}

/* Hover */
.setting input[type="checkbox"]:hover {
  border-color: #d71920;
}

/* Checked */
.setting input[type="checkbox"]:checked {
  background-color: #d71920;
  border-color: #d71920;
}

/* Check */
.setting input[type="checkbox"]:checked::after {
  content: "";

  position: absolute;

  left: 6px;
  top: 2px;

  width: 6px;
  height: 11px;

  border: solid white;
  border-width: 0 2px 2px 0;

  transform: rotate(45deg);
}

/* Focus */
.setting input[type="checkbox"]:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(215, 25, 32, 0.15);
}

/* Description */
.setting small {
  display: block;

  margin-top: 12px;
  margin-left: 34px;

  color: #6b7280;

  font-size: 13px;
  line-height: 1.5;
}
</style>
