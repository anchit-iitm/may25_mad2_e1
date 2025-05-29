<template>
    <div class="test_page">
        <h1>successfully seeing the test page</h1>
        <div>
            <label for="test field">Hello: </label>
            <input type="text" name="test field" id="test field" placeholder="Type something here..." v-model="this.var1">
            <input type="submit" value="Submit" @click="this.post_req_to_index_api()" >
        </div>
        {{ this.var1 }}
        {{ this.var2 }}
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'test',
    data() {    
        return {
            var1: '',
            var2: null
        };
    },
    methods: {
        clear(){
            this.var1 = ''
        },

        console_print() {
            console.log(this.var1);
        },

        get_req_to_index_api(){
            axios
                .get('http://localhost:5000/')
                .then(Response => {
                    console.log(Response)
                    this.var2 = Response.data.message;
                })
                .catch(Error => {
                    console.log(Error)
                });
        },
        post_req_to_index_api() {
            axios
                .post('http://localhost:5000/',
                    {
                        iitm: this.var1
                    }
                )
                .then(Response => {
                    console.log(Response)
                    this.var1 = '';
                    this.var2 = Response.data.message;
                })
                .catch(Error => {
                    console.log(Error)
                });
        }
    }

}
</script>

<style>

</style>