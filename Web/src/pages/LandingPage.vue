<script setup lang="ts">
import { store } from "../store"
import { useRouter } from 'vue-router'
import Searchbar from "../components/Searchbar.vue";
import Footer from "../components/Footer.vue";
const router = useRouter()

function handleSearch() {
    store.search()
    router.push('/search')
}

store.setSearchterm('')
</script>

<template>
    <section id="landing-section">
        <div class="img-container">
            <img class="logo" src="/wild-project-logo.png" alt="Wild Project logo" />
            <img src="/title.png" alt="Wild Project logo" />
        </div>

        <Searchbar class="landing-searchbar" :handleSearch="handleSearch"></Searchbar>

        <div class="buttons-container">
            <button @click="handleSearch" :disabled="store.searchterm === ''">Search</button>
            <button :disabled="store.searchterm === ''">I'm feeling lucky</button>
        </div>
        <Footer></Footer>
    </section>
</template>

<style scoped>
#landing-section {
    justify-content: center;
    height: 100vh;
}

.img-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-bottom: 1.5em;
    align-content: center;
}

img {
    overflow: auto;
    flex-grow: 0;
    object-fit: scale-down;
}

.landing-searchbar {
    width: 570px;
}

.buttons-container {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin: 1em;
}

@media only screen and (max-width: 767px) {
    .landing-searchbar {
        width: 100%;
    }
}
</style>
