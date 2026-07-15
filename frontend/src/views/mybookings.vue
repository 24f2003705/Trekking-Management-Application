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
                <i class="bi bi-calendar-check-fill me-2"></i>
                My Bookings</h2>
            <p class="text-muted">Your current trek bookings</p>
        </div>
    </div>
    <div class="card p-4">
        <table class="table table-bordered table-hover">
            <thead table-success>
                <tr>

                    <th>Trek</th>
                    <th>Location</th>
                    <th>Booking Date</th>
                    <th>Trek Status</th>
                    <th>Booking Status</th>
                    <th>Payment</th>
                    <th>Action</th>

                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="booking in bookings"
                    :key="booking.booking_id">

                    <td>{{ booking.trek_name }}</td>
                    <td>{{ booking.location }}</td>
                    <td>{{ booking.booking_date }}</td>
                    <td>{{ booking.trek_status }}</td>
                    <td>{{ booking.booking_status }}</td>
                    <td>{{ booking.payment_status }}</td>

                    <td>

                        <button
                            class="btn btn-danger btn-sm"
                            @click="cancelBooking(booking.booking_id)"
                            :disabled="
                                booking.booking_status=='Cancelled' ||
                                booking.booking_status=='Completed'">
                            Cancel
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

const bookings = ref([]);
const router = useRouter();

function goBack() {
    router.back();
}

async function loadBookings(){

    try{
        const response = await api.get("/user/bookings");
        bookings.value = response.data;
    }

    catch(error){
        console.log(error);
    }

}

async function cancelBooking(id){

    if(!confirm("Cancel this booking?")){
        return;
    }

    try{
        const response = await api.put(`/user/cancel_booking/${id}`);

        alert(response.data.message);

        loadBookings();
    }

    catch(error){

        alert(error.response.data.message);

    }

}

onMounted(()=>{
    loadBookings();
});

</script>