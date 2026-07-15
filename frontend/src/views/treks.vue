

<template>
    <AdminNavbar />
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="page-title">
                    <i class="bi bi-signpost-split-fill me-2"></i>
                    Trek Management
                </h2>
                <p class="text-muted">Manage trekking events, locations and schedules</p>
            </div>
            <button class="btn btn-primary px-4"
            data-bs-toggle="modal"
            data-bs-target="#addTrekModal"
            @click="resetForm">
                <i class="bi bi-plus-circle me-2"></i>
                Add Trek
            </button>
        </div>
        <div class="card card-custom p-4">
            <div class="card-body">
                <h5 class="mb-4">
                <i class="bi bi-map-fill me-2"></i>
                All Treks </h5>
            </div>
            <div class="input-group mb-4">
                <span class="input-group-text">
                    <i class="bi bi-search"></i>
                </span>

                <input
                class="form-control"
                placeholder="Search trek..."
                v-model="search">

            </div>
            <table class="table table-hover align-middle table-bordered">
                <thead class="table-success">
                    <tr>
                        <th>Name</th>
                        <th>Location</th>
                        <th>Difficulty</th>
                        <th>Duration</th>
                        <th>Total Slots</th>
                        <th>Available Slots</th>
                        <th>Status</th>
                        <th>Assigned Staff</th>
                        <th>Startdate</th>
                        <th>EndDate</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                <tr
                    v-for="trek in filteredTreks"
                    :key="trek.id">
                    <td>{{ trek.trek_name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td>{{ trek.duration }}</td>
                    <td>{{ trek.total_slots }}</td>
                    <td>{{ trek.available_slots }}</td>
                    <td>{{ trek.status }}</td>
                    <td>{{ trek.assigned_staff }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>{{ trek.end_date }}</td>
                    <td>
                        <button class="btn btn-sm btn-warning me-2"
                        data-bs-toggle="modal"
                        data-bs-target="#addTrekModal"
                        @click="editTrek(trek)">
                        <i class="bi bi-pencil-square"></i>
                            Edit
                        </button>

                        <button class="btn btn-sm btn-danger"
                        @click="deleteTrek(trek.id)">
                        <i class="bi bi-trash-fill"></i>
                            Delete
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="modal fade" id="addTrekModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="bi bi-map-fill me-2"></i>
                        {{ isEdit ? "Edit Trek" : "Add New Trek" }}
                    </h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Trek Name</label>
                            <input type="text" class="form-control" v-model="form.trek_name">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Location</label>
                            <input type="text" class="form-control" v-model="form.location">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Difficulty</label>
                            <select class="form-select" v-model="form.difficulty">
                                <option>Easy</option>
                                <option>Moderate</option>
                                <option>Hard</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Duration (Days)</label>
                            <input type="number" class="form-control" v-model="form.duration">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Total Slots</label>
                            <input type="number" class="form-control" v-model="form.total_slots">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Assign Staff</label>
                            <select class="form-select" v-model="form.assigned_staff_id">
                                <option :value="null">Select Staff</option>
                                <option 
                                v-for="staff in staffList"
                                :key="staff.id"
                                :value="staff.id"> {{ staff.name }}</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Start Date</label>
                            <input type="date" class="form-control" v-model="form.start_date">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">End Date</label>
                            <input type="date" class="form-control" v-model="form.end_date">
                        </div>
                        <div class="col-12">
                            <label class="form-label">Description</label>
                            <textarea rows="3" class="form-control" v-model="form.description"></textarea>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button class="btn btn-success" @click="isEdit ? updateTrek() : saveTrek()">
                        {{ isEdit ? "Update Trek" : "Save Trek" }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import AdminNavbar from "../components/AdminNavbar.vue";
import { useRouter } from "vue-router";
import { Modal } from "bootstrap";
import { ref, computed, onMounted } from "vue";
import api from "../services/api";
const router = useRouter();
const treks = ref([]);
const search = ref("");
const form = ref({
    trek_name:"",
    location: "",
    description: "",
    difficulty: "",
    duration: "",
    total_slots: "",
    assigned_staff_id:null,
    start_date: "",
    end_date: ""

});

const isEdit = ref(false);
const editId = ref(null);
const staffList = ref([]);

async function loadTreks(){
    try{
        const response = await api.get("/admin/treks");
        console.log("Response =", response.data);
        console.log("Treks =", response.data.treks);
        console.log("Length =", response.data.treks.length);
        console.log("Is Array =", Array.isArray(response.data.treks));

        treks.value = response.data.treks;
    }
    catch(error){
        console.log(error);
    }
}

async function saveTrek() {
    try{
        await api.post("/admin/treks", form.value);
        
        await loadTreks();
        const modalElement = document.getElementById("addTrekModal");
        const modal = Modal.getInstance(modalElement);
        if (modal){
            modal.hide();
        }
        alert("Trek added successfully");
    }
    catch(error){
        alert(error.response.data.message);
    }
    
}

async function updateTrek(){
    try {
        const response = await api.put(
            `/admin/treks/${editId.value}`,
            form.value
        );
        alert(response.data.message);
        await loadTreks();
        const modal = Modal.getInstance(document.getElementById("addTrekModal"));
        modal.hide();
        resetForm();
    }
     catch(error) {
        alert(error.response.data.message);
     }
}

async function deleteTrek(id) {

    const confirmDelete = confirm("Are you sure you want to delete this trek?");

    if(!confirmDelete) {
        return;
    }
    try {
        const response = await api.delete(`/admin/treks/${id}`);
        alert(response.data.message);
        await loadTreks()
    }

    catch(error) {
        alert(error.response.data.message);
    }
}
function editTrek(trek) {

    isEdit.value = true;
    editId.value = trek.id;

    form.value = {

        trek_name: trek.trek_name,
        location: trek.location,
        description: trek.description,
        difficulty: trek.difficulty,
        duration: trek.duration,
        total_slots: trek.total_slots,
        available_slots: trek.available_slots,
        status: trek.status,
        assigned_staff_id: trek.assigned_staff_id,
        start_date: trek.start_date,
        end_date: trek.end_date

    };

}

function resetForm() {

    form.value = {

        trek_name: "",
        location: "",
        description: "",
        difficulty: "Easy",
        duration: "",
        total_slots: "",
        assigned_staff_id: null,
        start_date: "",
        end_date: ""

    };

    isEdit.value = false;
    editId.value = null;

}

async function loadStaff() {
    try {
        const response = await api.get("/admin/staff");
        staffList.value = response.data.staffs;
    }
    catch(error){
        console.log(error);
    }
}
const filteredTreks = computed(() => {
    return treks.value.filter((trek) =>
    trek.trek_name.toLowerCase().includes(search.value.toLowerCase())
    );
});

onMounted(() => {
    loadTreks();
    loadStaff();
});
</script>