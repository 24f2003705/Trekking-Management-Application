<template>
    <div>
        <!--Navbar-->
        <nav class="navbar navbar-expand-lg bg-white shadow-sm py-3">
            <div class="container">
                <router-link class="navbar-brand fw-bold text-success fs-3" to="/">
                    TrekWay
                </router-link>
                <div>
                    <router-link to="/login" class="btn btn-outline-success me-2">
                        Login
                    </router-link>
                    <router-link to="/register" class="btn btn-success">
                        Register
                    </router-link>
                </div>
            </div>
        </nav>

        <!--Hero-->
        <section class="hero">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h1 class="display-3 fw-bold mb-4">
                            Adventure
                            <br>
                            Starts Here
                        </h1>
                        <p class="lead text-secondary mb-4">
                            Find the perfect trek, book instantly, and create unforgettable memories
                        </p>
                        <router-link to="/login" class="btn btn-success btn-lg px-4">
                            Explore Treks
                        </router-link>
                    </div>
                    <div class="col-lg-6">
                        <img src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80" class="img-fluid rounded-4 hero-image" alt="Mountain trek scenery">
                    </div>
                </div>
            </div>
        </section>

        <!--popular-->
        <section class="container py-5">
            <h2 class="text-center mb-5">
                Popular Treks
            </h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="card trek-card">
                        <img src="https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&w=900&q=80" class="card-img-top" alt="Kedarkantha trek landscape">
                        <div class="card-body">
                            <h5>Kedarkantha Trek</h5>
                            <p class="text-secondary">Uttarakhand</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card trek-card">
                        <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=900&q=80" class="card-img-top" alt="Hampta Pass trek landscape">
                        <div class="card-body">
                            <h5>Hampta Pass</h5>
                            <p class="text- secondary">Himachal Pradesh</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card trek-card">
                        <img src="https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80" class="card-img-top" alt="Valley of Flowers trek landscape">
                        <div class="card-body">
                            <h5>valley of flowers</h5>
                            <p class="text-secondary">Uttarakhand</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="container py-5">
            <h2 class="text-center mb-5">
            Why Choose TrekWay?
            </h2>

            <div class="row text-center g-4">

                <div class="col-md-4">
                    <i class="bi bi-shield-check display-4 text-success"></i>
                    <h5 class="mt-3">Safe Adventures</h5>
                    <p class="text-muted">
                        Verified trekking routes and experienced Trek Staff
                    </p>
                </div>

                <div class="col-md-4">
                    <i class="bi bi-calendar-check display-4 text-success"></i>
                    <h5 class="mt-3">Easy Booking</h5>
                    <p class="text-muted">
                        Book your favourite trek in just a few clicks
                    </p>
                </div>

                <div class="col-md-4">
                    <i class="bi bi-tree-fill display-4 text-success"></i>
                    <h5 class="mt-3">Amazing Destinations</h5>
                    <p class="text-muted">
                        Explore mountains, forests and beautiful landscapes
                    </p>
                </div>

            </div>

        </section>
        <section class="bg-success text-white py-5">

            <div class="container">
                <div class="row text-center">
                    <div class="col-md-3">
                        <h2>100+</h2>
                        <p>Treks</p>
                    </div>

                    <div class="col-md-3">
                    <h2>500+</h2>
                    <p>Trekkers</p>
                    </div>

                    <div class="col-md-3">
                    <h2>50+</h2>
                    <p>Guides</p>
                    </div>

                    <div class="col-md-3">
                    <h2>15+</h2>
                    <p>Locations</p>
                    </div>

                </div>

            </div>

        </section>
        <footer class="footer">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <h4 class="fw-bold text-success">
                            TrekWay
                        </h4>

                        <p class="text-muted mb-0">
                            Making trekking adventures simple, safe and memorable.
                        </p>
                    </div>

                    <div class="col-md-6 text-md-end">
                        <h5>Contact</h5>
                        <p class="text-muted mb-2">
                        <i class="bi bi-envelope-fill me-2"></i>
                        support@trekway.com
                        </p>
                        <p class="text-muted">
                        <i class="bi bi-geo-alt-fill me-2"></i>
                        India
                        </p>
                    </div>

                </div>
                <hr>
                <div class="text-center text-muted">
                © 2026 TrekWay. All Rights Reserved.
                </div>
            </div>
        </footer>
    </div>
    
</template>

<style scoped>
.hero{
    padding:90px 0;
}

.hero-image{
    height:500px;
    width: 100%;
    object-fit: cover;
    border-radius: 20px;
}

.trek-card{
    border: none;
    border-radius: 20px;
    overflow: hidden;
    transition: .3s;
}

.trek-card img{
    height: 220px;
    object-fit: cover;
}

.trek-card:hover{
    transform: translateY(-8px);
}
.footer{
    background:#f8f9fa;
    padding:60px 0 20px;
    margin-top:70px;
}

.footer-link{
    color:#555;
    text-decoration:none;
    display:block;
    margin-bottom:10px;
    transition:.3s;
}

.footer-link:hover{
    color:var(--primary);
    padding-left:5px;
}

.hero{
    background:linear-gradient(to right,#f4f8f3,#e8f5e9);
}

.display-4{
    color:var(--primary);
}
</style>