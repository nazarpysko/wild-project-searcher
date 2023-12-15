import axios from 'axios'
import { Results } from '../types'

function generateResults() {
    const videos: string[] = [
        'https://www.youtube.com/watch?v=39jH02oBXIE',
        'https://www.youtube.com/watch?v=LTUUF_x5Ceg',
        'https://www.youtube.com/watch?v=ggFSisWer2c',
        'https://www.youtube.com/watch?v=k1PvPo8Qa9g',
        'https://www.youtube.com/watch?v=1IL4LgKSUzk'
    ]

    const length: number = Math.floor(Math.random() * 6)
    const res: Results = []
    for (let i = 0; i < length; i++) {
        const timestamps = [45, 158, 1005]
        res.push({
            video_id: videos[i].split('=')[1],
            title: videos[i],
            transcriptions: [{
                transcription: "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Possimus quod ipsa porro, consequuntur saepedignissimos corrupti blanditiis! Quod aliquam blanditiis quaerat corporis possimus neque dicta optio vero error, dolorum ex!",
                timestamp: timestamps[0]
            }]
        })
    }

    return res
}

export async function fetchResults(searchterm: string) {
    try {
        return await axios.put('http://localhost:5000/api/search', `query=${searchterm}`)
    } catch (err) { console.error(err) }
}
