<template>
    <div class="admin-dashboard">
        <h1>Update Category</h1>
        <div>
            <label for="categoryName">Category Name:</label>
            <input type="text" id="categoryName" v-model="this.categoryName" required>
        </div>
        <div>
            <label for="categoryDesc">Category Description:</label>
            <input type="text" id="categoryDesc" v-model="this.categorDesc" required>
        </div>
        <button @click="updateCategory">Update Category</button>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    name: 'update',
    data() {
        return {
            token: "",
            role: "",
            categories: "",
            categoryId: "",
            categoryName: "",
            categorDesc: ""
        }
    },
    created() {
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
        get_categories() {
            axios.patch('http://localhost:5000/category',
            {
                id: this.$route.params.id
            },{
                headers: {
                    'Authorization': `${this.token}`,
                    'Content-Type': 'application/json'
                }}, 
            )
            .then(response => {
                if (response.status === 200) {
                    console.log('Category fetched successfully:', response.data);
                    this.categorDesc = response.data.category.description;
                    this.categoryName = response.data.category.name;
                } else {
                    console.error('Failed to fetch categories:', response.data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
            });
        },
        updateCategory() {
            axios.put('http://localhost:5000/category/update',
            {
                id: this.$route.params.id,
                name: this.categoryName,
                description: this.categorDesc
            },{
                headers: {
                    'Authorization': `${this.token}`,
                    'Content-Type': 'application/json'
                }}, 
            )
            .then(response => {
                if (response.status === 200) {
                    this.$router.push({ name: 'adminDashboard' });
                    
                } else {
                    console.error('Failed to fetch categories:', response.data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
            });
        }
    }
}
</script>