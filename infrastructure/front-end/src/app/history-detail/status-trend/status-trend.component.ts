import { Component, OnInit, Input, SimpleChanges, OnChanges } from '@angular/core';
import Chart from 'chart.js/auto';
import { FatigueHistory } from '../../model/history.model';

@Component({
  selector: 'app-status-trend',
  templateUrl: './status-trend.component.html',
  styleUrls: ['./status-trend.component.css']
})
export class StatusTrendComponent implements OnInit, OnChanges {
  public chart: any;
  @Input() trendData: FatigueHistory[] = [];
  @Input() duration: string = '';

  fatigueCount: number = 0;
  notFatigueCount: number = 0;
  dateRange: string = '';

  ngOnInit(): void {
    this.createChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['trendData'] || changes['duration']) {
      this.updateCounts();
      this.createChart();
    }
  }

  private updateCounts(): void {
    const organizedData = this.organizeDataByDate(this.trendData);
    this.fatigueCount = 0;
    this.notFatigueCount = 0;

    Object.values(organizedData).forEach(count => {
      this.fatigueCount += count.fatigue;
      this.notFatigueCount += count.notFatigue;
    });
  }

  createChart(): void {
    if (this.chart) {
      this.chart.destroy();
    }

    const organizedData = this.organizeDataByDate(this.trendData);
    
    const chartDataValues = Object.values(organizedData).map(data => data.fatigue);
    const maxDataValue = Math.max(...chartDataValues);
    
    const chartData = {
      labels: Object.keys(organizedData),
      datasets: [{
        label: 'Fatigue Count',
        data: chartDataValues,
        backgroundColor: 'green',
        borderColor: 'green',
        pointRadius: 4,
        fill: false
      }]
    };

    const chartOptions = {
      aspectRatio: 2.5,
      scales: {
        y: {
          beginAtZero: true,
          max: maxDataValue + 2,
          ticks: {
            stepSize: 1
          }
        },
        x: {
          grid: {
            drawOnChartArea: false
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    };

    this.chart = new Chart('MyChart', {
      type: 'line',
      data: chartData,
      options: chartOptions
    });
  }

  private organizeDataByDate(data: FatigueHistory[]): Record<string, { fatigue: number; notFatigue: number }> {
    const endDate = new Date();
    let startDate = new Date();

    switch (this.duration) {
      case 'week':
        startDate.setDate(endDate.getDate() - 7);
        break;
      case 'fortnight':
        startDate.setDate(endDate.getDate() - 15);
        break;
      case 'month':
        startDate.setDate(endDate.getDate() - 30);
        break;
    }
    this.dateRange = `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`;

    const counts: Record<string, { fatigue: number; notFatigue: number }> = {};
    let totalDays = 0;

    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
      const formattedDate = `${d.getMonth() + 1}/${d.getDate()}`;
      counts[formattedDate] = { fatigue: 0, notFatigue: 0 };
      totalDays++;
    }

    data.forEach(item => {
      const date = new Date(item.created_at);
      const formattedDate = `${date.getMonth() + 1}/${date.getDate()}`;
      if (formattedDate in counts) {
        counts[formattedDate].fatigue += 1;
      }
    });

    Object.keys(counts).forEach(key => {
      counts[key].notFatigue = 1 - counts[key].fatigue; // Assuming every day has either fatigue or not fatigue
    });

    this.fatigueCount = data.length;
    this.notFatigueCount = totalDays - this.fatigueCount;

    return counts;
  }
}
