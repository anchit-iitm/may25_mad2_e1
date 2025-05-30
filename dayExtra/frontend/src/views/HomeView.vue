<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App anchit"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  data() {
    return {
      token: "",
      role: "",
    };
  },
  created(){
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      console.log('No token found, redirecting to login...');
      this.$router.push({ name: 'login' });
    } else {
      console.log('Token found');
      this.role = localStorage.getItem('adminRole');
      if (this.role !== 'admin') {
        console.log('User is not an admin, redirecting to login...');
        this.$router.push({ name: 'login' });
      } else {
        console.log('User is an admin, access granted');
      }
    }
  }
}
</script>
