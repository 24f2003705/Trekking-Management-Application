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
                <i class="bi bi-signpost-split-fill me-2"></i>
                Explore Treks</h2>
            <p class="text-muted">Browse and book your next trekking adventure</p>
        </div>
    </div>
    <div class="card p-4">
        <div class="row g-3 mb-4">

            <div class="col-lg-3">
                <input
                    class="form-control"
                    placeholder="Search Trek..."
                    v-model="search">
            </div>

            <div class="col-lg-2">
                <select
                    class="form-select"
                    v-model="difficulty">
                    <option value="">Difficulty</option>
                    <option>Easy</option>
                    <option>Moderate</option>
                    <option>Hard</option>
                </select>
            </div>

            <div class="col-lg-2">
                <input
                    class="form-control"
                    placeholder="Location"
                    v-model="location">
            </div>

            <div class="col-lg-2">
                <input
                    type="number"
                    class="form-control"
                    placeholder="Duration"
                    v-model="duration">
            </div>

            <div class="col-lg-1 d-grid">
                <button
                    class="btn btn-primary"
                    @click="searchTreks">

                    <i class="bi bi-search"></i>

                </button>
            </div>

            <div class="col-lg-1 d-grid">
                <button
                    class="btn btn-success"
                    @click="filterTreks">

                    <i class="bi bi-funnel-fill"></i>

                </button>
            </div>

            <div class="col-lg-1 d-grid">
                <button
                    class="btn btn-secondary"
                    @click="loadTreks">

                    <i class="bi bi-arrow-clockwise"></i>

                </button>
            </div>

        </div>
        <table class="table table-bordered table-hover">
            <thead class="table-success">
                <tr>

                    <th>Name</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Available Slots</th>
                    <th>Start Date</th>
                    <th>End date</th>
                    <th>Action</th>

                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="trek in treks"
                    :key="trek.id">

                    <td>{{ trek.trek_name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td>{{ trek.duration }}</td>
                    <td>{{ trek.available_slots }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>{{ trek.end_date }}</td>

                    <td>

                        <button
                            class="btn btn-success btn-sm"
                            @click="bookTrek(trek.id)">
                            Book
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
import{ useRouter } from "vue-router";

const treks = ref([]);
const search = ref("");
const difficulty = ref("");
const location = ref("");
const duration = ref("");
const router = useRouter();

function goBack() {
    router.back();
}

async function loadTreks() {

    try {
        const response = await api.get("/user/treks");
        treks.value = response.data;
    }

    catch(error) {
        console.log(error);
    }

}

async function searchTreks() {

    if(search.value==""){
        loadTreks();
        return;
    }

    try{

        const response = await api.get(
            `/user/search?name=${search.value}`
        );
        treks.value = response.data;

    }

    catch(error){
        console.log(error);
    }

}
async function filterTreks() {

    try {
        const response = await api.get("/user/filter", {
            params: {
                difficulty: difficulty.value,
                location: location.value,
                duration: duration.value
            }
        });

        treks.value = response.data;

    }

    catch(error) {
        console.log(error);
    }
}

async function bookTrek(id){

    if(!confirm("Book this trek?")){
        return;
    }

    try{

        const response = await api.post(
            "/user/book",
            {
                trek_id:id
            }
        );

        alert(response.data.message);
        loadTreks();

    }

    catch(error){
        alert(error.response.data.message);
    }

}

onMounted(()=>{
    loadTreks();
});

</script>