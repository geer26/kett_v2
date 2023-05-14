<template>
    <div class="wo_main_container">
        
        <div
        class="counter_upper"
        @click="this.inc_reps"
        @contextmenu.prevent="this.dec_reps">
         COUNTER UPPER
        </div>

        <div></div>

        <div></div>

    </div>
</template>

<script>

export default {
    name: 'Workout_component',

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

    },

    data(){return{
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
        time: 0,
        workout: null,
        result: {},
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