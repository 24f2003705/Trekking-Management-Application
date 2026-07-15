<template>
    <div class="container-fluid vh-100">
        <div class="row h-100">
            <div class="col-lg-7 d-none d-lg-block p-0">
                <img src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80" class="register-image" alt="Mountain adventure scenery">
            </div>
            <div class="col-lg-5 d-flex align-items-center justify-content-center">
                <div class="card register-card p-5">
                    <h2 class="fw-bold mb-2"> Create Account</h2>
                    <p class="text-secondary mb-4">
                        Join Trekway and start your adventure
                    </p>
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input type="text" class="form-control" v-model="name">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" v-model="email">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password">
                    </div>
                    <div class="mb-4">
                        <label class="form-label">Confirm Password</label>
                        <input type="password" class="form-control" v-model="confirmPassword">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone Number</label>
                        <input type="text" class="form-control" v-model="phone">
                    </div>
                    <button class="btn btn-success w-100" @click="register">Register</button>
                    <div class="text-center mt-4">
                        Already have an account?
                        <router-link to="/login">Login</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const name = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const phone = ref("")

async function register(){
    if(password.value !== confirmPassword.value){
        alert("Password do not match")
        return
    }
    try{
        await api.post("/auth/register", {
            name:name.value,
            email:email.value,
            password:password.value,
            phone:phone.value
        })
        alert("Registration Successful")
        router.push("/login")
    }

    catch(error){
        alert(error.response?.data?.message || "Registration failed")
    }
}
</script>

<style scoped>
.register-image{
    width: 100%;
    height: 100vh;
    object-fit: cover;
}

.register-card{
    width: 430px;
    border-radius:20px;
}
</style>