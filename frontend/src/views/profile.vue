<template>
<div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <button
        class="btn btn-outline-secondary"
        @click="goBack">
        <i class="bi bi-arrow-left me-2"></i>
        Back
        </button>
        <h2 class="page-title">
            <i class="bi bi-person-circle me-2"></i>
            My Profile
        </h2>
    </div>

    <div class="row justify-content-center">
        <div class="col-lg-7">
            <div class="card card-custom">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-person-circle"
                        style="font-size:90px;color:var(--primary);">
                        </i>
                        <h4 class="mt-3"> {{ user.name }}</h4>
                        <p class="text-muted">{{ user.email }}</p>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input class="form-control"
                        v-model="user.name">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input class="form-control"
                        v-model="user.email" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input class="form-control"
                        v-model="user.phone">
                    </div>
                    <div class="d-grid">
                        <button
                        class="btn btn-primary"
                        @click="updateProfile">
                        <i class="bi bi-check-circle me-2"></i>
                        Update Profile
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const user = ref({
    name:"",
    email:"",
    phone:""
});
const router = useRouter();

function goBack() {
    router.back();
}

async function loadProfile(){

    try{
        const response = await api.get("/user/profile");
        user.value = response.data;
    }

    catch(error){
        console.log(error);
    }

}

async function updateProfile(){

    try{
        const response = await api.put(
            "/user/profile",
            {
                name:user.value.name,
                phone:user.value.phone
            }
        );

        alert(response.data.message);

    }

    catch(error){
        alert(error.response.data.message);
    }

}

onMounted(()=>{
    loadProfile();
});

</script>