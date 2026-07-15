<template>
<div class="card card-custom user-navbar mb-4">
    <div class="card-body">

        <div class="d-flex flex-wrap gap-2">

            <router-link
                to="/user"
                class="btn btn-outline-success">
                <i class="bi bi-house-door-fill me-2"></i>
                Dashboard
            </router-link>

            <router-link
                to="/user/treks"
                class="btn btn-outline-success">
                <i class="bi bi-signpost-split-fill me-2"></i>
                Explore Treks
            </router-link>

            <router-link
                to="/user/bookings"
                class="btn btn-outline-success">
                <i class="bi bi-calendar-check-fill me-2"></i>
                My Bookings
            </router-link>

            <router-link
                to="/user/history"
                class="btn btn-outline-success">
                <i class="bi bi-clock-history me-2"></i>
                History
            </router-link>

            <router-link
                to="/user/profile"
                class="btn btn-outline-success">
                <i class="bi bi-person-circle me-2"></i>
                Profile
            </router-link>

        </div>

    </div>
</div>    
</template>