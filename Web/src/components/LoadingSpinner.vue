<script setup lang="ts">
</script>

<template>
    <div class="container">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
</template>

  
<style scoped>
.container {
    --uib-size: 47px;
    --uib-color: black;
    --uib-speed: 1s;
    --uib-dot-size: calc(var(--uib-size) * 0.18);
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: calc(var(--uib-size) * 0.5);
    width: var(--uib-size);
}

.dot {
    flex-shrink: 0;
    width: calc(var(--uib-size) * 0.17);
    height: calc(var(--uib-size) * 0.17);
    border-radius: 50%;
    background-color: var(--uib-color);
    transition: background-color 0.3s ease;
}

.dot:nth-child(1) {
    animation: jump var(--uib-speed) ease-in-out calc(var(--uib-speed) * -0.45) infinite;
}

.dot:nth-child(2) {
    animation: jump var(--uib-speed) ease-in-out calc(var(--uib-speed) * -0.3) infinite;
}

.dot:nth-child(3) {
    animation: jump var(--uib-speed) ease-in-out calc(var(--uib-speed) * -0.15) infinite;
}

.dot:nth-child(4) {
    animation: jump var(--uib-speed) ease-in-out infinite;
}

@keyframes jump {

    0%,
    100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-200%);
    }
}
</style>
  