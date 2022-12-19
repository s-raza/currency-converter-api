const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/currencies',
    createProxyMiddleware({
      target: process.env.REACT_APP_PROXY_HOST || 'http://localhost:8080',
      changeOrigin: true,
    })
  );
}
