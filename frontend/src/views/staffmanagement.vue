

<template>
    <AdminNavbar/>
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="page-title">
                    <i class="bi bi-people-fill me-2"></i>
                    Staff Management
                </h2>
                <p class="text-muted">Empowering staff to deliver unforgettable adventures</p>
            </div>
            <button class="btn btn-primary"
            data-bs-toggle="modal"
            data-bs-target="#addStaffModal"
            @click="resetForm">
            <i class="bi bi-person-plus-fill me-2"></i>
                Add Staff
            </button>
        </div>
        <div class="card card-custom p-4">
            <div class="card-body">
                <h5 class="mb-4">
                <i class="bi bi-person-workspace me-2"></i>
                All Staff Members </h5>
            </div>
            <div class="input-group mb-4">
                <span class="input-group-text">
                    <i class="bi bi-search"></i>
                </span>
                <input
                class="form-control"
                placeholder="Search Staff..."
                v-model="search">
            </div>
            <table class="table table-hover align-middle table-bordered">
                <thead class="table-success">
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                <tr
                    v-for="staff in filteredStaff"
                    :key="staff.id">
                    <td>{{ staff.name }}</td>
                    <td>{{ staff.email }}</td>
                    <td>{{ staff.phone }}</td>
                    <td>
                        <span class="badge px-3 py-2"
                        :class="staff.status=='Active'
                        ?'bg-success' :'bg-danger'"> {{ staff.status }}</span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-warning me-2"
                        data-bs-toggle="modal"
                        data-bs-target="#addStaffModal"
                        @click="editStaff(staff)">
                        <i class="bi bi-pencil-square"></i>
                            Edit
                        </button>
                        <button class="btn btn-sm btn-danger"
                        @click="deleteStaff(staff.id)">
                        <i class="bi bi-trash-fill"></i>
                            Delete
                        </button>
                        <button class="btn btn-sm btn-secondary"
                        @click="toggleStatus(staff)">
                        {{ staff.status=="Active" ?"Deactivate" :"Activate" }}
                        </button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="modal fade" id="addStaffModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        {{ isEdit ? "Edit Staff" : "Add New Staff" }}
                    </h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Name</label>
                            <input type="text" class="form-control" v-model="form.name">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Email</label>
                            <input type="text" class="form-control" v-model="form.email">
                        </div>
                        <div class="col-md-6" v-if="!isEdit">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" v-model="form.password">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Phone</label>
                            <input type="text" class="form-control" v-model="form.phone">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Contact Details</label>
                            <input type="text" class="form-control" v-model="form.contact_details">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Experience</label>
                            <input type="number" class="form-control" v-model="form.experience">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button class="btn btn-success" @click="isEdit ? updateStaff() : saveStaff()">
                        {{ isEdit ? "Update Staff" : "Save Staff" }}
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
const staffs = ref([]);
const search = ref("");
const form = ref({
    name:"",
    email: "",
    password: "",
    phone: "",
    contact_details: "",
    experience: 0,
    status: "Active"

});

const isEdit = ref(false);
const editId = ref(null);

async function loadStaff(){
    try{
        const response = await api.get("/admin/staff");
        staffs.value = response.data.staffs;
    }
    catch(error){
        console.log(error);
    }
}

async function saveStaff() {
    try{
        const response=await api.post("/admin/staff", form.value);
        alert(response.data.message);
        await loadStaff();
    }
    catch(error){
        alert(error.response.data.message);
    }
    
}

async function updateStaff(){
    try {
        const response = await api.put(
            `/admin/staff/${editId.value}`,
            form.value
        );
        alert(response.data.message);
        await loadStaff();
        const modal = Modal.getInstance(document.getElementById("addStaffModal"));
        modal.hide();
        resetForm();
    }
     catch(error) {
        alert(error.response.data.message);
     }
}

async function deleteStaff(id) {

    const confirmDelete = confirm("Are you sure you want to delete Staff?");

    if(!confirmDelete) {
        return;
    }
    try {
        const response = await api.delete(`/admin/staff/${id}`);
        alert(response.data.message);
        await loadStaff()
    }

    catch(error) {
        alert(error.response.data.message);
    }
}
function editStaff(staff) {

    isEdit.value = true;
    editId.value = staff.id;

    form.value = {

        name:staff.name,
        email:staff.email,
        phone:staff.phone,
        status:staff.status,
        password:"",
        contact_details: staff.contact_details,
        experience:staff.experience

    };

}

function resetForm() {

    form.value = {

        name: "",
        email: "",
        password: "",
        phone: "",
        contact_details: "",
        experience: 0,
        status: "Active"

    };

    isEdit.value = false;
    editId.value = null;

}

async function toggleStatus(staff){

    try{

        await api.put(

            `/admin/staff/${staff.id}`,

            {

                status:

                staff.status=="Active"

                ?"Inactive"

                :"Active"

            }

        );

        await loadStaff();

    }

    catch(error){

        alert(error.response.data.message);

    }

}

const filteredStaff = computed(() => {
    return staffs.value.filter((staff) =>
    staff.name .toLowerCase() .includes(search.value.toLowerCase())
    );
});

onMounted(() => {
    loadStaff();
});
</script>