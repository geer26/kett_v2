<template>

  <Room_selector v-if="!this.connected"
    @connect_to_room="this.connect_to_room"
    @start_loading="this.startload"
    @raise_alert="this.raise_alert"/>

  <Spinner_component v-if="this.loading" class="spinner"/>

  <Results_component v-if="this.show_results" :result="this.all_results" @close_results="this.close_results"
  @raise_alert="this.raise_alert"/>

  <v-snackbar
    v-model="this.dialog"
    :timeout="5000"
    width="auto"
    >
    {{ this.dialog_text }}
    <v-icon
    @click="this.dialog = false"
    size="small"
    color="red-darken-2"
    icon="fas fa-xmark"
    >
    </v-icon>
  </v-snackbar>

  <div class="main_container">

    <div class="table_label">

      <img v-if="this.conn" src="./assets/img/connected.png" alt="" class="connectionimage">
      <img v-if="!this.conn" src="./assets/img/disconnected.png" alt="" class="connectionimage">
      <p style="font-size: 2rem; color: var(--red)">{{ this.room }}</p>

    </div>

    <div class="station_table_container glassmorphism_gray">

      <div class="station_entry"
      v-for="mate in this.supervised_list" 
      v-bind:value="{sid:mate.mate_sid, name:mate.mate_name}" 
      :key="mate.mate_sid"
      >

        <div class="station_icon_container">

          <v-switch
            v-if="!this.running_workout"
            v-model="mate.suspended"
            color="red-darken-2"
            @change="this.send_empty_name(mate)"
          ></v-switch>

          <v-icon
          v-if="mate.ready_to_go && !this.running_workout"
          color="green-darken-2"
          icon="fas fa-check"
          size="large"
          ></v-icon>

          <v-icon
          v-if="mate.finished"
          color="green-darken-2"
          icon="fas fa-square-check"
          size="large"
          ></v-icon>



      </div>

        <div class="station_name_container">

          <div class="mate_name">
            <p> {{ mate.mate_name }} </p>
          </div>

          <div class="comp_name">
            
            <input type="text"
            style="width: 80%"
            @keyup="send_name($event, mate.mate_sid)"
            v-model="mate.comp_name"
            v-if="!this.running_workout"
            />

            <p v-if="this.running_workout && mate.comp_name !== ''">{{ mate.comp_name }}</p>
          </div>

        </div>

        <div v-if="!mate.suspended" class="comp_name-container">

          <div class="comp_name-exercise_name">
            <p>{{ mate.current_exercise }}/{{ mate.current_weight }}kg</p>
          </div>

          <div class="comp_name-exercise_time">
            <p>{{ this.time_formatter(mate.current_time) }}</p>
          </div>

          <div class="comp_name-exercise_reps">
            <p>{{ mate.current_reps }}</p>
          </div>

        </div>

      </div>

    </div>

    <div class="control_panel_container">

      
      <div class="select_workout_container"
      v-if="!this.running_workout">
        <!--
        <select class="select_box" v-model="this.workout">
          <option v-for="wo in this.workouts" :value="{name: wo.name, workout: wo.workout}" :key="wo.name">{{ wo.name }}</option>
        </select>
        -->

        <p
          @click="this.show_wo_selector = true"
          style="cursor: pointer; color: var(--yellow); margin: 0; padding: 0;">
          {{ this.workout == null ? "SELECT WORKOUT" : this.workout.name }}
        </p>

      </div>
      
      <v-dialog
        v-model="this.show_wo_selector"
        transition="dialog-bottom-transition"
        scrollable
        width="40%"
      >
        <v-card
        v-for="wo in this.workouts" :value="{name: wo.name, workout: wo.workout}" :key="wo.name"
        variant="outlined"
        style="margin: 5px; display: flex; flex-direction: row; justify-content: space-around; align-items: center; margin-left: 20px; "
        >
          <div style="width: 40%; text-align: left;">
            <p style="margin: 10px; color: var(--yellow);">{{ wo.name }}</p>
          </div>

          <div style="width: 40%;">
            <input
              list="built_in_exercises"
              style="background-color: var(--dark_gray); color: var(--yellow); padding: 5px; max-height: 70%; max-width: 100%;"
              type="text"
              v-if="wo.name.includes('MINUTE')"
              v-model="wo.workout[1].exercise"
              onkeyup="this.value = this.value.toUpperCase();"
            >
          </div>

          <datalist id="built_in_exercises">
            <option value="OAJ"></option>
            <option value="TAJ"></option>
            <option value="OALC"></option>
            <option value="TALC"></option>   
            <option value="OAS"></option>
            <option value="TAS"></option>
            <option value="OAHS"></option>
            <option value="TAHS"></option>          
          </datalist>

          <div style="width: 20%; display: flex; justify-content: flex-end; align-items: center; padding-right: 20px;">
            <v-icon
              @click="this.select_workout(wo)"
              color="green-darken-2"
              icon="fas fa-play"
              size="large"
            ></v-icon>
          </div>

        </v-card>
      </v-dialog>

      

      <div class="start_button_container">
        <v-btn
          prepend-icon="fas fa-play"
          v-ripple
          @click="this.startevent"
          color="green-darken-2"
          v-if="this.all_ready">
          start
        </v-btn>
      </div>

    </div>
  </div>

