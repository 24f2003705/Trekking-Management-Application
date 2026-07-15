<template>
<UserNavbar/>
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="page-title">
                <i class="bi bi-person-fill me-2"></i>
                Welcome Trekker
            </h2>
            <p class="text-muted">
                Explore adventures and manage your trekking journey
            </p>
        </div>
        <button
        class="btn btn-outline-success"
        @click="logout">
        <i class="bi bi-box-arrow-right me-2"></i>
        Logout
        </button>
    </div>

    <div class="row g-4">
        <div class="col-md-3">
            <div class="card card-custom h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="stat-title">Total Bookings</div> 
                            <div class="stat-number">{{ dashboard.total_bookings }}</div>
                        </div>
                    </div>
                    <i class="bi bi-calendar-check-fill dashboard-icon text-success"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-custom h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="stat-title">Active Bookings</div> 
                            <div class="stat-number">{{ dashboard.active_bookings }}</div>
                        </div>
                    </div>
                    <i class="bi bi-activity dashboard-icon text-success"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-custom h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="stat-title">Completed Bookings</div> 
                            <div class="stat-number">{{ dashboard.completed_treks }}</div>
                        </div>
                    </div>
                    <i class="bi bi-check-circle-fill dashboard-icon text-success"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card card-custom h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="stat-title">Cancelled Bookings</div> 
                            <div class="stat-number">{{ dashboard.cancelled_bookings }}</div>
                        </div>
                    </div>
                    <i class="bi bi-x-circle-fill dashboard-icon text-success"></i>
                </div>
            </div>
        </div>
    </div>
    <div class="card card-custom mt-4">
    <div class="card-body">

        <h4>
            <i class="bi bi-tree-fill me-2 text-success"></i>
            Ready for Your Next Adventure?
        </h4>

        <p class="text-muted mb-3">
            Explore new trekking destinations, book upcoming adventures,
            and keep track of your trekking journey.
        </p>

        <div class="row text-center">

            <div class="col-md-4">
                <i class="bi bi-signpost-split-fill fs-2 text-success"></i>
                <h6 class="mt-2">Explore</h6>
                <small class="text-muted">
                    Find exciting treks
                </small>
            </div>

            <div class="col-md-4">
                <i class="bi bi-compass-fill fs-2 text-warning"></i>
                <h6 class="mt-2">Adventure</h6>
                <small class="text-muted">
                    Track your bookings
                </small>
            </div>

            <div class="col-md-4">
                <i class="bi bi-award-fill fs-2 text-primary"></i>
                <h6 class="mt-2">Achievement</h6>
                <small class="text-muted">
                    Complete more treks
                </small>
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
import UserNavbar from "../components/UserNavbar.vue";

const router = useRouter();
const dashboard = ref({});

function logout() {

    if(!confirm("Logout from your account?")) return;

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/login");

}

async function loadDashboard() {

    try {
        const response = await api.get("/user/dashboard");
        dashboard.value = response.data;
    }
    catch(error) {
        console.log(error);
    }

}

onMounted(() => {
    loadDashboard();
});

</script>