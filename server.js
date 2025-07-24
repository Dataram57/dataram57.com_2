const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, 'result', req.url);
    console.log(filePath);
    // Default to serving index.html if no specific file is requested
    if (req.url.lastIndexOf('.') < req.url.lastIndexOf('/')) {
        filePath = path.join(filePath, 'index.html');
    }
    console.log(filePath);
    // Check if the requested file exists
    fs.exists(filePath, (exists) => {
        if (exists) {
            // Read the file and serve its content
            fs.readFile(filePath, (err, data) => {
                if (err) {
                    res.writeHead(500, {'Content-Type': 'text/plain'});
                    res.end('Internal Server Error');
                } else {
                    // Determine the content type based on file extension
                    const contentType = getContentType(filePath);
                    res.writeHead(200, {'Content-Type': contentType});
                    res.end(data);
                }
            });
        } else {
            res.writeHead(404, {'Content-Type': 'text/plain'});
            res.end('404 Not Found');
        }
    });
});

// Helper function to determine content type based on file extension
function getContentType(filePath) {
    const extname = path.extname(filePath);
    switch (extname) {
        case '.html':
            return 'text/html';
        case '.css':
            return 'text/css';
        case '.js':
            return 'text/javascript';
        case '.json':
            return 'application/json';
        case '.png':
            return 'image/png';
        case '.jpg':
        case '.jpeg':
            return 'image/jpeg';
        default:
            return 'application/octet-stream';
    }
}

const PORT = process.env.PORT || 80;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
