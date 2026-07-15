<template>
    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="mb-4">
                <h2 class="page-title">
                    <i class="bi bi-person-workspace me-2"></i>
                    Welcome, {{ dashboard.staff_name }}
                </h2>
                <p class="text-muted">
                    Manage your assigned treks and participants
                </p>
            </div>
            <button class="btn btn-outline-success"
            @click="logout">
            <i class="bi bi-box-arrow-right me-2"></i>
            Logout
            </button>
        </div>
        <div class="row g-4">
            <div class="col-md-3">
                <div class="card card-custom">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="stat-title"> Assigned Treks</div>
                                <div class="stat-number">{{ dashboard.assigned_treks }}</div>
                            </div>
                            <i class="bi bi-signpost-split-fill dashboard-icon text-success"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-custom">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="stat-title"> Open Treks</div>
                                <div class="stat-number">{{ dashboard.open_treks }}</div>
                            </div>
                            <i class="bi bi-unlock-fill dashboard-icon text-success"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-custom">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="stat-title"> Completed Treks</div>
                                <div class="stat-number">{{ dashboard.completed_treks }}</div>
                            </div>
                            <i class="bi bi-check-circle-fill dashboard-icon text-success"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-custom">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="stat-title"> Total Participants</div>
                                <div class="stat-number">{{ dashboard.total_participants }}</div>
                            </div>
                            <i class="bi bi-people-fill dashboard-icon text-success"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card card-custom mt-4">
            <div class="card-body">
                <h4>
                    <i class="bi bi-lightning-fill me-2"></i>
                    Quick Actions
                </h4>
                <div class="mt-4">
                    <router-link
                    class="btn btn-primary me-3"
                    to="/staff/treks">
                        <i class="bi bi-map me-2"></i>
                        Assigned Treks
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api"
const dashboard = ref({});
import { useRouter } from "vue-router";

const router = useRouter();
function logout() {

    if (!confirm("Are you sure you want to logout?")) return;

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/login");
}

async function loadDashboard() {
    try{
        const response = await api.get("/staff/dashboard");
        dashboard.value = response.data;
    }
    catch(error){
        console.log(error);
    }
}

onMounted(() => {
    loadDashboard();
})
</script>