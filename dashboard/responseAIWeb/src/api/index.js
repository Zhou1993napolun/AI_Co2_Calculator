import request from "./request";

export const getDataBySelect = (data)=>request.post('/responseai/getData',data)
