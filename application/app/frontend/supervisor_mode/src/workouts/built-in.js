/*
const three_mins = {
    name: "3 MINUTES",
    workout : [
        {
          type: "PREPARE",
          exercise: "PREPARE",
          time: 5,
          max_reps: 0
        },
        {
          type: "WORK",
          exercise: "",
          time: 180,
          max_reps: 64000
        },
    ]
}

const five_mins = {
    name: "5 MINUTES",
    workout : [
        {
          type: "PREPARE",
          exercise: "PREPARE",
          time: 5,
          max_reps: 0
        },
        {
          type: "WORK",
          exercise: "",
          time: 300,
          max_reps: 64000
        },
    ]
}

const ten_mins = {
    name: "10 MINUTES",
    workout : [
        {
          type: "PREPARE",
          exercise: "PREPARE",
          time: 5,
          max_reps: 0
        },
        {
          type: "WORK",
          exercise: "",
          tim: 600,
          max_reps: 64000
        },
    ]
}

const thirty_mins = {
    name: "30 MINUTES",
    workout : [
        {
          type: "PREPARE",
          exercise: "PREPARE",
          time: 5,
          max_reps: 0
        },
        {
          type: "WORK",
          exercise: "",
          time: 1800,
          max_reps: 64000
        },
    ]
}
*/

const penthathlon = {
    name : "PENTATHLON",
    workout : [
      {
        type: "PREPARE",
        exercise: "PREPARE",
        time: 5,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "CLEAN",
        time: 360,
        max_reps: 120
      },
      {
        type: "REST",
        exercise: "REST",
        time: 300,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "CLEAN & PRESS",
        time: 360,
        max_reps: 60
      },
      {
        type: "REST",
        exercise: "REST",
        time: 300,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "JERK",
        time: 360,
        max_reps: 120
      },
      {
        type: "REST",
        exercise: "REST",
        time: 300,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "HALF SNATCH",
        time: 360,
        max_reps: 108
      },
      {
        type: "REST",
        exercise: "REST",
        time: 300,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "PUSH PRESS",
        time: 360,
        max_reps: 120
      },
    ]
  }

const half_penthathlon = {
    name : "HALF PENTATHLON",
    workout : [
      {
        type: "PREPARE",
        exercise: "PREPARE",
        time: 5,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "CLEAN",
        time: 180,
        max_reps: 60
      },
      {
        type: "REST",
        exercise: "REST",
        time: 120,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "CLEAN & PRESS",
        time: 180,
        max_reps: 30
      },
      {
        type: "REST",
        exercise: "REST",
        time: 120,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "JERK",
        time: 180,
        max_reps: 60
      },
      {
        type: "REST",
        exercise: "REST",
        time: 120,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "HALF SNATCH",
        time: 180,
        max_reps: 54
      },
      {
        type: "REST",
        exercise: "REST",
        time: 120,
        max_reps: 0
      },
      {
        type: "WORK",
        exercise: "PUSH PRESS",
        time: 180,
        max_reps: 60
      },
    ]
  }


const test_penta = {
  name : "TEST PENTA",
  workout : [
    {
      type: "PREPARE",
      exercise: "PREPARE",
      time: 5,
      max_reps: 0
    },
    {
      type: "WORK",
      exercise: "CLEAN",
      time: 10,
      max_reps: 10
    },
    {
      type: "REST",
      exercise: "REST",
      time: 5,
      max_reps: 0
    },
    {
      type: "WORK",
      exercise: "CLEAN & PRESS",
      time: 10,
      max_reps: 10
    },
    {
      type: "REST",
      exercise: "REST",
      time: 5,
      max_reps: 0
    },
    {
      type: "WORK",
      exercise: "JERK",
      time: 10,
      max_reps: 10
    },
    {
      type: "REST",
      exercise: "REST",
      time: 5,
      max_reps: 0
    },
    {
      type: "WORK",
      exercise: "HALF SNATCH",
      time: 10,
      max_reps: 10
    },
    {
      type: "REST",
      exercise: "REST",
      time: 5,
      max_reps: 0
    },
    {
      type: "WORK",
      exercise: "PUSH PRESS",
      time: 10,
      max_reps: 10
    },
  ]
}



export const workouts = [
    //three_mins,
    //five_mins,
    //ten_mins,
    //thirty_mins,
    penthathlon,
    half_penthathlon,
    test_penta,
]