<template>
  <header class="header">

    <div class="welcome">
      <h1>Welcome back, {{first_name}}</h1>
      <p>Here's what's happening with your workspace.</p>
    </div>

    <div class="actions">
      <div class="profile">
        UI
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import keycloak from "@/services/keycloak";

const first_name = keycloak.tokenParsed?.given_name;
</script>

<style>
.header{
    height:90px;
    background:white;

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:0 35px;

    border-bottom:1px solid #e5e7eb;
}

.welcome h1{
    font-size:34px;
    font-weight:700;
    color: black;
}

.welcome p{
    color:#64748b;
    margin-top:8px;
}

.actions{
    display:flex;
    align-items:center;
    gap:20px;
}

.actions input{
    width:320px;
    height:46px;

    border:1px solid #d1d5db;
    border-radius:10px;

    padding:0 18px;
}

.profile{
    width:48px;
    height:48px;

    border-radius:50%;

    background:#1d2634;
    color:white;

    display:flex;
    justify-content:center;
    align-items:center;

    font-weight:bold;
}

</style>