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
        const nTimestamps = Math.floor(Math.random() * 4) + 1

        res.push({
            id: videos[i].split('=')[1],
            videoURL: videos[i],
            timestamps: ['00:45', '10:15', '25:02'].slice(0, nTimestamps)
        })
    }

    return res
}

export function fetchResults(searchterm: string) {
    // TODO: Make real fetch

    console.log(`Searching ${searchterm} in Elasticsearch...`)
    return new Promise((resolve) => {
        setTimeout(() => {
            const data = generateResults()
            resolve(data)
        }, 1000)
    })
}
