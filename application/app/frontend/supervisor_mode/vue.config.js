const { defineConfig } = require('@vue/cli-service')

//PRODUCTION SETTING
//UNCOMMENT ON COMPILE
/*
module.exports = defineConfig({
    publicPath: '../../static/supervisor_dist',
    outputDir: '../../static/supervisor_dist',
    indexPath: '../../templates/supervisor_vue.html',

    configureWebpack: {
      devServer: {
        devMiddleware: {
            writeToDisk: true
        }
      }
    },

    transpileDependencies: true
})
*/


//DEV SETTING
//UNCOMMENT AT DEV

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: "./dist/",
  assetsDir: "static",
})

