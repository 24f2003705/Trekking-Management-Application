<template>
    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <button
            class="btn btn-outline-secondary"
            @click="goBack">
            <i class="bi bi-arrow-left me-2"></i>
            Back
            </button>
            <div class="text-end">
                <h2 class="page-title mb-0">
                    <i class="bi bi-map-fill me-2"></i>
                    Assigned Treks
                </h2>
                <p class="text-muted">
                    Manage trek progress, slots and participants
                </p>
            </div>
        </div>
    </div>
    <div class="card  card-custom">
        <div class="card-body">
            <table class="table table-bordered table-hover">
                <thead class="table-success">
                    <tr>
                        <th>Name</th>
                        <th>Location</th>
                        <th>Difficulty</th>
                        <th>Durartion</th>
                        <th>Total Slots</th>
                        <th>Available Slots</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Status</th>
                        <th>Action</th> 
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="trek in treks"
                    :key="trek.id">
                        <td>{{ trek.trek_name }}</td>
                        <td>{{ trek.location }}</td>
                        <td>{{ trek.difficulty }}</td>
                        <td>{{ trek.duration }}</td>
                        <td>{{ trek.total_slots }}</td>
                        <td>{{ trek.available_slots }}</td>
                        <td>{{ trek.start_date }}</td>
                        <td>{{ trek.end_date }}</td>
                        <td>
                            <span class="badge bg-primary">
                                {{ trek.status }}
                            </span>
                        </td>
                        <td>
                            <button class="btn btn-warning btn-sm me-2"
                            @click="updateStatus(trek)">
                            <i class="bi bi-pencil-square"></i>
                            Status
                            </button>
                            <button class="btn btn-info btn-sm me-2"
                            @click="updateSlots(trek)">
                            <i class="bi bi-grid"></i>
                            Slots
                            </button>
                            <button class="btn btn-success btn-sm" @click="viewParticipants(trek.id)">
                            <i class="bi bi-people-fill"></i>
                            Participants
                            </button>
                            <button class="btn btn-danger btn-sm ms-2"
                            @click="completeTrek(trek.id)">
                            <i class="bi bi-check-circle-fill"></i>
                            Complete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const router = useRouter();

const treks = ref([]);

function goBack() {
    router.back();
}

function viewParticipants(id){
    router.push(`/staff/participants/${id}`);
}

async function loadTreks() {

    try {

        const response = await api.get("/staff/treks");
        treks.value = response.data.assigned_treks;

    }
    catch(error) {
        console.log(error);
    }

}
async function updateStatus(trek) {
    const status = prompt(
        "Enter Status:\nPending\nOpen\nClosed\nOngoing\nCompleted",
        trek.status
    );

    if(!status) return;
    try {
        const response = await api.put(
            `/staff/treks/${trek.id}/status`,
            {
                status: status
            }

        );

        alert(response.data.message);

        loadTreks();

    }
     catch(error) {
        alert(error.response.data.message);
    }
}
async function updateSlots(trek) {
    const slots = prompt(
        "Available Slots",
        trek.available_slots
    );

    if(slots == null) return;

    try {

        const response = await api.put(
            `/staff/treks/${trek.id}/slots`,
            {
                available_slots: Number(slots)
            }

        );

        alert(response.data.message);

        loadTreks();

    }

    catch(error) {
        alert(error.response.data.message);
    }

}

async function completeTrek(id) {

    if(!confirm("Mark this trek as completed?")) return;

    try {

        const response = await api.put(
            `/staff/treks/${id}/complete`
        );

        alert(response.data.message);

        loadTreks();

    }

    catch(error) {
        alert(error.response.data.message);
    }

}

onMounted(() => {

    loadTreks();

});
</script>