</template>

<script>

import Room_selector from './components/Room_selector_component.vue'
import Spinner_component from './components/Spinner_component.vue'
import Results_component from './components/Results_component.vue'
import { socket, state } from '@/socket'
import { workouts } from '@/workouts/built-in'

export default {

  name: 'App',

  components: {
    Room_selector,
    Spinner_component,
    Results_component,
  },

  mounted(){

    this.workouts = workouts

    socket.on("mate_connect", (data) => {
      data.ready_to_go = false
      data.suspended = false
      this.supervised_list.push(data)
      this.sort_superviseds()
    })

    socket.on("mate_disconnect", (data) => {
      this.supervised_list = this.supervised_list.filter( supervised => {
        return supervised.mate_sid !== data.mate_sid
      })
      this.sort_superviseds()
      if(this.supervised_list.length < 1){
        this.running_workout = false
      }
    })

    socket.on("provide_roomstatus", (data) => {
      this.supervised_list.push(data)
      this.sort_superviseds()
    })

    socket.on("platform_ready", data => {
      let mate = this.supervised_list.filter( supervised => {
        return supervised.mate_sid == data.sid
      })[0]
      mate.ready_to_go = data.ready_to_go
    })

    socket.on("accept_exercise_change", data => {
      let mate = this.supervised_list.filter( supervised => {
        return supervised.mate_sid == data.sid
      })[0]

      mate.current_exercise = data.current_exercise ? data.current_exercise : mate.current_exercise
      mate.current_weight = data.current_exercise ? data.current_weight : mate.current_weight
      mate.current_reps = data.current_reps ? data.current_reps : mate.current_reps
      mate.current_time = data.current_time ? data.current_time : mate.current_time

      if (data.current_exercise !== undefined) {
        mate.current_reps = 0
      }

      //this.running_workout = true
      
    })

    socket.on("accept_finishtrigger", data => {
      let mate = this.supervised_list.filter( supervised => {
        return supervised.mate_sid == data.sid
      })[0]

      data.mate_name = mate.mate_name

      mate.finished = true

      this.all_results.push(data)
      this.send_empty_name(mate)

      if(this.all_finished){
        this.show_results_init()
      }

    })

  },

  computed: {
    conn() {
      return state.connected
    },

    all_ready(){
      let cango = true

      if (this.supervised_list.length == 0 || this.running_workout){
        cango = false
      }

      this.supervised_list.forEach( supervised => {
        if ((supervised.comp_name == "" && !supervised.suspended)){
          cango = false
        }

        if(!supervised.ready_to_go && !supervised.suspended){
          cango = false
        }

      })

      if (this.workout == {}){
        cango = false
      }

      return cango
    },

    all_finished(){
      let finished = true
      this.supervised_list.forEach(supervised => {
        if(!supervised.finished && !supervised.suspended){
          finished = false
        }
      })
      return finished
    }

  },

  methods: {

    connect_to_room(data){
      // TODO try connection
      this.room = data.room_name
      this.namespace = data.namespace
      this.connected = true
      this.socket.emit("fetch_roomstatus", {room: this.room})
      this.endload()
    },

    sort_superviseds(){
      this.supervised_list.sort((a, b) => a.mate_name.localeCompare(b.mate_name))
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

    select_workout(wo){
      this.workout = wo
      this.workouts.forEach(w => {
        if(w.name !== wo.name && w.name.includes('MINUT')){
          w.workout[1].exercise = ""
        }
      })
      this.show_wo_selector = false
    },

    startevent(){
      if(!this.workout){
        this.raise_alert({message: 'Select a workout!'})
        return
      }
      socket.emit("send_workout", this.workout)
      this.running_workout = true
    },

    send_name(e, sid){
      let n = e.target.value
      let data = {
        event: "nameenter",
        data: {
          sid: sid,
          name: n
        }
      }
      this.socket_send(data)
      if(n == ""){
        let mate = this.supervised_list.filter( m => {return m.mate_sid == sid} )[0]
        mate.ready_to_go = false
      }
    },

    send_empty_name(mate){
      const sid = mate.mate_sid
      mate.comp_name = ""

      let data = {
        event: "nameenter",
        data:{
          sid: sid,
          name: ""
        }
      }
      this.socket_send(data)
      mate.ready_to_go = false
    },

    time_formatter(time){
      if (isNaN(time)){
        return "00:00:00"
      }
      let rem = time
      if (time == 0){
        return "00:00:00"
      }
      let hour = Math.floor(rem/3600) >= 9 ? Math.floor(rem/3600) : "0" + Math.floor(rem/3600) 
      if (Math.floor(rem/3600) == 9) {hour = "09"}
      rem = rem%3600
      let min = Math.floor(rem/60) >=9 ? Math.floor(rem/60) : "0" + Math.floor(rem/60)
      if (Math.floor(rem/60) == 9) {min = "09"}
      rem = rem%60
      let sec = rem >=9 ? rem : "0" + rem
      if (rem == 9) {sec = "09"}
      return `${hour}:${min}:${sec}`
    },

    show_results_init(){
      this.supervised_list.forEach(supervised => {
        supervised.comp_name = ""
        supervised.finished = false
        supervised.suspended = false
        supervised.ready_to_go = false
        supervised.current_exercise = "-"
        supervised.current_reps = 0
        supervised.current_time = 0
        supervised.current_weight = 0
      })
      this.running_workout = false
      this.show_results = true
    },

    close_results(){
      this.show_results = false
    },

    raise_alert(data){
      this.dialog = true
      this.dialog_text = data.message
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
    workouts: [],
    workout: null,
    show_wo_selector: false,
    supervised_list: [],
    running_workout: false,
    all_results: [],
    show_results: false,
    dialog: false,
    dialog_text: "",
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
  height: 100%;
  width: 99%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  overflow: auto;
  padding: 10px;
}

.station_entry{
  position: relative;
  width: 99%;
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.station_name_container{
  position: relative;
  width: 40%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.station_name_container p{
  font-size: .8rem;
  text-transform: uppercase;
}

.mate_name{
  width: 30%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.mate_name p{
  /*font-size: 120%;*/
  color: var(--yellow);
  font-weight: 600;
  margin: 0;
  padding: 0;
}

.comp_name{
  position: relative;
  width: 70%;
  max-height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.comp_name p{
  font-size: 100%;
  color: var(--yellow);
  font-weight: 600;
  margin: 0;
  padding: 0;
}

.comp_name-container{
  position: relative;
  width: 60%;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.comp_name-exercise_name{
  position: relative;
  width: 60%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.comp_name-exercise_name p{
  font-size: 120%;
  color: var(--yellow);
  font-weight: 600;
  margin: 0;
  padding: 0;
}

.comp_name-exercise_reps{
  position: relative;
  width: 10%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.comp_name-exercise_reps p{
  font-size: 120%;
  color: var(--yellow);
  font-weight: 600;
  margin: 0;
  padding: 0;
}

.comp_name-exercise_time{
  position: relative;
  width: 30%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.comp_name-exercise_time{
  font-size: 120%;
  color: var(--red);
  font-weight: 600;
  margin: 0;
  padding: 0;
}

.station_entry input{
  font-size: 100%;
  font-weight: 500;
  /*width: 15%;*/
  max-height: 5vh;
  width: 15%;
  background-color: var(--dark_gray);
  color: var(--yellow);
  text-align: center;
  margin: 10px;
  padding: 5px;
  background-color:  rgba( 228,226,226, 0.2); 
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border-radius: 5px;
  border: 1px solid rgba( 228,226,226, 0.2); 
}

.station_entry input:disabled{
  background-color: var(--dark_gray);
}

.station_icon_container{
  position: relative;
  width: 10%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
}

.finish_label{
  margin: 0 !important;
  font-size: 80% !important;
  color: var(--green);
}

.checkicon{
  position:relative;
  height: 50%;

}

.station_icon_container p{
  position: relative;
  margin: 0;
  font-size: 2rem;
  display: inline-block;
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

.wo_selector_container{
  border: 1px solid var(--light_gray);
}

.wo_selector_item{
  margin: 5px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: 20px;
}

</style>
