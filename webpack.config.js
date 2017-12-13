const path = require('path')
const webpack = require('webpack')

module.exports = {
  entry: './assets/js/colour-namer.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'colournaming/static')
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
};
