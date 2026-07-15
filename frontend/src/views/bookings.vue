<template>
    <AdminNavbar/>
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="page-title">
                    <i class="bi bi-calendar-check-fill me-2"></i>
                    Booking Management
                </h2>
                <p class="text-muted">View all Trek bookings</p>
            </div>
        </div>
        <div class="card p-4">
            <div class="input-group mb-4">
                <span class="input-group-text">
                    <i class="bi bi-search"></i>
                </span>
                <input 
                class="form-control"
                placeholder="Search Booking..."
                v-model="search">
            </div>
            <table class="table table-hover table-bordered align-middle">
                <thead class="table-success">
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Trek</th>
                        <th>Booking Status</th>
                        <th>Payment Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in filteredBookings"
                    :key="booking.booking_id">
                    <td>{{ booking.booking_id }}</td>
                    <td>{{ booking.user }}</td>
                    <td>{{ booking.trek }}</td>
                    <td>
                        <span class="badge" 
                        :class="booking.booking_status == 'Approved'
                        ? 'bg-success' : 'bg-warning'">
                        {{ booking.booking_status }} 
                        </span>
                    </td>
                    <td>
                        <span class="badge"
                        :class="booking.payment_status == 'Paid'
                        ? 'bg-success' : 'bg-warning'">
                        {{ booking.payment_status }}
                        </span>
                    </td>
                    </tr>
                </tbody>
            </table>
    </div>
</div>
</template>


<script setup>
import AdminNavbar from "../components/AdminNavbar.vue";
import { useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import api from "../services/api";
const bookings = ref([]);
const search = ref("");
const router = useRouter();

async function loadBookings(){
    try {
        const response = await api.get("/admin/bookings");
        bookings.value = response.data.bookings;
    }
    catch(error){
        console.log(error);
    }
}
const filteredBookings = computed(() => {
    return bookings.value.filter(booking =>
        booking.user.toLowerCase().includes(search.value.toLowerCase()) ||
        booking.trek.toLowerCase().includes(search.value.toLowerCase())
    );
});

onMounted(() => {
    loadBookings();
})

</script>