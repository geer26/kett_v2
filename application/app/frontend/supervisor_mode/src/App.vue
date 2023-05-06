<template>

  <Room_selector v-if="!this.connected" @connect_to_room="this.connect_to_room"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <div class="main_container">

    <div class="table_label">

      <img v-if="this.conn" src="./assets/img/connected.png" alt="" class="connectionimage">
      <img v-if="!this.conn" src="./assets/img/disconnected.png" alt="" class="connectionimage">
      STATION TABLE
      <ConnectionManager/>

    </div>

    <div class="station_table_container glassmorphism_gray">

        
    </div>

    <div class="control_panel_container">

      <div class="select_workout_container">
        <select name="select" id="" class="select_box">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
      </select>
      </div>

      <div class="start_button_container"><a class="btn green_btn" style="width:50%;">START</a></div>

      <div class="timer_container"><p class="red_text">TIME</p></div>

    </div>
  </div>

</template>

<script>

import Room_selector from './components/Room_selector_component.vue'
import Spinner_component from "./components/Spinner_component.vue"
//import ConnectionState from './components/Connectionstate.vue'
import ConnectionManager from './components/ConnectionManager.vue'
import { socket, state } from "@/socket"

export default {

  name: 'App',

  components: {
    Room_selector,
    Spinner_component,
    //ConnectionState,
    ConnectionManager,
  },

  computed: {
    conn() {
      return state.connected
    }
  },

  methods: {
    connect_to_room(data){
      // TODO try connection
      data
      console.log("DATA AT CONNECTION: " + data.new_room + " - " + data.room_name)
      this.connected = true
    }
  },

  data(){return{
    room: null,
    connected: false,
    loading: false,
    socket: socket,
    state: state
  }}

}
</script>

<style>

.main_container{
  position: relative;
  height: 100%;
  width: 99%;
  display:flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;

  overflow: hidden;
}

.spinner{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.station_table_container{
  position: relative;
  height: 75%;
  width: 99%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  overflow: auto;
}

.table_label{
  position: relative;
  height: 15%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.control_panel_container{
  grid-area: control_panel;
  height: 10%;
  width: 100%;
  position: relative;
  padding-left: 20px;
  padding-right: 20px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr;
  justify-content: space-evenly;
  grid-template-areas:
        "select_workout start_button timer";
}

.select_workout_container{
  grid-area: select_workout;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}


.select_box{
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 500;
  width: 50%;
  max-height: 6vh;
  background-color: var(--light_gray);
  color: var(--dark_gray);
  text-align: center;
  margin: 10px;
  padding: 5px;
}

.start_button_container{
  grid_area: start_button;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.timer_container{
  grid-area: timer;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.connectionimage {
  max-height: 30%;
}

</style>
