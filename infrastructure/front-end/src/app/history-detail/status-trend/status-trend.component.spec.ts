import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatusTrendComponent } from './status-trend.component';

describe('StatusTrendComponent', () => {
  let component: StatusTrendComponent;
  let fixture: ComponentFixture<StatusTrendComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StatusTrendComponent]
    });
    fixture = TestBed.createComponent(StatusTrendComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
