<template>


    <Construction_component v-if="this.mode == 'Supervised'"/>

    <Sidebar_component
      @start_workout="this.start_workout"
      @halt_workout="this.halt_workout"
      :state="this.state"
      />

    <Result_component v-if="this.show_results" @close_results="this.close_results" :result="this.result"/>

    <div
      class="counter_upper" 
      @click="this.inc_reps"
      @contextmenu.prevent="this.dec_reps"
      >

      <div class="rep_label">
        <p>REPS</p>
      </div>

      <h1 :class="{ green_text : maxed, red_text : !maxed }">{{this.reps}}</h1>

      <div class="name_label">
        <p>{{ this.name }}</p>
      </div>

    </div>

    <div
      class="info_upper"
      @click="this.inc_reps"
      @contextmenu.prevent="this.dec_reps">

      <div class="blinker" v-if="this.workout && this.state == 'PREPARE'">
        <img src="./assets/img/attention.png" alt="ATTENTION" class="info_image">
      </div>

      <div class="blinker" v-if="this.workout && this.state == 'REST'">
        <img src="./assets/img/pause.png" alt="ATTENTION" class="info_image">
      </div>

      <div class="blinker" v-if="this.workout && this.state == 'WORK'">
        <img src="./assets/img/work.png" alt="ATTENTION" class="info_image">
      </div>

      <div class="blinker" v-if="this.workout && this.state == 'FINISHED'">
        <img src="./assets/img/stop.png" alt="ATTENTION" class="info_image">
      </div>
      
    </div>

    <div
      class="counter_lower" 
      @click="this.inc_reps"
      @contextmenu.prevent="this.dec_reps">

      <div class="time_label">
        <p>TIME</p>
      </div>

      <div class="workout_label">
        <p>{{ this.exercise }}</p>
      </div>

      <Timer_component :time="this.time" class="time-counter" ref="timer"/>

    </div>

    <div
      class="info_lower weight_text_container"
      @click="this.inc_reps"
      @contextmenu.prevent="this.dec_reps">

        <img src="./assets/img/arrow_up.png" alt="UPARROW" v-if="this.show_weight_adjust" class="pointered kb_image"
        @click="this.inc_weight"/>
        <p>
        {{ this.weight }}
        </p>
        <img src="./assets/img/arrow_down.png" alt="DOWNARROW" v-if="this.show_weight_adjust" class="pointered kb_image"
        @click="this.dec_weight"/>
    
    </div>


</template>

<script>

import Sidebar_component from './components/Sidebar_component.vue'
import Timer_component from './components/Timer_component.vue'
import Result_component from './components/Result_component.vue'
import Construction_component from './components/Construction_component.vue'

