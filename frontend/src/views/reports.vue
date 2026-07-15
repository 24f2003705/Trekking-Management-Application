<template>
<AdminNavbar/>
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="page-title">
                <i class="bi bi-bar-chart-fill me-2"></i>
                Reports & Analytics
            </h2>
            <p class="text-muted">
                Monitor trekking statistics and generate reports.
            </p>
        </div>
        <button
        class="btn btn-success"
        @click="openReport">
            <i class="bi bi-file-earmark-text me-2"></i>
            Monthly Report
        </button>
    </div>
    <div class="row">
        <div class="col-md-4 mb-3">
            <div class="card p-3 text-center">
                <h5>Total Treks</h5>
                <h2>{{ dashboard.total_treks }}</h2>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card p-3 text-center">
                <h5>Total Staff</h5>
                <h2>{{ dashboard.total_staff }}</h2>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="card p-3 text-center">
                <h5>Total Users</h5>
                <h2>{{ dashboard.total_users }}</h2>
            </div>
        </div>
        <div class="col-md-6 mb-3">
            <div class="card p-3 text-center">
                <h5>Total Bookings</h5>
                <h2>{{ dashboard.total_bookings }}</h2>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card p-3 text-center">
                <h5>Open Treks</h5>
                <h2>{{ dashboard.open_treks }}</h2>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card p-3 text-center">
                <h5>Completed Treks</h5>
                <h2>{{ dashboard.completed_treks }}</h2>
            </div>
        </div>
    </div>
    <div class="card card-custom mt-4">
        <div class="card-body">
            <h4 class="mb-4">
                <i class="bi bi-bar-chart-line-fill me-2"></i>
                Booking Statistics
            </h4>
            <canvas id="bookingChart"></canvas>
        </div>
    </div>
</div>
</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../services/api";
import Chart from "chart.js/auto";
import AdminNavbar from "../components/AdminNavbar.vue";

const dashboard = ref({});
const bookingReport = ref({});

async function openReport() {

    try {
        const response = await api.get(
            "/admin/reports/monthly",
            {
                responseType: "blob"
            }
        );

        const blob = new Blob(
            [response.data],
            {
                type: "text/html"
            }
        );

        const url = window.URL.createObjectURL(blob);
        window.open(url, "_blank");
    }

    catch(error) {
        alert(error.response?.data?.message || "Unable to open report");
    }

}

async function loadReports(){

    const dashboardRes = await api.get("/admin/reports/dashboard");
    dashboard.value = dashboardRes.data;

    const bookingRes = await api.get("/admin/reports/bookings");
    bookingReport.value = bookingRes.data;

    new Chart(document.getElementById("bookingChart"),{

        type:"bar",

        data:{

            labels:["Booked","Completed","Cancelled"],
            datasets:[{
                label:"Bookings",
                data:[

                    bookingReport.value.booked,
                    bookingReport.value.completed,
                    bookingReport.value.cancelled
                ],
                backgroundColor:[
                    "#40916c",
                    "#2d6a4f",
                    "#d4a373"
                ]
            }]
        }
    });

}

onMounted(()=>{
    loadReports();
});

</script>