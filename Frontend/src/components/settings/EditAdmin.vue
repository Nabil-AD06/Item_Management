<template>
  <div class="card">
    <h2>Profile Settings</h2>
    <div class="form-card">
      <label>Username</label>
      <input type="text" v-model="username" placeholder="New username" />
      <label>Email</label>
      <input type="email" placeholder="New email" />
      <button>Save</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getProfile, updateProfile } from "@/services/profile.service";

const username = ref("");
const email = ref("");

onMounted(async () => {
    const response = await getProfile();

    username.value = response.data.username;
    email.value = response.data.email;
});

const save = async () => {
    await updateProfile({
        username: username.value,
        email: email.value,
    });

    alert("Profile updated successfully");
};

</script>

<style scoped>
.card {
  width: 750px;
  margin: 50px auto;
  background: white;
  border-radius: 12px;
  padding: 35px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.form-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top:50px;
}

.card h2 {
  padding-top: 30px;
  color: #374151;
  font-size: 30px;
}
.form-card input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;

  border: 1px solid #d1d5db;
  border-radius: 8px;

  outline: none;
  transition: 0.3s;
}
.form-card input::placeholder {
  color: #9ca3af;
}
.form-card input:focus {
  border-color: #d71920;
  box-shadow: 0 0 0 3px rgba(215, 25, 32, 0.15);
}
.form-card button {
  margin-top: 20px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: #d71920;
  color: white;
  font-size: 16px;
  font-weight: 600;
  margin-top:40px;
  margin-bottom:50px;
  cursor: pointer;
  transition: 0.3s;
}

.form-card label {
  font-size: 16px;
  font-weight: 600;
  color: #4b5563;
}

.form-card button:hover {
  background: #b4151b;
}
</style>
