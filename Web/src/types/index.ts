export interface Transcription {
    transcription: string
    timestamp: number
}

export interface Result {
    video_id: string
    title: string
    transcriptions: Transcription[]
}

export type Results = Result[]
