
<template>
    <AdminNavbar/>
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="page-title">
                    <i class="bi bi-person-fill me-2"></i>
                    User Management
                </h2>
                <p class="text-muted">Where every trail tells a story</p>
            </div>
        </div>
        <div class="card card-custom p-4">
            <div class="card-body">
                <h5 class="mb-4">
                <i class="bi bi-person me-2"></i>
                All Users </h5>
            </div>
            <div class="input-group mb-4">
                <span class="input-group-text">
                    <i class="bi bi-search"></i>
                </span>
                <input
                class="form-control"
                placeholder="Search Trekker.."
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
                    v-for="user in filteredUsers"
                    :key="user.id">
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.phone }}</td>
                    <td>
                        <span class="badge"
                        :class="user.status=='Active'
                        ?'bg-success' :'bg-danger'"> {{ user.status }}</span>
                    </td>
                    <td>
                        <button class="btn btn-sm"
                        :class="user.status == 'Active' ? 'btn-danger' : 'btn-success'"
                        @click="toggleStatus(user)">
                        {{ user.status=="Active" ?"Deactivate" :"Activate" }}
                        </button>
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
const users = ref([]);
const search = ref("");
const router = useRouter();

async function loadUser(){
    try{
        const response = await api.get("/admin/users");
        users.value = response.data.users;
    }
    catch(error){
        console.log(error);
    }
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

async function toggleStatus(user){

    try{
        const response = await api.put(
            `/admin/users/${user.id}/status`,
            {
                status:
                user.status == "Active" ? "Inactive" : "Active"
            }
        );
        alert(response.data.message);
        await loadUser();
    }
    catch(error) {
        alert(error.response.data.message);
    }
}

const filteredUsers = computed(() => {
    return users.value.filter((user) =>
    user.name .toLowerCase() .includes(search.value.toLowerCase())
    );
});

onMounted(() => {
    loadUser();
});
</script>