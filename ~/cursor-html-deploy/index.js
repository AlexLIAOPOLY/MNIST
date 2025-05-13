#!/usr/bin/env node

const express = require('express');
const bodyParser = require('body-parser');
const ngrok = require('ngrok');
const fs = require('fs');
const path = require('path');
const os = require('os');

const app = express();
const port = 3456;
let currentContent = '';
let publicUrl = '';

// 增加对JSON请求体的支持，设置较大的限制
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.text({ limit: '50mb' }));

// MCP方法：部署HTML内容
const deployHtml = async (req, res) => {
  try {
    const content = req.body.value || '';
    currentContent = content;
    
    // 返回部署URL
    res.json({ url: publicUrl });
  } catch (error) {
    console.error('Deploy error:', error);
    res.status(500).json({ error: error.message });
  }
};

// 设置API路由
app.post('/mcp', (req, res) => {
  const method = req.query.method;
  
  if (method === 'deployHtml') {
    return deployHtml(req, res);
  }
  
  res.status(404).json({ error: 'Method not found' });
});

// 展示当前部署的HTML内容
app.get('/', (req, res) => {
  res.send(currentContent || '<html><body><h1>No content deployed yet</h1></body></html>');
});

// 启动服务器
app.listen(port, async () => {
  console.log(`HTML Deploy server running on http://localhost:${port}`);
  
  try {
    // 创建公共URL
    publicUrl = await ngrok.connect({
      addr: port,
      region: 'us'
    });
    console.log(`Public URL: ${publicUrl}`);
    
    // 输出MCP协议信息
    console.log(JSON.stringify({
      name: 'cursor_html_deploy',
      version: '1.0',
      tools: {
        deploy_html: {
          description: 'Deploy HTML content to a public URL',
          parameters: {
            value: {
              type: 'string',
              description: 'HTML or text content to deploy'
            }
          },
          returns: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'Public URL where content is deployed'
              }
            }
          }
        }
      }
    }));
  } catch (error) {
    console.error('Ngrok error:', error);
  }
});

process.on('SIGINT', async () => {
  console.log('Shutting down...');
  await ngrok.kill();
  process.exit(0);
}); 