<template>
  <div class="card">
    <h2>Add Admin</h2>
    <div class="form-card">
      <label>Username</label>
      <input type="text" placeholder="Enter Username" />
      <div class="container">
        <div class="field1">
          <label>First name </label>
          <input type="text" placeholder="Enter first name" />
        </div>
        <div class="field2">
          <label>Last name</label>
          <input type="text" placeholder="Enter last name" />
        </div>
      </div>
      <label>Email</label>
      <input type="email" placeholder="Enter email" />
      <label>Password</label>
      <input type="password" placeholder="Enter Password" />
      <label>Confirm Password</label>
      <input type="password" placeholder="Verify Password" />
      <button>Save</button>
    </div>
  </div>
</template>

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
