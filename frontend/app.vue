<template>
    <div id="app">
      <nav>
        <router-link to="/">货物列表</router-link>
        <router-link to="/login" v-if="!isLoggedIn">登录</router-link>
        <router-link to="/register" v-if="!isLoggedIn">注册</router-link>
        <span v-if="isLoggedIn">欢迎, {{ username }}!</span>
        <button v-if="isLoggedIn" @click="logout">退出</button>
      </nav>
      <router-view/>
    </div>
  </template>
<script>
  import { mapState, mapActions } from 'vuex'
  
  export default {
    computed: {
      ...mapState(['isLoggedIn', 'username'])
    },
    methods: {
      ...mapActions(['logout'])
    }
  }
</script>
  