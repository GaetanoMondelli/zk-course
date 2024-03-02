import * as tls from 'tls';
import * as fs from 'fs';

const options: tls.TlsOptions = {
  key: fs.readFileSync('keys/key.pem'),
  cert: fs.readFileSync('keys/cert.pem')
};

const server = tls.createServer(options, (socket) => {
//   console.log('server connected', socket.authorized ? 'authorized' : 'unauthorized');
  socket.write("42");
  socket.setEncoding('utf8');
  socket.pipe(socket);
});

server.listen(8000, () => {
  console.log('server listening on port 8000');
});
