const path = require('path');

const isDev = process.env.NODE_ENV === 'development';

const config = {
    entry: {
        main: './src/index.js',
        minedetail: './src/minedetail.js'
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'static', 'frontend')
    },
    module: {
        rules: [
            {
                test: /\.js$/, // 匹配 .js 文件
                exclude: /node_modules/, // 排除 node_modules 目录
                use: {
                    loader: 'babel-loader', // 使用 babel-loader
                },
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
};

if (isDev) {
    config.mode = 'development';
} else {
    config.mode = 'production';
}

module.exports = config;