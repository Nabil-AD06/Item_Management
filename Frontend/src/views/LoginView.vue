<template>
  <div class="login-page">
    <div class="content">
      <form class="login-card">
        <div class="card-header">
            <img src="@/assets/logo.jpg" alt="Yazaki Logo" class="logo"/>
          <h1>Welcom Back</h1>
        </div>
        <div>
          <div class="label-card">
            <label>Email</label>
          </div>
          <input type="email" placeholder="Enter your email" />
        </div>
        <div>
          <div class="label-card">
            <label>Password</label>
          </div>
          <input type="password" placeholder="Enter your password" />
        </div>
        <button>Sign In</button>
      </form>
    </div>
  </div>
</template>



<style scoped>
.login-page {
  width: 100%;
  height: 100vh;

  background-image: url("@/assets/yazaki.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.card-header{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 40px;
    flex-direction: column;
}
.logo{
    width: 200px;
    height: auto;
}
.content {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: end;
  padding-right: 150px;
}
.login-card {
  padding: 50px;
  padding-top: 40px;
  padding-bottom: 80px;
  /* display:flex; */
  justify-content: center;
  align-items: center;
  background: #FFFFFF;
  border-radius: 12px;
  width: 600px;
}

.label-card {
  padding: 8px;
  color: black;
}
.login-card h1 {
  margin: 0;
  color: black;
  font-size: 32px;
  font-weight: 600;
}
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 2px;
}

.login-card input::placeholder {
  color: rgba(0, 0, 0, 0.3);
}

input {
  padding: 18px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 8px;
  margin-bottom: 25px;
  padding-right: 300px;
  background-color: rgb(232, 232, 232);
}

button {
  width: 100%;
  padding: 14px;
  border: none;
  background: #d71920;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 40px;
}

button:hover {
  background: #b9151b;
}
</style>
