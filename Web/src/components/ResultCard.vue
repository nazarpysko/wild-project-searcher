<script setup lang="ts">
defineProps(['result'])

function getLink(videoURL: string, timestamp: string) {
    const time: string[] = timestamp.split(':')
    let ytTimestamp: string
    if (time.length === 3) {
        ytTimestamp = `${time[0]}h${time[1]}m${time[2]}s`
    } else {
        ytTimestamp = `${time[0]}m${time[1]}s`
    }

    return `${videoURL}#t=${ytTimestamp}`
}
</script>

<template>
    <div class="container">
        <div class="img-container">
            <a :href="result.videoURL" target="_BLANK">
                <img :src="`https://img.youtube.com/vi/${result.id}/sddefault.jpg`" alt="Youtube Thumbnail" />
            </a>
        </div>

        <div class="card">
            <hgroup>
                <h3>The Wild Project #246 ft Vicente Garrido | Hay psicópatas entre nosotros, Así piensa un asesino</h3>
                <a :href="result.videoURL" target="_BLANK">{{ result.videoURL }}</a>
            </hgroup>
            <div class="timestamps" v-for="timestamp in result.timestamps" :key="result.id + timestamp">
                <a :href="getLink(result.videoURL, timestamp)" target="_BLANK">{{ timestamp }}</a>
                <span>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Possimus quod ipsa porro, consequuntur saepe
                    dignissimos corrupti blanditiis! Quod aliquam blanditiis quaerat corporis possimus neque dicta optio
                    vero error, dolorum ex!
                </span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    gap: 1.5em;
}

.img-container {
    border-radius: 8px;
    flex-shrink: 0;
    width: 360px;
    height: 200px;
    overflow: hidden;
}

img {
    height: 100%;
    width: 100%;
    object-fit: cover;
    transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
}

img:hover {
    transform: scale(1.1);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.card {
    width: 100%;
    padding: 1.5em;

    border: 1px solid #d2d6dc;
    border-radius: 8px;

    text-align: left;
}

hgroup * {
    margin: 0;
}

hgroup {
    margin-bottom: 1em;
}

.timestamps {
    display: inline-flex;
    gap: 1em;
}

.timestamps:not(:last-child) {
    margin-bottom: 0.5em;
}
</style>
