const path = require('path');

module.exports = {
  entry: './assets/index2.js',  // Path to your input file
  output: {
    filename: 'index-bundle.js',  // Output bundle file name
    path: path.resolve(__dirname, 'static'),  // Path to your Django static directory
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Resolve both .js and .jsx extensions
  },
  mode: 'development',  // Set the mode to development; you might want to change this to 'production' for production builds
};
