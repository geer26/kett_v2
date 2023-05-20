<template>

    <div class="result_container glassmorphism_gray">

        <div class="name_container">
            <h1>{{ this.result.name }}</h1>
        </div>
        
        <div class="results">
            <table>
                <tr>
                    <th>EXERCISE</th>
                    <th>TIME ELAPSED</th>
                    <th>WORKING WEIGHT</th>
                    <th>REPS</th>
                    <th>SCORE</th>
                </tr>
                <tr v-for="res in this.result.results" v-bind:value="{name: res.exercise}" :key="res.exercise">
                    <td>{{ res.exercise }}</td>
                    <td>{{ res.time }}</td>
                    <td>{{ res.weight }}</td>
                    <td>{{ res.reps }}</td>
                    <td>{{ !isNaN(res.weight) && !isNaN(res.reps) ? (res.weight/8)*res.reps : "0" }}</td>
                </tr>
                <tr>
                    <td>ALL SCORE</td>
                    <td>{{ this.all_score }}</td>
                </tr>
            </table>
        </div>

        <div class="buttons-container">
            <a 
            class="btn red_btn"
            @click="this.$emit('close_results')"
            >
                <p>close</p>
            </a>

            <a class="btn green_btn" @click="this.save_result">
                <p>save result</p>
            </a>
        </div>

    </div>

</template>

<script>
    export default {
        name: "Result_component",

        props: {
            result: {},
        },

        computed: {
            all_score(){
                let all_score = 0
                this.result.results.forEach(res => {
                    let w = Number(res.weight)
                    let r = Number(res.reps)
                    let score = !isNaN(w) && !isNaN(r) ? (w/8)*r : "No score available!"
                    if (!isNaN(score)){
                        all_score += score
                    }
                })
                return all_score
            },
        },
            

        mounted(){
            //this.save_result()
        },

        methods: {
            save_result(){
                let all_score = 0
                let csv_header = 'exercise, time elapsed, working weight, reps, score\n'
                this.result.results.forEach( res => {
                    let w = Number(res.weight)
                    let r = Number(res.reps)
                    let score = !isNaN(w) && !isNaN(r) ? (w/8)*r : "No score available!"
                    if (!isNaN(score)){
                        all_score += score
                    }
                    const row = `${res.exercise},${res.time},${res.weight},${res.reps},${score}\n`
                    csv_header += row
                })
                let main = `NAME, ${this.result.name}, SCORE, ${all_score}\n`
                csv_header = main + csv_header
                
                let filename = `${this.result.name}.csv`
                let element = document.createElement('a')
                element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_header))
                element.setAttribute('download', filename);
                element.style.display = 'none'
                document.body.appendChild(element)
                element.click()
                document.body.removeChild(element)
            },
        },

        data(){return{
            csvdata: null,
            href: null
            }
        },

    }
</script>

<style scoped>
    .result_container{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        padding: 5px;
        /*backdrop-filter: blur(10px);
        background-color: var(--light_gray_70);*/
        z-index: 2;
        color: var(--dark_gray);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .name_container {
        width: 90%;
        max-height: 10%;
    }

    .results{
        height: 80%;
        width: 90%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        overflow: auto;
    }

    .buttons-container {
        display: flex;
        justify-content: space-around;
        width: 90%;
        max-height: 10%;
        padding: 10px;
    }

    .btn_base {
        font-weight: 600;
        font-size: 1.3rem;
        width: 20%;
        margin: 10px;
    }

    table {
        border-collapse: collapse;
        width: 100%;
    }

    th {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
    }

    td {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
        text-align: center;
        font-size: 1.6rem;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }

</style>