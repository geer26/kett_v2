import { reactive } from "vue"
import { io } from "socket.io-client"

export const state = reactive({
  connected: false,
  roomevents: [],
  barEvents: []
})


// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.NODE_ENV === "production" ? undefined : window.location.hostname + ":5000"
//const URL = window.location.hostname + ":5000"

export const socket = io(URL, {
    autoConnect: true
  })

socket.on("connect", () => {
  state.connected = true
})

socket.on("error_message", data => {
  return data
})

socket.on("disconnect", () => {
  state.connected = false
})

socket.on("createroom", (...args) => {
  state.roomevents.push(args)
})

socket.on("bar", (...args) => {
  state.barEvents.push(args)
})