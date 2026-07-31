<template>
  <div class="card">
    <h2>Add Admin</h2>
    <form @submit.prevent="save">
      <div class="form-card">
        <label>Username</label>
        <input type="text" v-model="username" placeholder="Enter Username" />
        <div class="container">
          <div class="field1">
            <label>First name </label>
            <input
              type="text"
              v-model="first_name"
              placeholder="Enter first name"
            />
          </div>
          <div class="field2">
            <label>Last name</label>
            <input
              type="text"
              v-model="last_name"
              placeholder="Enter last name"
            />
          </div>
        </div>
        <label>Email</label>
        <input type="email" v-model="email" placeholder="Enter email" />
        <label>Password</label>
        <input
          type="password"
          v-model="password"
          placeholder="Enter Password"
        />
        <label>Confirm Password</label>
        <input
          type="password"
          v-model="confirm_password"
          placeholder="Verify Password"
        />
        <button type="submit">Save</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { create_admin } from "@/services/profile.service";

const username = ref("");
const first_name = ref("");
const last_name = ref("");
const email = ref("");
const password = ref("");
const confirm_password = ref("");

const save = async () => {
  try {
    if (password.value !== confirm_password.value) {
      alert("Passwords do not match");
      return;
    }
    await create_admin({
      username: username.value,
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      confirm_password: confirm_password.value,
    });

    alert("Admin added Successfully");
    username.value = "";
    first_name.value = "";
    last_name.value = "";
    email.value = "";
    password.value = "";
    confirm_password.value = "";
  } catch (error: any) {
    console.error(error);
    alert("error.response?.data?.error || Failed to add Admin");
  }
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

.container {
  display: flex;
  flex-direction: row;
}

.form-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 50px;
}

.card h2 {
  padding-top: 30px;
  color: #374151;
  font-size: 30px;
}
.form-card label {
  font-size: 16px;
  font-weight: 600;
  color: #4b5563;
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

.field1 {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 10px;
  margin-right: 20px;
}
.field2 {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 10px;
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
  margin-top: 40px;
  margin-bottom: 50px;
  cursor: pointer;
  transition: 0.3s;
}

.form-card button:hover {
  background: #b4151b;
}
</style>
