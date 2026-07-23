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
            <label>Full Name</label>
          </div>
          <input type="text" placeholder="Enter your full name" />
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
        <div>
          <div class="label-card">
            <label>Confirm Password</label>
          </div>
          <input type="password" placeholder="Confirm password" />
        </div>
        <h4>
          you have an account ?
          <RouterLink to="/register"> Sign In</RouterLink>
        </h4>
        <button>Sign Up</button>
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
.login-card h4 {
  color: black;
}

.card-header{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 0px;
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
  padding-top: 20px;
  padding-bottom: 70px;
  /* display:flex; */
  justify-content: center;
  align-items: center;
  background: #FFFFFF;
  border-radius: 12px;
  width: 600px;
}

.label-card {
  padding: 4px;
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
  margin-top: 2px;
  margin-bottom: 15px;
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
  margin-top: 20px;
}

button:hover {
  background: #b9151b;
}
</style>
