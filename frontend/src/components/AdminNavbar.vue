<template>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <router-link
                class="navbar-brand"
                to="/admin">

                <i class="bi bi-tree-fill me-2"></i>
                TrekWay
            </router-link>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbar">

                <span class="navbar-toggler-icon"></span>

            </button>

            <div
                class="collapse navbar-collapse"
                id="navbar">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin">

                            <i class="bi bi-speedometer2 me-1"></i>
                            Dashboard

                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin/treks">

                            <i class="bi bi-signpost-split-fill me-1"></i>
                            Treks

                        </router-link>
                    </li>

                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin/staff">

                            <i class="bi bi-people-fill me-1"></i>
                            Staff

                        </router-link>
                    </li>

                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin/users">

                            <i class="bi bi-person-fill me-1"></i>
                            Users

                        </router-link>
                    </li>

                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin/bookings">

                            <i class="bi bi-calendar-check-fill me-1"></i>
                            Bookings

                        </router-link>
                    </li>

                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/admin/reports">

                            <i class="bi bi-bar-chart-fill me-1"></i>
                            Reports

                        </router-link>
                    </li>

                </ul>

                <button
                    class="btn btn-light"
                    @click="logout">

                    <i class="bi bi-box-arrow-right me-1"></i>
                    Logout

                </button>

            </div>

        </div>

    </nav>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function logout(){

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/login");

}
</script>