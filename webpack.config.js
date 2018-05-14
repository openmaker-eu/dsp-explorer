var webpack = require('./node_modules/webpack');
var BundleTracker = require('webpack-bundle-tracker');
var path = require('path');
var ContextReplacementPlugin = require('webpack/lib/ContextReplacementPlugin');

module.exports = {

    context: __dirname,

    entry: {
        dashboard: ['babel-polyfill', path.resolve('dashboard/static/js')],
        pss: ['babel-polyfill', path.resolve('pss/static/js') ],
    },

    output: {
        path: path.resolve("static/bundles"),
        publicPath: '/static/bundles/',
        filename: '[name]-[hash].js'
    },

    optimization: {
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendor',
                    chunks: 'all',
                },
                commons: {
                    name: "commons",
                    chunks: "initial",
                    minChunks: 2
                }
            }
        }
    },

    module: {
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
                    { loader: "css-loader" },
                    { loader: "sass-loader"}
                ]
            },
            {
                test: /\.js?$/,
                exclude:  /node_modules/,
                use: {
                    loader: 'babel-loader'
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

    resolve: {
        modules: ['node_modules']
    },

    plugins: [
        // replace moment require with empty module
        new ContextReplacementPlugin(/\.\/locale$/, 'empty-module', false, /js$/),
        new BundleTracker({filename: './webpack-stats.json'}),
        // provide global plugins (EG jquery, lodash)
        new webpack.ProvidePlugin({
            jQuery: 'jquery',
            $: 'jquery',
            jquery: 'jquery',
        }),
    ]
   

};