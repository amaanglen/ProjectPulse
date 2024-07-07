<template>

    <div>
        <h2>Mad II Project </h2>
        <center>
            <h1 class="Head">JanKanBan Board</h1>
            <div style="margin-top:10%;">
                <h1>Email</h1>
                <input type="email" placeholder="Enter Username" this.user_data.username
                    v-model="this.user_data.username">
            </div>
            <div style="margin-top:2%;">
                <h1>Password</h1>
                <input type="password" placeholder="Enter Password" v-model="this.user_data.password">
                <br> <br>
                <button class="btn btn-light" @click="TryRegister()">Register</button>
            </div>
            <h3 v-if="registerfail">Username is already taken, kindly provide another</h3>
            <h3 v-if="incompletecredentials">Incomplete Credentials</h3>


            <div style="margin-top:5%;">
                <h1>Login </h1> <button @click="gotologin()" class="btn btn-info">Click Here</button>

            </div>

        </center>
        <br><br><br><br><br><br><br>
    </div>
</template>
    
<script>



export default {
    name: 'Register',
    props: {},
    data() {
        return {
            user_data: { "username": '', "password": '' },
            a: {},
            registerfail: false,
            incompletecredentials: false
        }
    },
    methods: {
        async TryRegister() {
            await fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify(this.user_data),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then(data => this.a = data).catch((err) => console.log(err));

            if(this.user_data.username === '' || this.user_data.password ===''){
                this.incompletecredentials = true
            }

            if (this.a["name"] === null) {
                this.registerfail = true
            }
            else {
                window.location = ('/login')

            }


        },
        gotologin() {
            window.location = ('/login')
        }



    }

}
    
</script>
    
<style scoped>
.Head {
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    font-size: 180px;
    color: black;
}
</style>