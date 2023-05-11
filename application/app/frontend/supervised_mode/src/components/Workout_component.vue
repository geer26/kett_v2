<template>
    <div class="wo_main_container">

    </div>
</template>

<script>

export default {
    name: 'Workout_component',

}

</script>

<style scoped>
.wo_main_container{
    position: absolute;
    background-image: url("../assets/img/bg_logoless.jpg"); 

    display: grid;

    grid-template-columns: 4fr 1fr;
    grid-template-rows: 5fr 1fr 5fr;

    justify-content: space-evenly;
    grid-template-areas:
        "counter_upper info_upper"
        "labels labels"
        "counter_lower info_lower";
}

</style>