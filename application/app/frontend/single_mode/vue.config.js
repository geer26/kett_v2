const { defineConfig } = require('@vue/cli-service')

//PRODUCTION SETTING
//UNCOMMENT ON COMPILE

module.exports = defineConfig({
    publicPath: '../../static/single_dist',
    outputDir: '../../static/single_dist',
    indexPath: '../../templates/single_vue.html',

    configureWebpack: {
      devServer: {
        devMiddleware: {
            writeToDisk: true
        }
      }
    },

    transpileDependencies: true
})



//DEV SETTING
//UNCOMMENT AT DEV
/*
module.exports = defineConfig({
  transpileDependencies: true,
  // outputDir must be added to Django's TEMPLATE_DIRS
  outputDir: "./dist/",
  // assetsDir must match Django's STATIC_URL
  assetsDir: "static",
})
*/
