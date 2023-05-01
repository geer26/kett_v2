<template>
    <div class="modal_background">
        
        <div class="modal">
            
            <h1>ROOM</h1>
            
            <input type="text" v-model="this.room" class="room_input">
            
            <div class="room_selection">
                <a :class="{orang_selected : !this.new_room}" class="unselected_text">REJOIN</a>
                <label class="switch">
                    <input type="checkbox" v-model="this.new_room">
                    <span class="slider round"></span>
                </label>
                <a :class="{blu_selected : this.new_room}" class="unselected_text">CREATE</a>
            </div>

            <a class="btn blue_btn" v-if="this.new_room">CREATE NEW</a>
            <a class="btn orange_btn" v-if="!this.new_room">JOIN</a>
        
        </div>

    </div>
</template>

<script>

export default {

name: "Room_selector",
props: {
  
},

data(){return{
    room: "",
    new_room: true,
}}

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
    background-color: var(--dark_gray_70);
    border-radius: 5px;
    box-shadow: var(--yellow_shadow);
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.room_input {
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 500;
        width: 60%;
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
    color: var(--light_gray_70);
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

</style>