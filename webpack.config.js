var path = require("path")
var webpack = require('webpack')
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
var BundleTracker = require('webpack-bundle-tracker');
var CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');

module.exports = {

    entry: {
        dashboard: path.resolve(__dirname, 'dashboard/static/js')
        // enter a new entry point here
    },
    output: {
        path: path.join(__dirname, "static/bundles"),
        publicPath: '/static/bundles/',
        filename: "[name]-[chunkhash].js"
    },
    module : {
        rules: [
            { test: /\.html?$/, loader: ["html-loader"] },
            {
                test: /\.scss?$/,
                loaders: ["style-loader", "css-loader", "sass-loader"]
            },
            {
                test: /\.js?$/, loader: 'babel-loader' ,
                exclude:  /node_modules/,
                query: {
                    presets: [ 'es2015' , 'stage-0' ],
                }
            },
            {
                test: /\.(ttf|otf|eot|svg|woff2(\?\S*)?$)(\?[a-z0-9]+)?$/,
                loaders: [ "file-loader?name=fonts/[name].[ext]" ]
            }
        ]
    },
    plugins: [
        new CommonsChunkPlugin({
            filename: "commons-[chunkhash].js",
            name: "commons"
        }),
        new BundleTracker(),
        new CleanObsoleteChunks()
    ]
}