<template>
  <Room_selector v-if="!this.connected"
    @connect_to_room="this.connect_to_room"
    @start_loading="this.startload"
    @stop_loading="this.endload"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <h1>SUPERVISED</h1>
</template>

<script>

import Room_selector from './components/Room_selector_component.vue'
import Spinner_component from './components/Spinner_component.vue'
import { socket, state } from '@/socket'

export default {

  name: 'App',
  components: {
    Room_selector,
    Spinner_component,
  },

  computed: {
    conn() {
      return state.connected
    }
  },

  methods: {
    connect_to_room(data){
      // TODO try connection
      //console.log("DATA AT CONNECTION: " + data.new_room + " - " + data.room_name)
      this.room = data.room_name
      this.connected = true
      this.endload()
    },

    startload(){
      this.loading = true
    },

    endload(){
      this.loading = false
    },
  },

  data(){return{
    room: null,
    connected: false,
    loading: false,
    socket: socket,
    state: state
    }
  },

}

</script>

<style>
</style>
