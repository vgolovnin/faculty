var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker');


module.exports = {
    context: path.join(__dirname, 'academic', 'assets'),
    entry: {
        main: './index.js',
        // academic_admin: './admin/academic_admin.js',
    },
    output: {
        path: path.resolve(__dirname, './dist'),
        publicPath: '/dist/',
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        css: 'style-loader!css-loader',
                        scss: 'style-loader!css-loader!sass-loader'
                    }
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                loader: "style-loader!css-loader"
            },
            {
                test: /\.scss$/,
                loader: "style-loader!css-loader!sass-loader",
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "url-loader?limit=10000&mimetype=application/font-woff"
            },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file-loader"
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    devServer: {
        hot: true,
        proxy: {'**': 'http://localhost:8000/'},
    },
    performance: {
        hints: false
    },
    devtool: '#eval-source-map',

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify(process.env.NODE_ENV),
                APP_URL: `'/'`,
            }
        }),
    ],
}

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map'
    module.exports.plugins.concat([
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        })
    ])
}
