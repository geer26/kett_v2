<template>

    <div class="sidebar glassmorphism_gray">

        <div class="switch_holder">
            <p class="sidebar_label">Name</p>
            <input type="text" class="competitor_name_input" @keyup="this.change_id" v-model="this.id">
        </div>

        <div class="switch_holder">
            <p class="sidebar_label">Select workout</p>

            <select v-model="this.workout" class="competitor_name_input" @change="this.select_workout">
                <option value="" selected=""></option>
                <option v-for="wo in this.workout_list" v-bind:value="{name: wo.name, workout: wo.workout}" :key="wo.name">{{ wo.name }}</option>
            </select>

        </div>

        <div class="switch_holder">

            <p class="sidebar_label"
            v-if="this.workout.name == 'CUSTOM'">
                Workout time
            </p>
            <input type="number" class="competitor_name_input" v-model="this.workout.workout[1].time" 
            v-if="this.workout.name == 'CUSTOM'"
            @keyup="this.select_timed">

            <p class="sidebar_label"
            v-if="['3 MINUTES', '5 MINUTES', '10 MINUTES', '30 MINUTES', 'CUSTOM'].includes(this.workout.name)">
            Exercise name
            </p>
            <input type="text" class="competitor_name_input" v-model="this.workout.workout[1].exercise"
            v-if="['3 MINUTES', '5 MINUTES', '10 MINUTES', '30 MINUTES', 'CUSTOM'].includes(this.workout.name)"
            @keyup="this.select_timed">

        </div>

        <a
        class="btn green_btn btn_base"
        v-if="this.ready_to_go && this.state == 'PREPARE'"
        @click="this.start_workout">
            <p>start</p>
        </a>

        <a
        v-if="['WAIT', 'WORK', 'REST', 'COOLDOWN'].includes(this.state)"
        class="btn red_btn btn_base"
        @click="this.$emit('halt_workout')">
            <p>stop</p>
        </a>

    </div>

</template>

<script>

import { workouts } from '../workouts/built_in'

export default {

  name: "Sidebar_component",
  props: {
    state: String,
  },

  mounted(){
    this.workout_list = workouts
    this.mode = "Single"
  },

  methods:{

    change_id(){
        if(this.id != ""){
            this.id_selected = true
        } else{
            this.id_selected = false
        }
        this.check_if_ready()
    },

    select_workout(){
        this.workout_selected = true
        if(!['3 MINUTES', '5 MINUTES', '10 MINUTES', '30 MINUTES', 'CUSTOM'].includes(this.workout.name)){
            this.timed_selected = true
        }
        this.check_if_ready()
    },

    select_timed(){
        if(['3 MINUTES', '5 MINUTES', '10 MINUTES', '30 MINUTES', 'CUSTOM'].includes(this.workout.name) && 
        this.workout.workout[1].exercise != "" && this.workout.workout[1].time > 0){
            this.timed_selected = true
        }else{
            this.timed_selected = false
        }
        this.check_if_ready()
    },

    check_if_ready(){
        if (this.id_selected && this.workout_selected && this.timed_selected) {
            this.ready_to_go = true
        } else{
            this.ready_to_go = false
        }
    },

    start_workout(){
        this.$emit('start_workout', {comp_name: this.id, workout: this.workout})
    },

    stop_workout(){
        
    },

  },

  data(){
    return{

        mode: "Single",
        id: "",
        custom_workout_time: 0,

        workout: {},
        workout_list: [],
        id_selected: false,
        workout_selected: false,
        timed_selected: false,
        ready_to_go: false,
    }

    }
}
</script>

<style scoped>
    .sidebar {
        position: absolute;
        top: 0;
        left: -14%;
        height: 100vh;
        width: 15%;
        /*backdrop-filter: blur(2px);
        background-image: linear-gradient(to right, rgba(0,0,0,0),rgba(0,0,0,0),
        rgba(0,0,0,0),rgba(0,0,0,0),rgba(0,0,0,0),rgba(0,0,0,0),rgba(0,0,0,0),var(--yellow_40));*/
        transition: .4s ease;
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        padding-top: 20px;
    }

    .sidebar:hover {
        left:0;
    }

    .btn_base {
        width: 70%;
    }

    .switch_holder{
        width: 70%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    .sidebar_label{
        color: var(--yellow);
        font-size: 1vw;
    }

    .competitor_name_input {
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 500;
        width: 100%;
        max-height: 6vh;
        background-color: var(--light_gray);
        color: var(--dark_gray);
        text-align: center;
        margin: 10px;
        padding: 5px;
    }
    
</style>