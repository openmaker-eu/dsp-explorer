var path = require("path")
var webpack = require('webpack')
require("babel-polyfill");
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
var BundleTracker = require('webpack-bundle-tracker');
var CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');
var ContextReplacementPlugin = require('webpack/lib/ContextReplacementPlugin');

module.exports = {

    entry: {
        dashboard: ['babel-polyfill', path.resolve(__dirname, 'dashboard/static/js') ],
        pss: [ path.resolve(__dirname, 'pss/static/js') ]
    },
    output: {
        path: path.join(__dirname, "static/bundles"),
        publicPath: '/static/bundles/',
        filename: "[name]-[chunkhash].js"
    },
    module : {
        rules: [
            {   test: /\.html?$/, loader: ["html-loader"] },
            {
                test: /\.css?$/,
                loaders: ["style-loader", "css-loader"]
            },
            {
                test: /\.scss?$/,
                use : [
                    { loader: "style-loader" },
                    { loader:  "css-loader" },
                    { loader: "sass-loader"
                        // ,
                        // options: {
                        //     sourceMap: true,
                        //     data: '@import "base";',
                        //     includePaths: [ path.resolve(__dirname, "./static/styles/") ]
                        // }
                    }
                ]
    
            },
            {
                test: /\.js?$/, loader: 'babel-loader' ,
                exclude:  /node_modules/,
                query: {
                    presets: [ 'es2015' , 'stage-0'],
                }
            },
            {
                test: /\.(jpe?g|png|gif|svg)$/i,
                use: [
                    'url-loader?limit=10000',
                    'img-loader'
                ]
            },
            {
                test: /\.(png|woff|woff2|eot|ttf|svg|json)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader?limit=100000&name=../fonts/[hash].[ext]'

            }

        ]
    },
    plugins: [
        // new ContextReplacementPlugin(
        //     /moment[\/\\]locale$/,
        //     /de|fr|hu|it|en|es/
        // ),,
        new ContextReplacementPlugin(/\.\/locale$/, 'empty-module', false, /js$/),
        
        new CommonsChunkPlugin({
            filename: "commons-[chunkhash].js",
            name: "commons"
        }),
        new BundleTracker(),
        new CleanObsoleteChunks()

    ],
    
    resolve : {
        extensions : [ '.js', '.css', '.scss', '.html' ],
        alias : {
            'basescss':  path.resolve(__dirname, "./static/styles/base.scss"),
        }
    }
}