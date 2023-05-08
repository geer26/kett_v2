const { defineConfig } = require('@vue/cli-service')

//PRODUCTION SETTING
//UNCOMMENT ON COMPILE
/*
module.exports = defineConfig({
    publicPath: '../../static/supervised_dist',
    outputDir: '../../static/supervised_dist',
    indexPath: '../../templates/supervised_vue.html',

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
  // outputDir must be added to Django's TEMPLATE_DIRS
  outputDir: "./dist/",
  // assetsDir must match Django's STATIC_URL
  assetsDir: "static",
})
