import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryFilterComponent } from './history-filter.component';

describe('HistoryFilterComponent', () => {
  let component: HistoryFilterComponent;
  let fixture: ComponentFixture<HistoryFilterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HistoryFilterComponent]
    });
    fixture = TestBed.createComponent(HistoryFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
