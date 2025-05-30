<template>
    <div class="admin-dash">
        <h1>Admin Dashboard</h1>
        <p>Welcome, Admin!</p>
        <p>Your role is: {{ role }}</p>
        <table>
            <thead>
                <tr>
                    <th>id</th>
                    <th>Category Name</th>
                    <th>Category Description</th>
                    <th>Category status</th>
                    <th>actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="category in categories" :key="category.id">
                    <td>{{ category.id }}</td>
                    <td>{{ category.name }}</td>
                    <td>{{ category.description }}</td>
                    <td v-if="category.status === false">Active</td><td v-else>Inactive</td>
                    <td>
                        <router-link :to="{'name': 'update', params: {'id': category.id}}">Edit</router-link> | 
                        <button @click="this.deleteCategory(category.id)">switchSttus</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    name: 'adminDash',
    data(){
        return{
            token: "",
            role: "",
            categories: ""
        }
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
                this.get_categories();
            }
        }
    },
    methods: {
        get_categories(){
            axios.post('http://localhost:5000/category',
                {
                    // request body that is empty for this request, i added this because the header was not being sent without a body
                },
                {
                    headers: {
                        'Authorization': `${this.token}`,
                    }
                }
            )
            .then(response => {
                if(response.status === 200) {
                    this.categories = response.data.categories;
                } else {
                    console.error('Failed to fetch categories:', response.data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
            });
        },
        deleteCategory(id){
            axios.patch(`http://localhost:5000/category/update`, 
            {
                "id": id
            },{
                headers: {
                    'Authorization': `${this.token}`,
                    'Content-Type': 'application/json'
                }
            },
            )
            .then(response => {
                if(response.status === 201) {
                    console.log('Category deleted successfully');
                    this.get_categories(); // Refresh the categories list
                } else {
                    console.error('Failed to delete category:', response.data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting category:', error);
            });
        }
    }
}
</script>