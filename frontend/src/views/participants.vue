<template>
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <button
        class="btn btn-outline-secondary"
        @click="goBack">
        <i class="bi bi-arrow-left me-2"></i>
        Back
        </button>
        <div class="text-end">
            <h2 class="page-title mb-0">
                <i class="bi bi-people-fill me-2"></i>
                Participants</h2>
            <p class="text-muted">{{ trekName }}</p>
        </div>
    </div>
    <div class="card p-4">
        <table class="table table-bordered table-hover">
            <thead class="table-success">
                <tr>
                    <th>Booking ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Booking Status</th>
                    <th>Payment Status</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="participant in participants"
                    :key="participant.booking_id">

                    <td>{{ participant.booking_id }}</td>
                    <td>{{ participant.name }}</td>
                    <td>{{ participant.email }}</td>
                    <td>{{ participant.phone }}</td>
                    <td>{{ participant.booking_status }}</td>
                    <td>{{ participant.payment_status }}</td>

                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const participants = ref([]);
const trekName = ref("");
const router = useRouter();

function goBack() {
    router.back();
}

async function loadParticipants() {

    try {
        const response = await api.get(
            `/staff/treks/${route.params.id}/participants`
        );

        participants.value = response.data.participants;
        trekName.value = response.data.trek_name;
    }

    catch(error) {
        console.log(error);
    }

}

onMounted(() => {
    loadParticipants();
});

</script>