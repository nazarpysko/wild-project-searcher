<script setup lang="ts">
import { store } from '../store';
import { useRoute } from 'vue-router'

const route = useRoute()

</script>

<template>
    <footer v-if="route.path === '/' || !store.isLoading">
        <span>Made with ❤️ by </span> <strong>Gabriella & Co</strong>
    </footer>
</template>

<style scoped>
footer {
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 0.75em;
}
</style>
