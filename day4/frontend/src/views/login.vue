<template>
    <div class="login_page">
        <h1>Login Page</h1>
        <div>
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="this.userid" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="this.password" required>
            </div>
            <button @click="this.login()">Login</button>
        </div>
        {{ this.token }}
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
                userid: this.userid,
                password: this.password
            })
            .then(response => {
                if (response.data.success) {
                    this.token = response.data.authToken;
                } else {
                    this.errorMessage = response.data.message;
                }
            })
            .catch(error => {
                console.error(error);
                this.errorMessage = 'An error occurred during login.';
            });
        }
    }
};
</script>