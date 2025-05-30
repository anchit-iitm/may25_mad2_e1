<template>
    <div class="login_page">
        <h1>Login Page</h1>
        <div>
            <div>
                <label for="username">email:</label>
                <input type="text" id="username" v-model="this.userid" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="this.password" required>
            </div>
            <button @click="this.login()">Login</button>
        </div>
        <p v-if="this.errorMessage" class="error">{{ this.errorMessage }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'login',
    data() {
        return {
            userid: '',
            password: '',
            errorMessage: '',
            token: ''
        };
    },
    methods: {
        login() {
            axios.post('http://localhost:5000/login', {
                email: this.userid,
                password: this.password
            })
            .then(response => { 
                if (response.status === 200) {
                    console.log('Login response:', response.data);
                    this.token = response.data.authToken;
                    console.log('Login successful, token:', this.token);
                    localStorage.setItem('authToken', this.token);
                    localStorage.setItem('userEmail', response.data.user.email);
                    if(response.data.user.roles[1] === 'admin') {
                        localStorage.setItem('userRole', response.data.user.roles[0]);
                        localStorage.setItem('adminRole', response.data.user.roles[1]);
                    } else {
                        localStorage.setItem('userRole', response.data.user.roles[0]);
                    }
                    localStorage.setItem('userUsername', response.data.user.username);

                    this.$router.push({ name: 'home' });
                } else {
                    this.errorMessage = response.data.message;
                }
            })
            .catch(error => {
                console.error(error);
                this.errorMessage = error.response ? error.response.data.message : 'An error occurred during login.';
            });
        }
    }
};
</script>