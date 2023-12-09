import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css']
})
export class NotificationComponent {
  @Input() shiftNumber!: number;
  @Output() closeNotificationClick: EventEmitter<void> = new EventEmitter<void>();

  closeNotification() {
    this.closeNotificationClick.emit();
  }
}
