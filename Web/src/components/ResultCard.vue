<script setup lang="ts">
defineProps(['result'])
const youtubeURL = "https://www.youtube.com/watch?v="
function getLink(video_id: string, timestamp: number) {
    const time: string[] = getReadableTimestamp(timestamp).split(':')
    let ytTimestamp: string
    if (time.length === 3) {
        ytTimestamp = `${time[0]}h${time[1]}m${time[2]}s`
    } else {
        ytTimestamp = `${time[0]}m${time[1]}s`
    }

    return `${youtubeURL}${video_id}#t=${ytTimestamp}`
}

function getReadableTimestamp(timestamp: number): string {
    const hours = Math.floor(timestamp / 360)
    const minutes = Math.floor((timestamp - hours * 360) / 60)
    const seconds = Math.floor(timestamp - (hours * 360 + minutes * 60))
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}
</script>

<template>
    <div class="container">
        <div class="img-container">
            <a :href="youtubeURL + result.video_id" target="_BLANK">
                <img :src="`https://img.youtube.com/vi/${result.video_id}/sddefault.jpg`" alt="Youtube Thumbnail" />
            </a>
        </div>

        <div class="card">
            <hgroup>
                <h3>{{ result.title }}</h3>
                <a :href="youtubeURL + result.video_id" target="_BLANK">{{ youtubeURL + result.video_id }}</a>
            </hgroup>
            <div class="timestamps" v-for="transcription in result.transcriptions"
                :key="result.video_id + transcription.timestamp">
                <a :href="getLink(result.video_id, transcription.timestamp)" target="_BLANK">{{
                    getReadableTimestamp(transcription.timestamp) }}</a>
                <span>{{ transcription.transcription }}</span>
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
    display: flex;
    gap: 1em;
}

.timestamps:not(:last-child) {
    margin-bottom: 0.5em;
}

@media only screen and (min-width: 767px) {
    .img-container {
        width: 360px;
    }
}

@media only screen and (max-width: 767px) {
    .container {
        flex-direction: column;
        gap: 0;
    }

    .img-container {
        border-radius: 8px 8px 0px 0px;
    }

    .card {
        box-sizing: border-box;
        margin-top: -10px;
        background-color: white;
    }
}
</style>
