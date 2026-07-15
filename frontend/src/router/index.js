import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/login.vue";
import Register from "../views/register.vue";
import AdminDashboard from "../views/admindashboard.vue";
import StaffDashboard from "../views/staffdashboard.vue";
import UserDashboard from "../views/userdashboard.vue";
import NotFound from "../views/notfound.vue";
import Home from "../views/home.vue";
import Forbidden from "../views/forbidden.vue"
import Treks from "../views/treks.vue";
import Staffs from "../views/staffmanagement.vue";
import Users from "../views/manageusers.vue";
import Bookings from "../views/bookings.vue";
import StaffTreks from "../views/stafftreks.vue";
import Participants from "../views/participants.vue";
import UserTreks from "../views/usertreks.vue";
import MyBookings from "../views/mybookings.vue";
import History from "../views/history.vue";
import Reports from "../views/reports.vue";
import Profile from "../views/profile.vue";

const routes = [
    {
        path: "/",
        component: Home
    },
    {
        path: "/login",
        component: Login
    },
    {
        path: "/register",
        component: Register
    },
    {
        path: "/admin",
        component: AdminDashboard,
        meta: {requiresAuth: true, role: "Admin"}
    },
    {
        path: "/staff",
        component: StaffDashboard,
        meta: { requiresAuth: true, role: "Trek Staff"}
    },
    {
        path: "/user",
        component: UserDashboard,
        meta: { requiresAuth: true, role: "Trekker"}
    },
    {
         path: "/admin/treks",
        component: Treks,
        meta: { requiresAuth: true, role: "Admin" }
    },
    {
        path: "/admin/staff",
        component: Staffs,
        meta: { requiresAuth: true, role: "Admin" }
    },
    {
        path: "/admin/users",
        component: Users,
        meta: { requiresAuth: true, role: "Admin"}
    },
    {
        path: "/admin/bookings",
        component: Bookings,
        meta: { requiresAuth: true, role: "Admin"}
    },
    {
        path: "/staff/treks",
        component: StaffTreks,
        meta:{ requiresAuth:true, role:"Trek Staff"}
    },
    {
        path: "/staff/participants/:id",
        component: Participants,
        meta:{
            requiresAuth:true,
            role:"Trek Staff"
        }
    },
    {
        path:"/user/treks",
        component:UserTreks,
        meta:{ requiresAuth:true, role:"Trekker"}
    },
    {
        path: "/user/bookings",
        component: MyBookings,
        meta:{
            requiresAuth:true,
            role:"Trekker"
        }
    },
    {
        path:"/user/history",
        component:History,
        meta:{
            requiresAuth:true,
            role:"Trekker"
        }
    },
    {
        path:"/admin/reports",
        component:Reports,
        meta:{
            requiresAuth:true,
            role:"Admin"
        }
    },
    {
        path:"/user/profile",
        component:Profile,
        meta: { requiresAuth: true, role: "Trekker"}
    },
    {
        path: "/403",
        component: Forbidden
    },
    {
        path: "/:pathMatch(.*)*",
        component: NotFound
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")

    if (to.meta.requiresAuth && !token) {
        return next("/login")
    }
    if (to.meta.role && role !== to.meta.role) {
        return next("/403")
    }
    next()
})

export default router;