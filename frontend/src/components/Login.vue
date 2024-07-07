<template>


        <h2>Mad II Project </h2>
            <div>
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
                <button class="btn btn-light" @click.prevent="TryLogin()">Login</button>
            
            </div>
            <br><br>
            <h3 v-if="loginfail">Username with these credentials does not exist, kindly register</h3>
            <h3 v-if="incompletecredentials">Incomplete Credentials</h3>

            <div style="margin-top:5%;">
                <h1>Forgot Password?</h1> <button @click="gotoforgot()" class="btn btn-info">Click Here</button> 
                <h1>Register </h1> <button @click="gotoregister()" class="btn btn-info">Click Here</button>
            </div>

        <br><br><br><br><br><br><br>
    </div>

</template>

<script>



export default {
    name: 'Login',
    props: {},
    data() {
        return {
            user_data: { "username": '', "password": '' },
            a: { "name": '' },
            loginfail: false,
            incompletecredentials: false
        }
    },
    methods: {
        async TryLogin() {



            await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify(this.user_data),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json()).then(data => this.a = data).catch((err) => console.log(err));


            if (this.user_data.username === '' || this.user_data.password === '') {
                this.incompletecredentials = true
                return
            }

            if (this.a["name"] === null) {
                this.loginfail = true
            }
            else {

                window.location = ('/base/' + this.a[0].id)
                

            }


        },
        gotoregister() {
            window.location = ('/register')
        },
        gotoforgot(){
            window.location = ('/forgotpassword')
        }
    }

}

</script>

<style scoped>
.Head {
  
    font-size: 150px;
    color: black;
}
</style>