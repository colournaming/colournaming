const path = require('path')
const webpack = require('webpack')

module.exports = {
  entry: {
    namer: './assets/js/colour-namer.js',
    experiment: './assets/js/experiment.js'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'colournaming/static')
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
};
