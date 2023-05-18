<template>
    <div class="modal_background">
        
        <div class="modal glassmorphism_gray">

            <h4 style="margin: 5px;">Station name</h4>
            <input type="text" v-model="this.station" class="room_input" :disabled="!this.conn">
            <h4 style="margin: 5px;">Event name</h4>
            <input type="text" v-model="this.room" class="room_input" :disabled="!this.conn">
            
            <a class="btn" :class="{orange_btn : !this.conn, blue_btn : this.conn}" style="width:70%; justify-content: space-around;" @click="this.join_room">
              
              <img v-if="this.conn" src="../assets/img/connected.png" alt="" class="connectionimage">
              <img v-if="!this.conn" src="../assets/img/disconnected.png" alt="" class="connectionimage">

              <p v-if="this.conn">join</p>
              <p v-if="!this.conn">server down</p>
            </a>
        
        </div>

    </div>
</template>

<script>

import { socket, state  } from "@/socket"

export default {

name: "Room_selector",

mounted(){

  socket.on('room_confirmed', (data) => {
    if (data.status == 1){
      
      this.$emit('connect_to_room', {
        new_room: this.new_room,
        room_name: this.room,
        namespace: data.namespace,
        station_name: this.station,
        comp_name: "",
        suspended: false,
        ready_to_go: false,
        current_exercise: "-",
        current_weight: 0,
        current_reps: 0,
        current_time: "00:00:00",
      })
      
      return
    } else {
      alert(data.message)
    }

  })

  

},

props: {
  
},

computed: {
    conn() {
      return state.connected
    }
  },

methods: {

  join_room(){
    //this.$emit("start_loading")

    if(!this.conn){
      alert("Server is unavailable!")
      //this.$emit("stop_loading")
      return
    }
    if (this.station == ""){
      alert("Station name must be specified!")
      //this.$emit("stop_loading")
      return
    }
    if(this.room == "") {
      alert("Event name must be specified!")
      //this.$emit("stop_loading")
      return
    }

    socket.emit('joinroom', {
      room_name: this.room,
      super: false,
      station_name: this.station,
      comp_name: "",
      suspended: false,
      ready_to_go: false,
      current_exercise: "-",
      current_weight: 0,
      current_reps: 0,
    })
    return
  },

},

data(){return{
    station: "",
    room: "",
    state: state,
}},

}

</script>

<style scoped>
.modal_background{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    backdrop-filter: blur(5px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.modal{
    position: relative;
    max-width: 30%;
    padding: 10px;
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.room_input {
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 500;
        width: 70%;
        max-height: 6vh;
        background-color: var(--light_gray);
        color: var(--dark_gray);
        text-align: center;
        margin: 10px;
        padding: 5px;
    }


.room_selection{
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content:space-between;
    align-items: center;
    margin: 20px;
}

    /* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin-left: 10px;
  margin-right: 10px;
}


.unselected_text{
    color: var(--light_gray_40);
}

.orang_selected{
    color: var(--orang);
    font-weight: 600;
    font-size: 1rem;;
}


.blu_selected{
    color: var(--blu);
    font-weight: 600;
    font-size: 1rem;
}


/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--orang);
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: var(--light_gray);
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--blu);
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.room_label_container{
  position: relative;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.connectionimage {
  max-height: 3vh;
  margin: 0;
}

</style>