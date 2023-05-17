<template>
  <Room_selector v-if="!this.connected"
    @connect_to_room="this.connect_to_room"
    @start_loading="this.startload"
    @stop_loading="this.endload"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <Result_component v-if="this.show_results" @close_results="this.close_results" :result="this.result"/>

  <Workout_component
    v-if="this.ready_to_go"
    :comp_name="this.comp_name"
    ref="wo"
    @finished="this.finished"
    @new_exercise="this.new_exercise"/>

  <p v-if="this.suspended" class="color: var(--red);"> SUSPENDED </p>  
  <h1 class="station_name" v-if="!this.show_results">{{ this.station_name.toUpperCase() }}</h1>
  <h1 class="competitor_name" v-if="!this.show_results" @change="this.chage_comp_name">{{ this.comp_name }}</h1>

  <div class="readyicon_container" v-if="!this.show_results">
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
import Result_component from './components/Result_component.vue'
import { socket, state } from '@/socket'

export default {

  name: 'App',

  components: {
    Room_selector,
    Spinner_component,
    Workout_component,
    Result_component,
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
      current_exercise: "-",
      current_weight: 0,
      current_reps: 0,
    })
  })

  socket.on('toggle_suspend', () => {
    this.suspended = !this.suspended
  })

  socket.on("send_workout", (data) => {
    if(this.comp_name !== "" && !this.suspended && this.ready_to_go){
      this.workout = data
      this.$refs.wo.start_workout(data)
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

    finished(result){
      this.ready_to_go = false
      this.result = result
      this.show_results = true
      //TODO send finish trigger and the results
    },

    close_results(){
      this.show_results = false
      this.result = {}
      //this._init()
    },

    new_exercise(data){
      socket.emit("new_exercise", data)
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
    comp_name: "",
    suspended: false,
    result: {},
    workout: {},
    ready_to_go: false,
    show_results: false,
    current_exercise: "-",
    current_weight: 0,
    current_reps: 0,
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
  width: 30%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.readyicon{
  position: relative;
  height: 60%;
  cursor: pointer;
  -webkit-filter: drop-shadow(5px 5px 5px #222);
  filter: drop-shadow(5px 5px 5px #222);
  transition: .3s ease;
}

.readyicon:hover{
  height: 63%;
}

</style>