<template>
  <Room_selector v-if="!this.connected"
    @connect_to_room="this.connect_to_room"
    @start_loading="this.startload"
    @stop_loading="this.endload"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <Workout_component v-if="this.ready_to_go" :comp_name="this.comp_name"/>

  <p v-if="this.suspended" class="color: var(--red);"> SUSPENDED </p>  
  <h1 class="station_name">{{ this.station_name.toUpperCase() }}</h1>
  <h1 class="competitor_name" @change="this.chage_comp_name">{{ this.comp_name }}</h1>

  <div class="readyicon_container">
    <img src="./assets/img/check.png" alt="ready_to_go"
    class="readyicon"
    v-if="!this.ready_to_go && this.connected && this.comp_name !== ''"
    @click="this.iamready">
  </div>
  

</template>

<script>

import Room_selector from './components/Room_selector_component.vue'
import Spinner_component from './components/Spinner_component.vue'
import Workout_component from './components/Workout_component.vue'
import { socket, state } from '@/socket'

export default {

  name: 'App',

  components: {
    Room_selector,
    Spinner_component,
    Workout_component
  },

  mounted(){

  socket.on("nameenter", (data) => {
    this.comp_name = data.name
    if (data.name == ""){
      this.ready_to_go = false
    }
  })

  socket.on('fetch_roomstatus', () => {
    socket.emit('provide_roomstatus', {
      room_name: this.room,
      super: false,
      mate_name: this.station_name,
      comp_name: this.comp_name,
      suspended: this.suspended,
      ready_to_go: this.ready_to_go,
    })
  })

  socket.on('toggle_suspend', () => {
    this.suspended = !this.suspended
  })

  socket.on("send_workout", (data) => {
    console.log(data)
    if(this.comp_name !== "" && !this.suspended && this.ready_to_go){
      this.workout = data
      //TODO start here!
    }
    return
  })

  },

  computed: {
    conn() {
      return state.connected
    }
  },

  methods: {
    connect_to_room(data){
      // TODO try connection
      this.room = data.room_name
      this.namespace = data.namespace
      this.station_name = data.station_name
      this.connected = true
      this.endload()
    },

    startload(){
      this.loading = true
    },

    endload(){
      this.loading = false
    },

    socket_send(data){
      data.namespace = this.namespace
      socket.emit(data.event, data)
    },

    iamready(){
      this.ready_to_go = true
      let data = {
        ready_to_go: true,
      }
      socket.emit("ready_to_go", data)
    },

    chage_comp_name(){
      if(this.comp_name == ""){
        this.ready_to_go = false
        let data = {
        ready_to_go: false,
      }
      socket.emit("ready_to_go", data)
      }
    },

  },

  data(){return{
    room: null,
    //connected: false,
    connected: false,
    namespace: "",
    loading: false,
    socket: socket,
    state: state,
    station_name: "",
    in_progress: false,
    comp_name: "",
    suspended: false,
    workout: {},
    ready_to_go: false,
    }
  },

}

</script>

<style>

.station_name{
  margin: 0;
  font-size: 10vh;
  color: var(--red);
}

.competitor_name{
  margin: 0;
  font-size: 20vh;
  color: var(--yellow);
}

.readyicon_container{
  position: relative;
  height: 10%;
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.readyicon{
  position: relative;
  height: 90%;
  cursor: pointer;
  -webkit-filter: drop-shadow(5px 5px 5px #222);
  filter: drop-shadow(5px 5px 5px #222);
  transition: .3s ease;
}

.readyicon:hover{
  height: 95%;
}

</style>