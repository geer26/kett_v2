<template>
  <Room_selector v-if="!this.connected"
    @connect_to_room="this.connect_to_room"
    @start_loading="this.startload"
    @stop_loading="this.endload"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <Workout_component v-if="this.in_progress"/>

  
  <h1 class="station_name">{{ this.station_name.toUpperCase() }}</h1>
  <h1 class="competitor_name">{{ this.comp_name }}</h1>
  

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

  socket.on("nameenter", (data) => this.comp_name = data.name)

  },

  computed: {
    conn() {
      return state.connected
    }
  },

  methods: {
    connect_to_room(data){
      // TODO try connection
      console.log(data)
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
    }
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

</style>