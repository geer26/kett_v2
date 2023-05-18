<template>
    <div class="wo_main_container">
        
        <div
        class="counter_upper"
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">
         
          <div class="rep_label">
            <p>REPS</p>
          </div>

          <h1 :class="{ green_text : maxed, red_text : !maxed }">{{this.reps}}</h1>

          <div class="name_label">
            <p>{{ this.comp_name }}</p>
          </div>

        </div>

        <div
        class="info_upper"
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">

          <div class="blinker" v-if="this.workout && this.state == 'PREPARE'">
            <img src="../assets/img/attention.png" alt="ATTENTION" class="info_image">
          </div>

          <div class="blinker" v-if="this.workout && this.state == 'REST'">
            <img src="../assets/img/pause.png" alt="ATTENTION" class="info_image">
          </div>

          <div class="blinker" v-if="this.workout && this.state == 'WORK'">
            <img src="../assets/img/work.png" alt="ATTENTION" class="info_image">
          </div>

          <div class="blinker" v-if="this.workout && this.state == 'FINISHED'">
            <img src="../assets/img/stop.png" alt="ATTENTION" class="info_image">
          </div>

        </div>

        <div class="labels"
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">

          <div class="time_label">
            <p>TIME</p>
          </div>

          <div class="workout_label">
            <p>{{ this.exercise }}</p>
          </div>

        </div>

        <div
        class="counter_lower" 
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">
        
          <Timer_component :time="this.time" class="time-counter" ref="timer"/>

        </div>

        <div
        class="info_lower weight_text_container"
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">
        
          <img src="../assets/img/arrow_up.png" alt="UPARROW" v-if="this.show_weight_adjust" class="pointered kb_image"
          @click="this.inc_weight"/>

          <p style="font-size: 7vh;">{{ this.weight }}</p>

          <img src="../assets/img/arrow_down.png" alt="DOWNARROW" v-if="this.show_weight_adjust" class="pointered kb_image"
          @click="this.dec_weight"/>

        </div>

    </div>
</template>

<script>

//import { socket } from '@/socket';
import Timer_component from './Timer_component.vue'

export default {
    name: 'Workout_component',

    components: {
      Timer_component,
    },

    created: function() {
      window.addEventListener('keypress',this.keypress);
    },

    props: {
        comp_name: String,
    },

    mounted(){

    },

    computed: {

    },

    methods: {

        keypress(e){
            if(e.which == 32){
            this.inc_reps()
            }
        },

        inc_reps(){
            if (this.countable_state.includes(this.state) && this.reps < this.max_reps){
                ++this.reps
                const d = {current_reps: this.reps}
                this.$emit("new_exercise", d)
                // TODO emit on socket!
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
                const d = {current_reps: this.reps}
                this.$emit("new_exercise", d)
                if (this.max_reps == this.reps && this.countable_state.includes(this.state)){
                    this.maxed = true
                } else {
                    this.maxed = false
                }
            }
        },

        inc_weight(){
          if (this.weight <= 46){
            this.weight += 2
            const d = {current_weight: this.weight}
            this.$emit("new_exercise", d)
          }
        },

        dec_weight(){
          if (this.weight >= 4){
            this.weight -= 2
            const d = {current_weight: this.weight}
            this.$emit("new_exercise", d)
          }
        },

        start_workout(data){
          this.workout = data.workout
          this.result.name = this.comp_name
          this.result.results = []
          this.next()
        },

        next(){
          this.index += 1
          if (this.index >= this.workout.length) {
            this.state = "FINISHED"
            this.show_results = true
            this.$emit("finished", this.result)
          } else {
            // TODO emit on socket
            this.do_exercise(this.index)
          }
        },

        do_exercise(index){
          let res = {}
          let exercise = this.workout[index]
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

          const d = {current_exercise: this.exercise, current_weight: this.weight, current_reps: this.reps, current_time: this.time}
          if (!this.countable_state.includes(this.state)){
            d.current_weight = 0
            d.current_reps = 0
          }
          this.$emit('new_exercise', d)

          // Indítjuk a visszaszámlálást
          this.timer = setInterval(() => {
            this.time -= 1
            this.$emit("new_exercise", {current_time: this.time})
              // Ha lejárt az időzítő
              if (this.time < 0) {
                //!!!SAVE RESULT!!!
                res.reps = this.reps
                // Időzítést töröljük - ez fontos!
                this.time = 0
                clearInterval(this.timer)
                if (this.state == "WORK"){this.result.results.push(res)}
                this.next();
              }
          }, 1000);
        },

    },

    data(){return{
        countable_state: ["WORK"],
        non_countable_state: ["PREPARE", "WAIT", "REST", "COOLDOWN", "FINISHED"],
        state: "",
        reps: 0,
        weight: 24,
        show_weight_adjust: true,
        max_reps: 32000,
        maxed: false,
        exercise: "---",
        time: 0,
        result: {},
        workout: {},
        index: -1,
        timer: null,
        show_results: false,
    }},

}

</script>

<style scoped>
.wo_main_container{
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;

    background-image: url("../assets/img/bg_logoless.jpg");
    z-index: 1;

    display: grid;

    grid-template-columns: 4fr 1fr;
    grid-template-rows: 5fr 1fr 5fr;

    justify-content: space-evenly;
    grid-template-areas:
        "counter_upper info_upper"
        "labels labels"
        "counter_lower info_lower";
}

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

.labels{
  grid-area: labels;
  position: relative;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin: 0;
  /*max-height: 10%;*/
}

.counter_lower{
    grid-area: counter_lower;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
    max-height: 100%;
    margin: 0;
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
    margin: 0;
}

.rep_label{
  color: var(--yellow);
  position: absolute;
  top: 10%;
  left: 20%;
  padding: 0;
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
  left: 16%;
  padding: 0;
}

.time_label p{
  font-size: 3vw;
  text-shadow: 0px 0px 3px var(--yellow);
  padding: 0;
  margin: 0;
}

.workout_label{
  color: var(--red);
  position: relative;
  /*top: -25%;
  left: 50%;*/
  padding: 0;
  margin: 0;
}

.workout_label p {
  position: relative;
  font-size: 4vw;
  text-shadow: 0px 0px 3px var(--red);
  padding: 0;
  margin: 0;
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