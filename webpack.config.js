const path = require('path')
const webpack = require('webpack')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

module.exports = {
  entry: {
    namer: './assets/js/colour-namer.js',
    experiment: './assets/js/experiment.js'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'colournaming/static')
  },
  module: {
    loaders: [{
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
    }]
  },
  plugins: [
    new UglifyJsPlugin({
      test: /\.js$/,
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
};