export default {
  name: 'App',
  components: {
    Sidebar_component,
    Timer_component,
    Result_component,
    Construction_component,
  },

  mounted(){
  },

  computed(){
  },

  methods:{

    _init(){
      this.mode = "Single"
      this.state = "PREPARE"
      this.reps = 0
      this.weight = 24
      this.show_weight_adjust = true
      this.max_reps = 32000
      this.maxed = false
      this.exercise = "---"
      this.time = "-:-:-"
      this.workout = null
      this.name = ""
      this.result = {}
      this.index = -1
      this.timer = null
    },

    resulinit(){
      this.mode = "Single"
      this.state = "PREPARE"
      this.reps = 0
      this.weight = 24
      this.show_weight_adjust = true
      this.max_reps = 32000
      this.maxed = false
      this.exercise = "---"
      this.time = "-:-:-"
      this.workout = null
      this.index = -1
      this.timer = null
    },

    select_mode(mode){
      this.mode = mode
    },

    close_results(){
      this.show_results = false
      this.result = {}
      this.name = ""
      this._init()
    },

    inc_reps(){
      if (this.countable_state.includes(this.state) && this.reps < this.max_reps){
        ++this.reps
        if (this.max_reps == this.reps && this.countable_state.includes(this.state)){
          this.maxed = true
        } else {
          this.maxed = false
        }
      }
    },

    dec_reps(){
      if (this.countable_state.includes(this.state) && this.reps > 0){
        --this.reps
        if (this.max_reps == this.reps && this.countable_state.includes(this.state)){
          this.maxed = true
        } else {
          this.maxed = false
        }
      }
    },

    start_workout(data){
      this.name = data.comp_name
      this.workout = data.workout
      this.result.name = this.name
      this.result.results = []
      this.next()
    },

    next(){
      this.index += 1
      if (this.index >= this.workout.workout.length) {
        // Ha nincs több elem a tömbben, akkor vége
        //DO SOMETHING!
        this.state = "FINISHED"
        this.show_results = true
        this.resulinit()
      } else {
        this.do_exercise(this.index)
      }
    },

    halt_workout(){
      this.time = 0
      clearInterval(this.timer)
      this.state = "FINISHED"
      this._init()
    },

    finish_countdown(){
      this.state = "FINISHED"
      this._init()
    },

    do_exercise(index){
      // Actual element
      let res = {}
      let exercise = this.workout.workout[index]
      this.state = exercise.type
      this.max_reps = exercise.max_reps
      this.exercise = exercise.exercise
      res.exercise = exercise.exercise
      this.reps = 0
      this.maxed = false
      if (exercise.type == "WORK" || this.state == "FINISHED" || this.state == "COOLDOWN"){
        this.show_weight_adjust = false
      } else {
        this.show_weight_adjust = true
      }

      // Hátralévő idő mutatása
      this.time = exercise.time
      res.time = this.time
      res.weight = this.weight

      // Indítjuk a visszaszámlálást
      this.timer = setInterval(() => {
        this.time -= 1
          // Ha lejárt az időzítő
          if (this.time < 0) {
            //!!!SAVE RESULT!!!
            res.reps = this.reps
            // Időzítést töröljük - ez fontos!
            this.time = "-:-:-"
            clearInterval(this.timer)
            if (this.state == "WORK"){this.result.results.push(res)}
            this.next();
          }
      }, 1000);
    },

    inc_weight(){
      if (this.weight <= 44){
        this.weight += 4
      }
    },

    dec_weight(){
      if (this.weight >= 12){
        this.weight -= 4
      }
    },

  },

  data() {return{
    mode: "Single",
    countable_state: ["WORK"],
    non_countable_state: ["PREPARE", "WAIT", "REST", "COOLDOWN", "FINISHED"],
    state: "PREPARE",
    reps: 0,
    weight: 24,
    show_weight_adjust: true,
    max_reps: 32000,
    maxed: false,
    exercise: "---",
    time: "-:-:-",
    workout: null,
    result: {},
    name: "",
    index: -1,
    timer: null,
    show_results: false,
  }},

}

</script>

<style scoped>
.counter_upper{
    grid-area: counter_upper;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction:column;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.counter_upper h1 {
  font-size: 17vw;
  margin: 0;
  margin-left: 20%;
  padding: 0;
  text-shadow: 0px 0px 3px var(--red);
}

.info_upper{
    grid-area: info_upper;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
}

.info_image{
    width: 50%;
}

.counter_lower{
    grid-area: counter_lower;
    text-align: center;
    position: relative;
    top: -5%;
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
    max-height: 100%;
}

.time-counter{
  position: absolute;
  color: var(--red);
  margin-left: 20%;
  text-shadow: 0px 0px 3px var(--red);
}

.info_lower{
    grid-area: info_lower;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
}

.rep_label{
  color: var(--yellow);
  position: absolute;
  top: 10%;
  left: 20%;
  padding: 10px;
}

.rep_label p{
  font-size: 3vw;
  text-shadow: 0px 0px 3px var(--yellow);
}

.name_label{
  color: var(--yellow);
  position: absolute;
  top: 10%;
  right: 0;
  padding: 10px;
}

.name_label p{
  font-size: 3vw;
  text-shadow: 0px 0px 3px var(--yellow);
}

.time_label{
  color: var(--yellow);
  position: absolute;
  top: 0;
  left: 20%;
  padding: 10px;
}

.time_label p{
  font-size: 3vw;
  text-shadow: 0px 0px 3px var(--yellow);
}

.workout_label{
  color: var(--red);
  position: absolute;
  top: -25%;
  left: 50%;
  padding: 10px;
}

.workout_label p {
  font-size: 4vw;
  text-shadow: 0px 0px 3px var(--red);
}


.green_text {
  color: var(--green);
  text-shadow: 0px 0px 3px var(--green);
}

.red_text {
  color: var(--red);
  text-shadow: 0px 0px 3px var(--red);
}

.kb_weight_container{
  position: relative;
  width: 70%;
  max-height: 100%;
}

.weight_text_container{
  position: relative;
  max-width: 100%;
  text-align: center;
}

.weight_text_container p{
  color: var(--yellow);
  text-shadow: 0px 0px 3px var(--yellow);
  font-size: 5rem;
  margin: 0; 
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.kb_image {
  max-width: 20%;
  -webkit-filter: drop-shadow(0px 0px 3px var(--yellow));
  filter: drop-shadow(0px 0px 3px var(--yellow));
}

.pointered {
  cursor: pointer;
}

</style>
