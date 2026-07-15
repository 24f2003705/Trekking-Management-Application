<template>

    <AdminNavbar />

    <div class="container-fluid py-4">

        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="page-title">
                    Welcome, Admin
                </h2>

                <p class="text-muted">
                    Manage your trekking organization efficiently
                </p>
            </div>

            <div class="text-end">
                <small class="text-muted">
                    Today
                </small>
                <h6>{{ new Date().toLocaleDateString() }}</h6>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-lg-3 col-md-6">
                <div class="card card-custom p-4 h-100">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="stat-title">
                                Total Treks
                            </div>
                            <div class="stat-number">

                                {{ dashboard.total_treks }}

                            </div>
                        </div>
                        <i class="bi bi-signpost-split-fill dashboard-icon text-success"></i>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card card-custom p-4 h-100">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="stat-title">

                                Staff Members

                            </div>
                            <div class="stat-number">
                                {{ dashboard.total_staff }}
                            </div>

                        </div>
                        <i class="bi bi-people-fill dashboard-icon text-primary"></i>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card card-custom p-4 h-100">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="stat-title">

                                Total Bookings

                            </div>
                            <div class="stat-number">

                                {{ dashboard.total_bookings }}

                            </div>
                        </div>
                        <i class="bi bi-calendar-check-fill dashboard-icon text-warning"></i>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="card card-custom p-4 h-100">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="stat-title">

                                Trekkers

                            </div>

                            <div class="stat-number">

                                {{ dashboard.total_users }}

                            </div>
                        </div>
                        <i class="bi bi-person-fill dashboard-icon text-danger"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import AdminNavbar from "../components/AdminNavbar.vue";

const dashboard = ref({
    total_treks: 0,
    total_staff: 0,
    total_bookings: 0,
    total_users: 0
});

async function loadDashboard() {
    try{
        const response = await api.get("/admin/dashboard");
        console.log(response.data);
        dashboard.value = response.data;
    }
    catch (error) {
        console.log(error);
    }
}

onMounted(() => {
    loadDashboard();
});
</script>