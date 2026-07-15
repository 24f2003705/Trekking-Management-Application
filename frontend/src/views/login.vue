<template>
    <div class="container-fluid vh-100">
        <div class="row h-100">
            <div class="col-lg-7 d-none d-lg-block p-0">
                <img src="https://images.unsplash.com/photo-1517824806704-9040b037703b?auto=format&fit=crop&w=1200&q=80" class="login-image" alt="Trekking adventure illustration">
            </div>
            <div class="col-lg-5 d-flex align-items-center justify-content-center">
                <div class="card login-card p-5">
                    <h2 class="fw-bold mb-2"> Welcome Back</h2>
                    <p class="text-secondary mb-4"> Login to continue your trekking journey</p>
                    <div class="mb-3">
                        <label class="form-label">
                            Email
                        </label>
                        <input type="email" class="form-control" v-model="email">
                    </div>
                    <div class="mb-4">
                        <label class="form-label">
                            Password
                        </label>
                        <input type="password" class="form-control" v-model="password">
                    </div>
                    <button class="btn btn-primary w-100" @click="login">
                        Login
                    </button>
                    <div class="text-center mt-4">
                        Don't have an account?
                        <router-link to="/register">Register here</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {ref} from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
const router=useRouter()

const email=ref("")
const password=ref("")

async function login(){
    try{
        const response=await api.post("/auth/login", {
            email: email.value,
            password: password.value
        });
        console.log(response.data)

        localStorage.setItem("token", response.data.access_token)
        localStorage.setItem("role", response.data.role)
        localStorage.setItem("name", response.data.name)
        localStorage.setItem("user_id", response.data.user_id)
        if(response.data.role==="Admin"){
            router.push("/admin")
        }
        else if(response.data.role==="Trek Staff"){
            router.push("/staff")
        }
        else{
            router.push("/user")
        }
    }
    catch(error){
        console.log(error)
        alert(error.response.data.message)
    }
}
</script>

<style scoped>
.login-image{
    width: 100%;
    height: 100vh;
    object-fit: cover;
}

.login-card{
    width: 420px;
    border-radius: 20px;
}
</style>