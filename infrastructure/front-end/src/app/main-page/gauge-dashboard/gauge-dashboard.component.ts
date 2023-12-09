import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { NgxGaugeType } from 'ngx-gauge/gauge/gauge';

@Component({
  selector: 'app-gauge-dashboard',
  templateUrl: './gauge-dashboard.component.html',
  styleUrls: ['./gauge-dashboard.component.css']
})
export class GaugeDashboardComponent implements OnInit, OnChanges {
  @Input() gaugeValue: number = 0; // This will hold the value passed from the parent

  gaugeType: NgxGaugeType = "arch";
  gaugeLabel: string = "Index";
  gaugeAppendText: string = "%";
  thresholdConfig = {
    '0': { color: 'green', "bgOpacity": 0.2 },
    '51': { color: 'orange', "bgOpacity": 0.2 },
    '81': { color: 'red', "bgOpacity": 0.2 }
  };

  markerConfig = {
    "0": { color: 'fff', size: 2, label: '0', type: 'line'},
    "50": { color: '#fff', size: 2, label: '50', type: 'line'},
    "80": { color: 'fff', size: 2, label: '80', type: 'line'},
    "100": { color: 'fff', size: 2, label: '100', type: 'line'},
  };

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['gaugeValue']) {
      // Handle the change in gaugeValue
      this.changeGaugeValue(changes['gaugeValue'].currentValue);
    }
  }

  changeGaugeValue(newValue: number) {
    this.gaugeValue = newValue;
  }
}
