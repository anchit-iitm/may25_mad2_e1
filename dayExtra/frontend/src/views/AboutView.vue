<template>
  <div class="about">
    <h1>This is an about page</h1>
    {{ this.data }}
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'AboutView',
  data() {
    return {
      data: null
    };
  },
created() {
    this.fetchData();
  },
  methods: {
    fetchData(){
      axios.get('http://localhost:5000/')
        .then(response => {
          this.data = response.data;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  }
};
</script>