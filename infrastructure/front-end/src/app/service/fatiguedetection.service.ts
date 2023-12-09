import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FatigueDetectionService {
  private socket1: WebSocket;
  private socket2: WebSocket;

  constructor() {

    this.socket1 = new WebSocket('ws://20.237.111.52:8000/ws1');
    this.initializeWebSocket(this.socket1, 'Socket1');

    this.socket2 = new WebSocket('ws://20.237.111.52:8000/ws2');

    this.initializeWebSocket(this.socket2, 'Socket2');
  }

  private initializeWebSocket(socket: WebSocket, socketName: string) {
    console.log(`${socketName} initialization started`);
    
    socket.onopen = (event) => {
      console.log(`${socketName} connection opened`, event);
    };

    socket.onerror = (event) => {
      console.error(`${socketName} WebSocket error`, event);
    };

    socket.onclose = (event) => {
      console.log(`${socketName} connection closed`, event);
    };
  }

  public getFatigueAlertsFromSocket1(): Observable<any> {
    return new Observable(observer => {
      this.socket1.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Message from Socket1:', data);
        observer.next(data);
      };
    });
  }

  public getFatigueAlertsFromSocket2(): Observable<any> {
    return new Observable(observer => {
      this.socket2.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Message from Socket2:', data);
        observer.next(data);
      };
    });
  }
}
