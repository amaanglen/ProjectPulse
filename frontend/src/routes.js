import {createWebHistory, createRouter} from 'vue-router'
import ViewBase from '/src/ViewBase.vue'
import Login from '/src/components/Login.vue'
import Register from '/src/components/Register.vue'
import ForgotPassword from '/src/components/ForgotPassword'

const routes = [
    {
        name: 'ViewBase',
        path:'/base/:userid',
        component: ViewBase
    },
    {
        name: 'Login',
        path:'/login',
        component: Login

    },
    {
        name: 'Register',
        path:'/register',
        component: Register

    },
    {
        name: 'ForgotPassword',
        path:'/forgotpassword',
        component: ForgotPassword

    }
];


const router = createRouter({
    history: createWebHistory(), routes
});

export default router;