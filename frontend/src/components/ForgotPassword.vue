<template>


        <h2>Mad II Project </h2>
            <div>
            <h1 class="Head">JanKanBan Board</h1>
            <div style="margin-top:10%;">
                <h1>Forgot Password?</h1>
                <h1>Enter email</h1>
                <input type="email" placeholder="Enter Username" v-model="this.user_data.useremail">
            </div>
            <br>
            <h5>{{ a.user }}</h5>
            <h4></h4>
                <br> <br>
                <button class="btn btn-light" @click.prevent="TryForgot()">Click Here</button>
            
            <br><br>
            <h3 v-if="loginfail">Username with these credentials does not exist, kindly register</h3>
            <h3 v-if="incompletecredentials">Incomplete Credentials</h3>

            <div style="margin-top:5%;">
                <h1>Login </h1> <button @click="gotologin()" class="btn btn-info">Click Here</button>

            </div>

        <br><br><br><br><br><br><br>
    </div>

</template>

<script>



export default {
    name: 'ForgotPassword',
    props: {},
    data() {
        return {
            user_data: { "useremail": '' },
            a: { "user": 'Kindly enter your registered email id' },
            loginfail: false,
            incompletecredentials: false
        }
    },
    methods: {
        async TryForgot() {



            await fetch('http://127.0.0.1:5000/forgotpassword/'+ this.user_data.useremail, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json()).then(data => this.a = data).catch((err) => console.log(err));


                

            


        },
        gotologin() {
            window.location = ('/login')
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