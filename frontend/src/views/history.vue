<template>
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="page-title">
            Trekking History
            </h2>
            <p class="text-muted">View all your completed trekking adventures</p>
        </div>
        <button
        class="btn btn-success"
        @click="exportHistory">
        <i class="bi bi-download me-2"></i>
        Export CSV
        </button>
    </div>
    <div class="card p-4">
        <table class="table table-bordered table-hover">
            <thead class="table-success">
                <tr>

                    <th>Trek</th>
                    <th>Location</th>
                    <th>Booking Date</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>

                </tr>
            </thead>
            <tbody>

                <tr
                    v-for="history in histories"
                    :key="history.booking_id">

                    <td>{{ history.trek_name }}</td>
                    <td>{{ history.location }}</td>
                    <td>{{ history.booking_date }}</td>
                    <td>{{ history.start_date }}</td>
                    <td>{{ history.end_date }}</td>
                    <td>

                        <span class="badge bg-success">

                            {{ history.status }}

                        </span>

                    </td>

                </tr>

            </tbody>
        </table>
    </div>
    <div
    v-if="exportStatus.status == 'Ready'"
    class="card card-custom mt-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5>
                        <i class="bi bi-file-earmark-spreadsheet-fill text-success me-2"></i>
                        Latest Export
                    </h5>
                    <p class="text-muted mb-0">
                        {{ exportStatus.filename }}
                    </p>

                    <small class="text-success">
                        <i class="bi bi-check-circle-fill me-1"></i>
                        Ready to Download
                    </small>

                </div>

                <button
                class="btn btn-success"
                @click="downloadCSV">
                    <i class="bi bi-download me-2"></i>
                    Download CSV
                </button>

            </div>
        </div>
    </div>
    <div class="mt-3">
        <button
            class="btn btn-outline-secondary"
            @click="goBack">
            <i class="bi bi-arrow-left me-2"></i>
            Back
        </button>
    </div>
</div>
</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const histories = ref([]);
const exportStatus = ref({});
const router = useRouter();

function goBack() {
    router.back();
}

async function exportHistory(){

    try{

        const response = await api.post("/user/export-history");

        alert(response.data.message);
        setTimeout(() => {
            loadExportStatus();
        },1500);

    }

    catch(error){

        alert(error.response.data.message);

    }

}

async function loadHistory(){

    try{
        const response = await api.get("/user/history");
        histories.value = response.data;
    }

    catch(error){
        console.log(error);
    }

}

async function loadExportStatus() {

    try {
        const response = await api.get("/user/latest-export");
        exportStatus.value = response.data;
    }

    catch(error) {
        console.log(error);
    }

}

async function downloadCSV() {

    try {

        const response = await api.get(
            "/user/download-export",
            {
                responseType: "blob"
            }
        );

        const url = window.URL.createObjectURL(
            new Blob([response.data])
        );

        const link = document.createElement("a");

        link.href = url;
        link.download = exportStatus.value.filename;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        window.URL.revokeObjectURL(url);

    }

    catch(error) {

        alert(error.response?.data?.message || "Unable to download CSV");

    }

}

onMounted(()=>{
    loadHistory();
    loadExportStatus();
});

</script>